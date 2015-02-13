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
        self.filepath = filepath
        self.tableView = QtGui.QTableView(self)
        self.setCentralWidget(self.tableView)
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
        df = pd.read_csv(self.filepath)
        self.dataFrameModel = DataFrameModel(df)
        self.tableView.setModel(self.dataFrameModel)

    def showImportWizard(self):
        self.importWiz = QImportWizard(self, filepath)
        self.importWiz.show()


if __name__ == '__main__':
    filepath = op.join(op.dirname(__file__), "iris.csv")
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(filepath)
    window.show()
    app.exec_()
    sys.exit()
