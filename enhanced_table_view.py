#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""
another table editor... # TODO: Get a life.
"""

from PySide import QtGui
from dialogs import PlotPropertiesDialog, QSummStatDlg
import numpy as np


class QEnhancedTableView(QtGui.QTableView):

    def __init__(self, parent=None, ax=None, histAx=None, barAx=None):
        super(QEnhancedTableView, self).__init__(parent)
        self.ax = ax
        self.histAx = histAx
        self.barAx = barAx
        self.setAlternatingRowColors(True)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)

        self.xyPlotMenu = QtGui.QMenu("&XY Plot")
        self.xyPlotLines = QtGui.QAction("&Lines", self,
                                         triggered=self.plotColsLine)
        self.xyPlotMenu.addAction(self.xyPlotLines)

        self.xyPlotScatter = QtGui.QAction("&Scatter", self,
                                           triggered=self.plotColsScatter)
        self.xyPlotMenu.addAction(self.xyPlotScatter)

        self.xyPlotMenu.addSeparator()

        self.editPlotAct = QtGui.QAction("&Properties", self,
                                         triggered=self.showPlotProperties)
        self.xyPlotMenu.addAction(self.editPlotAct)

        menu.addMenu(self.xyPlotMenu)

        self.histAct = QtGui.QAction("&Histogram", self,
                                     triggered=self.showHistogram)
        menu.addAction(self.histAct)

        self.barAct = QtGui.QAction("&Bar Chart", self,
                                    triggered=self.showBarChart)
        menu.addAction(self.barAct)

        self.summStatAct = QtGui.QAction("Su&mmary Statistics", self,
                                         triggered=self.showSummStats)
        menu.addAction(self.summStatAct)

        menu.exec_(event.globalPos())

    def showSummStats(self):
        df = self.model().df
        selection = self.selectionModel().selection()
        col = df.columns[selection[0].left()]
        desc = df[col].describe().to_string()
        dlg = QSummStatDlg(self, desc)
        dlg.show()

    def showHistogram(self):
        tabbedArea = self.parent().parent().tabbedArea
        tabbedArea.setCurrentIndex(1)
        self.redrawHistogram()

    def showBarChart(self):
        tabbedArea = self.parent().parent().tabbedArea
        tabbedArea.setCurrentIndex(2)
        self.redrawBarChart()

    def plotColsLine(self, **kwargs):
        df = self.model().df
        selection = self.selectionModel().selection()
        if len(selection) == 2:
            xCol = df.columns[selection[0].left()]
            yCol = df.columns[selection[1].left()]
        x = df[xCol].values
        y = df[yCol].values
        grid = kwargs.get("grid", False)
        self.ax.plot(x, y, **kwargs)
        self.ax.grid(grid)
        self.ax.set_xlabel(xCol)
        self.ax.set_ylabel(yCol)
        self.ax.figure.canvas.draw()

    def plotColsScatter(self, **kwargs):
        df = self.model().df
        selection = self.selectionModel().selection()
        if len(selection) == 2:
            xCol = df.columns[selection[0].left()]
            yCol = df.columns[selection[1].left()]
        x = df[xCol].values
        y = df[yCol].values
        grid = kwargs.pop('grid')
        self.ax.scatter(x, y, **kwargs)
        self.ax.grid(grid)
        self.ax.set_xlabel(xCol)
        self.ax.set_ylabel(yCol)
        self.ax.figure.canvas.draw()

    def showPlotProperties(self):
        dlg = PlotPropertiesDialog()
        if dlg.exec_() == QtGui.QDialog.Accepted:
            props = dlg.plotKwargs
            if props.pop('style') == "line":
                self.plotColsLine(**props)
            else:
                self.plotColsScatter(**props)

    def redrawHistogram(self):
        pos = self.parent().parent().binSlider.value()
        selection = self.selectionModel().selection()
        if len(selection) == 1:
            df = self.model().df
            xCol = df.columns[selection[0].left()]
            x = df[xCol]
            self.histAx.hist(x, pos)
            self.histAx.set_title(xCol)
        else:
            x = self.parent().parent().x
            self.histAx.hist(x, pos)
        self.histAx.figure.canvas.draw()

    def redrawBarChart(self):
        selection = self.selectionModel().selection()
        if len(selection) == 1:
            df = self.model().df
            xCol = df.columns[selection[0].left()]
            x = df[xCol]
            vcs = x.value_counts()
            self.barAx.bar(np.arange(vcs.shape[0]), vcs.values)
            self.barAx.set_title(xCol)
            self.barAx.set_xticks(np.arange(vcs.shape[0]) + 0.8)
            self.barAx.set_xticklabels(vcs.index)
        self.barAx.figure.canvas.draw()
