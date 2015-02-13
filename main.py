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


class DataFrameModel(QtCore.QAbstractTableModel):

    def __init__(self, df=None):
        self.df = df
        super(DataFrameModel, self).__init__()

    def data(self, index, role):
        row = self.df.index[index.row()]
        column = self.df.columns[index.column()]
        return str(self.df[column][row])

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            return self.df.columns[section]
        return self.df.index[section]

    def rowCount(self, parent):
        return self.df.shape[0]

    def columnCount(self, parent):
        return self.df.shape[1]


class MainWindow(QtGui.QMainWindow):

    def __init__(self, filepath=None):
        super(MainWindow, self).__init__()
        self.filepath = filepath
        self.read_csv()

        self.tableView = QtGui.QTableView(self)
        self.dataFrameModel = DataFrameModel(self.df)
        self.tableView.setModel(self.dataFrameModel)

        self.setCentralWidget(self.tableView)

    def read_csv(self):
        self.df = pd.read_csv(self.filepath)


if __name__ == '__main__':
    filepath = op.join(op.dirname(__file__), "iris.csv")
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(filepath)
    window.show()
    app.exec_()
    sys.exit()
