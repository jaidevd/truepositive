#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""
blah
"""
from PySide import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as \
        FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from dialogs import PlotPropertiesDialog


class QCanvas(FigureCanvas):
    def __init__(self, figure, parent):
        super(QCanvas, self).__init__(figure)
        self.setParent(parent)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        self.editPlotPropsAct = QtGui.QAction("&Edit Properties", self,
                                              triggered=self.showPropsDialog)
        menu.addAction(self.editPlotPropsAct)
        menu.exec_(event.globalPos())

    def showPropsDialog(self):
        dlg = PlotPropertiesDialog(self)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            self.redrawAxes()

    def redrawAxes(self):
        pass


class MainWindow(QtGui.QMainWindow):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.mainWidget = QtGui.QWidget()
        l = QtGui.QVBoxLayout(self.mainWidget)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        y = np.sin(x)
        ax.plot(x, y)
        canvas = QCanvas(fig, self.mainWidget)
        l.addWidget(canvas)
        self.mainWidget.setLayout(l)
        self.setCentralWidget(self.mainWidget)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
