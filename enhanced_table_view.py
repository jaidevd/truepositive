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


class QEnhancedTableView(QtGui.QTableView):

    def __init__(self, parent=None, ax=None):
        super(QEnhancedTableView, self).__init__(parent)
        self.ax = ax
        self.createContextMenuActions()
        self.setAlternatingRowColors(True)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        for act in self.contextMenuActions:
            menu.addAction(act)
        menu.exec_(event.globalPos())

    def createContextMenuActions(self):
        self.contextMenuActions = []
        self.xyPlotAct = QtGui.QAction("&XY Plot", self,
                                       triggered=self.plotCols)
        self.contextMenuActions.append(self.xyPlotAct)

    def plotCols(self):
        df = self.model().df
        selection = self.selectionModel().selection()
        if len(selection) == 2:
            xCol = df.columns[selection[0].left()]
            yCol = df.columns[selection[1].left()]
        x = df[xCol].values
        y = df[yCol].values
        self.ax.plot(x, y)
        self.ax.set_xlabel(xCol)
        self.ax.set_ylabel(yCol)
