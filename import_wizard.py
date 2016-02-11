#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""

"""

from PyQt4 import QtGui, QtCore
from data_frame_model import DataFrameModel
import pandas as pd
from misc import colnames


class QDelimtierSelectorBox(QtGui.QComboBox):

    def __init__(self, parent):
        super(QDelimtierSelectorBox, self).__init__(parent=parent)
        self.delimMap = {"Comma": ",",
                         "Tab": "\t",
                         "Space": " "}
        self.addItems(self.delimMap.keys())
        self.currentIndexChanged.connect(self.changePreviewDelimiter)

    @QtCore.pyqtSlot(QtCore.QObject, int)
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

    @QtCore.pyqtSlot(QtCore.QObject, int)
    def changePreviewIndex(self, newInt):
        setattr(self.parent(), "INDEX_COL", self.indexList[newInt])
        self.parent().changePreviewIndex(self.indexList[newInt])


class QNRowsSelectorBox(QtGui.QLineEdit):

    def __init__(self, parent, orgNrows):
        super(QNRowsSelectorBox, self).__init__(parent=parent)
        self.setText(str(orgNrows))
        validator = QtGui.QIntValidator(0, orgNrows, self)
        self.setValidator(validator)


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

    @QtCore.pyqtSlot(QtCore.QObject, str)
    def changeParserEngine(self, toggled):
        for engineBtn in (self.c_select, self.py_select):
            if engineBtn.isChecked():
                break
        parser = engineBtn.text().lower()
        setattr(self.parent(), "PARSER_ENGINE", parser)
        self.parent().preview()


class ColumnSelectorWidget(QtGui.QDialog):

    def __init__(self, colList, parent=None):
        super(ColumnSelectorWidget, self).__init__(parent=parent)
        self.colList = colList

        allSelector = QtGui.QCheckBox("All Columns")
        allSelector.setChecked(True)
        allSelector.stateChanged.connect(self.toggleCBoxList)
        self.allSelector = allSelector

        noneSelector = QtGui.QPushButton("Select None")
        noneSelector.clicked.connect(self.triggerNoneSelect)
        self.noneSelector = noneSelector

        layout = QtGui.QVBoxLayout()
        masterSelectors = QtGui.QHBoxLayout()
        masterSelectors.addWidget(self.allSelector)
        masterSelectors.addWidget(self.noneSelector)
        layout.addLayout(masterSelectors)
        self.cBoxList = []
        for col in colList:
            cBox = QtGui.QCheckBox(str(col))
            cBox.setChecked(True)
            cBox.setEnabled(False)
            self.cBoxList.append(cBox)
        for cBox in self.cBoxList:
            layout.addWidget(cBox)

        # Ok/ Cancel Layout
        ok_pb = QtGui.QPushButton("OK")
        ok_pb.clicked.connect(self.accept)
        no_pb = QtGui.QPushButton("Cancel")
        no_pb.clicked.connect(self.reject)
        okCancelLayout = QtGui.QHBoxLayout()
        okCancelLayout.addWidget(ok_pb)
        okCancelLayout.addWidget(no_pb)
        layout.addLayout(okCancelLayout)

        self.setLayout(layout)

    def toggleCBoxList(self):
        if not self.allSelector.isChecked():
            for cBox in self.cBoxList:
                if cBox.text() != self.parent().INDEX_COL:
                    cBox.setEnabled(True)
        else:
            for cBox in self.cBoxList:
                cBox.setChecked(True)
                cBox.setEnabled(False)

    def triggerNoneSelect(self):
        self.allSelector.setChecked(False)
        for cBox in self.cBoxList:
            cBox.setChecked(False)


class DateTimeColumnSelector(QtGui.QDialog):

    def __init__(self, colList, parent=None):
        super(DateTimeColumnSelector, self).__init__(parent=parent)
        self.colList = colList
        self.dateTimeCols = []

        layout = QtGui.QVBoxLayout()
        cBoxList = []
        for col in colList:
            cBox = QtGui.QCheckBox(str(col))
            cBox.setChecked(False)
            cBoxList.append(cBox)
        for cBox in cBoxList:
            layout.addWidget(cBox)
        self.cBoxList = cBoxList

        # Ok/ Cancel Layout
        ok_pb = QtGui.QPushButton("OK")
        ok_pb.clicked.connect(self.accept)
        no_pb = QtGui.QPushButton("Cancel")
        no_pb.clicked.connect(self.reject)
        okCancelLayout = QtGui.QHBoxLayout()
        okCancelLayout.addWidget(ok_pb)
        okCancelLayout.addWidget(no_pb)
        layout.addLayout(okCancelLayout)

        self.setLayout(layout)

    def accept(self):
        for box in self.cBoxList:
            if box.isChecked():
                self.dateTimeCols.append(box.text())
        if len(self.dateTimeCols) > 0:
            setattr(self.parent(), 'DATETIME_COLS', self.dateTimeCols)
        super(DateTimeColumnSelector, self).accept()


class QImportWizard(QtGui.QDialog):

    # Initialize default constants
    PREVIEW_NROWS = 100
    SEP = ','
    INDEX_COL = None
    HEADER = 0
    PARSER_ENGINE = "c"
    USECOLS = None
    NROWS = None
    DATETIME_COLS = False

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

        # Parser Engine layout
        parserSelector = QParserButton(self)
        parserSelectorLabel = QtGui.QLabel("Parser Engine")
        parserEngineLayout = QtGui.QHBoxLayout()
        parserEngineLayout.addWidget(parserSelectorLabel)
        parserEngineLayout.addWidget(parserSelector)
        paramLayout.addLayout(parserEngineLayout)

        # Column select dialog
        self.colSelector = ColumnSelectorWidget(
                                           self.previewData.columns.tolist(),
                                           parent=self)
        selectColsBtn = QtGui.QPushButton("Select Columns")
        selectColsBtn.clicked.connect(self.showColumnSelector)
        paramLayout.addWidget(selectColsBtn)

        # DateTime column selector dialog
        self.dateTimeColSelector = DateTimeColumnSelector(
                                            self.previewData.columns.tolist(),
                                            parent=self)
        selectDTimeColsBtn = QtGui.QPushButton("Select DateTime Columns")
        selectDTimeColsBtn.clicked.connect(self.dateTimeColSelector.exec_)
        paramLayout.addWidget(selectDTimeColsBtn)

        # Nrows selector widget
        nrows = self.getMaxRows()
        nrowsSelector = QNRowsSelectorBox(parent=self, orgNrows=nrows)
        nrowsSelectorLayout = QtGui.QHBoxLayout()
        nrowsSelectorLayout.addWidget(QtGui.QLabel("No. of rows"))
        nrowsSelectorLayout.addWidget(nrowsSelector)
        self.nrowsSelector = nrowsSelector
        paramLayout.addLayout(nrowsSelectorLayout)

        # Ok/ Cancel Layout
        ok_pb = QtGui.QPushButton("OK")
        ok_pb.clicked.connect(self.accept)
        no_pb = QtGui.QPushButton("Cancel")
        no_pb.clicked.connect(self.reject)
        okCancelLayout = QtGui.QHBoxLayout()
        okCancelLayout.addWidget(ok_pb)
        okCancelLayout.addWidget(no_pb)
        paramLayout.addLayout(okCancelLayout)

        # Layout
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.tableView)
        layout.addLayout(paramLayout)
        self.setLayout(layout)

    def getMaxRows(self):
        firstCol = colnames(str(self.filepath))[0]
        return pd.read_csv(str(self.filepath), usecols=[firstCol]).shape[0]

    def showColumnSelector(self):
        if self.colSelector.exec_() == QtGui.QDialog.Accepted:
            self.USECOLS = []
            for cBox in self.colSelector.cBoxList:
                if cBox.isChecked():
                    self.USECOLS.append(cBox.text())
            self.previewSelectedColumns()

    def preview(self):
        if self.filepath.endsWith(".tsv"):
            parser = pd.read_table
        parser = pd.read_csv
        self.previewData = parser(str(self.filepath),
                                  nrows=self.PREVIEW_NROWS, sep=self.SEP,
                                  index_col=self.INDEX_COL,
                                  header=self.HEADER,
                                  engine=self.PARSER_ENGINE,
                                  usecols=self.USECOLS)

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

    def previewSelectedColumns(self):
        self.previewModel = DataFrameModel(self.previewData[self.USECOLS])
        self.tableView.setModel(self.previewModel)

    def accept(self):
        self.NROWS = int(self.nrowsSelector.text())
        super(QImportWizard, self).accept()


if __name__ == '__main__':
    import os.path as op
    import sys
    filepath = op.join(op.dirname(__file__), "iris.csv")
    app = QtGui.QApplication(sys.argv)
    window = QImportWizard(None, filepath)
    window.show()
    app.exec_()
    sys.exit()
