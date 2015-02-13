#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""

"""

from PySide import QtCore


class DataFrameModel(QtCore.QAbstractTableModel):

    def __init__(self, df=None):
        self.df = df
        super(DataFrameModel, self).__init__()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = self.df.index[index.row()]
            column = self.df.columns[index.column()]
            return str(self.df[column][row])
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.df.columns[section]
            return self.df.index[section]
        return

    def rowCount(self, parent):
        return self.df.shape[0]

    def columnCount(self, parent):
        return self.df.shape[1]



