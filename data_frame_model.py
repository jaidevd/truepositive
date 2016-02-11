#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""
AbstractTableModel for Pandas dataframes
"""

from PyQt4 import QtCore


class DataFrameModel(QtCore.QAbstractTableModel):

    def __init__(self, df=None):
        self.df = df
        super(DataFrameModel, self).__init__()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.df.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.df.columns[section]
            return str(self.df.index[section])
        return

    def rowCount(self, parent):
        return self.df.shape[0]

    def columnCount(self, parent):
        return self.df.shape[1]
