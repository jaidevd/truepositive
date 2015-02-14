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


class QDelimtierSelectorBox(QtGui.QComboBox):

    def __init__(self, parent):
        super(QDelimtierSelectorBox, self).__init__(parent=parent)
        self.delimMap = {"Comma": ",",
                         "Tab": "\t",
                         "Space": " "}
        self.addItems(self.delimMap.keys())
        self.currentIndexChanged.connect(self.changePreviewDelimiter)

    @QtCore.Slot(QtCore.QObject, int)
    def changePreviewDelimiter(self, newInt):
        key = self.delimMap.keys()[newInt]
        setattr(self.parent(), "SEP", self.delimMap[key])
        self.parent().changePreviewDelimiter()


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


class QParserButton(QtGui.QWidget):

    def __init__(self, parent=None):
        super(QParserButton, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        c_select = QtGui.QRadioButton("C", parent=self)
        py_select = QtGui.QRadioButton("Python", parent=self)
        c_select.setChecked(True)
        c_select.toggled.connect(self.changeParserEngine)
        py_select.toggled.connect(self.changeParserEngine)
        layout.addWidget(c_select)
        layout.addWidget(py_select)
        self.setLayout(layout)
        self.c_select = c_select
        self.py_select = py_select

    @QtCore.Slot(QtCore.QObject, str)
    def changeParserEngine(self, toggled):
        for engineBtn in (self.c_select, self.py_select):
            if engineBtn.isChecked():
                break
        parser = engineBtn.text().lower()
        setattr(self.parent(), "PARSER_ENGINE", parser)
        self.parent().preview()


class QImportWizard(QtGui.QDialog):

    # Initialize default constants
    PREVIEW_NROWS = 100
    SEP = ','
    INDEX_COL = None
    HEADER = 0
    PARSER_ENGINE = "c"

    def __init__(self, parent, filepath=None):
        super(QImportWizard, self).__init__(parent)
        self.setWindowTitle("Import Wizard")
        self.setModal(True)
        if filepath is None:
            self.filepath = self.parent().filepath
        else:
            self.filepath = filepath
        self.preview()

        # TableView widget
        self.tableView = QtGui.QTableView()
        self.previewModel = DataFrameModel(self.previewData)
        self.tableView.setModel(self.previewModel)

        # Layout for all parameters
        paramLayout = QtGui.QVBoxLayout()

        # Index selector widget
        self.indexSelectorBox = QIndexSelectorBox(self,
                                                  self.previewData.columns)
        indexSelectorLabel = QtGui.QLabel("Index Column")
        indexColLayout = QtGui.QHBoxLayout()
        indexColLayout.addWidget(indexSelectorLabel)
        indexColLayout.addWidget(self.indexSelectorBox)
        paramLayout.addLayout(indexColLayout)

        # Delimiter selector Widget
        self.delimiterSelectorBox = QDelimtierSelectorBox(self)
        delimiterSelectorLabel = QtGui.QLabel("Delimiter")
        delimLayout = QtGui.QHBoxLayout()
        delimLayout.addWidget(delimiterSelectorLabel)
        delimLayout.addWidget(self.delimiterSelectorBox)
        paramLayout.addLayout(delimLayout)

        # Ok/ Cancel Layout
        ok_pb = QtGui.QPushButton("OK")
        ok_pb.clicked.connect(self.accept)
        no_pb = QtGui.QPushButton("Cancel")
        no_pb.clicked.connect(self.reject)
        okCancelLayout = QtGui.QHBoxLayout()
        okCancelLayout.addWidget(ok_pb)
        okCancelLayout.addWidget(no_pb)
        paramLayout.addLayout(okCancelLayout)

        # Parser Engine layout
        paramLayout.addWidget(QParserButton(self))

        # Layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.tableView)
        layout.addLayout(paramLayout)
        self.setLayout(layout)

    def preview(self):
        self.previewData = pd.read_csv(self.filepath,
                                       nrows=self.PREVIEW_NROWS, sep=self.SEP,
                                       index_col=self.INDEX_COL,
                                       header=self.HEADER,
                                       engine=self.PARSER_ENGINE)

    def changePreviewIndex(self, newCol):
        if newCol == "None":
            self.previewData.index = range(self.previewData.shape[0])
        else:
            newIndex = self.previewData[newCol]
            self.previewData.set_index(newIndex, inplace=True)
        self.previewModel = DataFrameModel(self.previewData)
        self.tableView.setModel(self.previewModel)

    def changePreviewDelimiter(self):
        self.preview()
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
