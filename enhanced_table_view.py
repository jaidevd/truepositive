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
from dialogs import PlotPropertiesDialog


class QEnhancedTableView(QtGui.QTableView):

    def __init__(self, parent=None, ax=None):
        super(QEnhancedTableView, self).__init__(parent)
        self.ax = ax
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

        menu.exec_(event.globalPos())

    def showHistogram(self):
        tabbedArea = self.parent().parent().tabbedArea
        tabbedArea.setCurrentIndex(1)

    def plotColsLine(self, **kwargs):
        df = self.model().df
        selection = self.selectionModel().selection()
        if len(selection) == 2:
            xCol = df.columns[selection[0].left()]
            yCol = df.columns[selection[1].left()]
        x = df[xCol].values
        y = df[yCol].values
        grid = kwargs.pop('grid')
        self.ax.plot(x, y, **kwargs)
        self.ax.grid(grid)
        self.ax.set_xlabel(xCol)
        self.ax.set_ylabel(yCol)

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

    def showPlotProperties(self):
        dlg = PlotPropertiesDialog()
        if dlg.exec_() == QtGui.QDialog.Accepted:
            props = dlg.plotKwargs
            if props.pop('style') == "line":
                self.plotColsLine(**props)
            else:
                self.plotColsScatter(**props)
