#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""
Write drunk, edit sober
"""

import sys
import pandas as pd
import os.path as op
from PySide import QtCore, QtGui
from import_wizard import QImportWizard
from data_frame_model import DataFrameModel
from q_canvas import QCanvas
from enhanced_table_view import QEnhancedTableView
import numpy as np
import matplotlib.pyplot as plt


class MyFileDialog(QtGui.QFileDialog):

    accepted = QtCore.Signal(QtCore.QObject)

    def __init__(self, parent=None):
        super(MyFileDialog, self).__init__()
        self.parent = parent

    def accept(self):
        super(MyFileDialog, self).accept()
        setattr(self.parent, "filepath", self.selectedFiles()[0])
        self.accepted.emit(self.parent)


class MainWindow(QtGui.QMainWindow):

    def __init__(self, filepath=None):
        super(MainWindow, self).__init__()

        self.getXYPlotArea()
        self.getHistPlotArea()

        self.filepath = filepath
        self.tableView = QEnhancedTableView(self, self.ax, self.histAx)

        self.tabbedArea = QtGui.QTabWidget()
        self.tabbedArea.addTab(self.xyCanvas, "XY Plots")
        histWidget = QtGui.QWidget(self.tabbedArea)
        histLayout = QtGui.QHBoxLayout()
        self.binSlider = QtGui.QSlider(QtCore.Qt.Vertical, parent=histWidget)
        self.binSlider.setRange(10, 100)
        self.binSlider.setSingleStep(10)
        self.binSlider.setTickPosition(QtGui.QSlider.TicksRight)
        self.binSlider.setTracking(False)
        self.binSlider.valueChanged.connect(self.tableView.redrawHistogram)
        histLayout.addWidget(self.histCanvas)
        histLayout.addWidget(self.binSlider)
        histWidget.setLayout(histLayout)
        self.tabbedArea.addTab(histWidget, "Histogram")

        centralSplitter = QtGui.QSplitter(self)
        centralSplitter.addWidget(self.tableView)
        centralSplitter.addWidget(self.tabbedArea)

        self.setCentralWidget(centralSplitter)
        self.parserKwargs = {}
        self.readCsv()

        # Menu Bar
        self.openFileDialog = MyFileDialog(parent=self)
        self.openFileDialog.accepted.connect(self.showImportWizard)

        menuBar = QtGui.QMenuBar()
        fileMenu = QtGui.QMenu("&File", parent=menuBar)
        openAct = fileMenu.addAction("Open")
        openAct.triggered.connect(self.openFileDialog.exec_)
        menuBar.addMenu(fileMenu)

        self.setMenuBar(menuBar)

    def readCsv(self):
        df = pd.read_csv(self.filepath, **self.parserKwargs)
        self.dataFrameModel = DataFrameModel(df)
        self.tableView.setModel(self.dataFrameModel)

    def showImportWizard(self):
        self.importWiz = QImportWizard(self)
        result = self.importWiz.exec_()
        if result == QtGui.QDialog.Accepted:
            self.makeParserKwargs()
            self.readCsv()

    def makeParserKwargs(self):
        self.parserKwargs = {"sep": self.importWiz.SEP,
                             "index_col": self.importWiz.INDEX_COL,
                             "engine": self.importWiz.PARSER_ENGINE,
                             "usecols": self.importWiz.USECOLS,
                             "nrows": self.importWiz.NROWS,
                             "parse_dates": self.importWiz.DATETIME_COLS}

    def getXYPlotArea(self):
        self.getExampleFigure()
        self.xyCanvas = QCanvas(self.fig, self)

    def getHistPlotArea(self):
        self.getExampleHist()
        self.histCanvas = QCanvas(self.histFig, self)

    def getExampleFigure(self):
        x = np.linspace(-2*np.pi, 2*np.pi, 1000)
        y = np.sin(x)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hold(False)
        ax.plot(x, y)
        self.ax = ax
        self.fig = fig

    def getExampleHist(self):
        x = np.random.random(1000)
        histFig = plt.figure()
        histAx = histFig.add_subplot(111)
        histAx.hold(False)
        histAx.hist(x, 100)
        self.x = x
        self.histAx = histAx
        self.histFig = histFig


if __name__ == '__main__':
    filepath = op.join(op.dirname(__file__), "iris.csv")
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(filepath)
    window.show()
    sys.exit(app.exec_())
