#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""

"""

from PySide import QtGui, QtCore
from data_frame_model import DataFrameModel
import pandas as pd


class QIndexSelectorBox(QtGui.QComboBox):

    def __init__(self, parent, dfColumns):
        super(QIndexSelectorBox, self).__init__(parent=parent)
        self.indexList = [str(None)] + dfColumns.tolist()
        self.addItems(self.indexList)
        self.currentIndexChanged.connect(self.changePreviewIndex)

    @QtCore.Slot(QtCore.QObject, int)
    def changePreviewIndex(self, newInt):
        setattr(self.parent(), "INDEX_COL", newInt)
        self.parent().changePreviewIndex(self.indexList[newInt])


class QImportWizard(QtGui.QDialog):

    # Initialize default constants
    PREVIEW_NROWS = 100
    SEP = ','
    INDEX_COL = None
    HEADER = 0

    def __init__(self, parent, filepath):
        super(QImportWizard, self).__init__(parent=parent)
        self.setWindowTitle("Import Wizard")
        self.setModal(True)
        self.filepath = filepath
        self.preview()

        # TableView widget
        self.tableView = QtGui.QTableView()
        self.previewModel = DataFrameModel(self.previewData)
        self.tableView.setModel(self.previewModel)

        # Index selector widget
        self.indexSelectorBox = QIndexSelectorBox(parent,
                                                  self.previewData.columns)
        indexSelectorLabel = QtGui.QLabel("Index Column")
        indexColLayout = QtGui.QHBoxLayout()
        indexColLayout.addWidget(indexSelectorLabel)
        indexColLayout.addWidget(self.indexSelectorBox)

        # Layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.tableView)
        layout.addLayout(indexColLayout)
        self.setLayout(layout)

    def preview(self):
        self.previewData = pd.read_csv(self.filepath,
                                       nrows=self.PREVIEW_NROWS, sep=self.SEP,
                                       index_col=self.INDEX_COL,
                                       header=self.HEADER)

    def changePreviewIndex(self, newCol):
        if newCol == "None":
            self.previewData.index = range(self.previewData.shape[0])
        else:
            newIndex = self.previewData[newCol]
            self.previewData.set_index(newIndex, inplace=True)
        self.previewModel = DataFrameModel(self.previewData)
        self.tableView.setModel(self.previewModel)


if __name__ == '__main__':
    import os.path as op
    import sys
    filepath = op.join(op.dirname(__file__), "iris.csv")
    app = QtGui.QApplication(sys.argv)
    window = QImportWizard(None, filepath)
    window.show()
    app.exec_()
    sys.exit()
