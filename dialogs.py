#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 jaidev <jaidev@newton>
#
# Distributed under terms of the MIT license.

"""

"""

from PySide import QtGui
from matplotlib.markers import MarkerStyle


class QSummStatDlg(QtGui.QDialog):
    def __init__(self, parent=None, text=None):
        super(QSummStatDlg, self).__init__(parent)
        self.desc = QtGui.QLabel(text)
        masterLayout = QtGui.QVBoxLayout(self)
        masterLayout.addWidget(self.desc)
        self.setLayout(masterLayout)


class PlotPropertiesDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(PlotPropertiesDialog, self).__init__(parent)

        masterLayout = QtGui.QVBoxLayout()

        # Plot Style
        plotStyleLayout = QtGui.QHBoxLayout()
        self.line_select = QtGui.QRadioButton("Line", self)
        self.line_select.setChecked(True)
        self.scatter_select = QtGui.QRadioButton("Scatter", self)
        plotStyleLayout.addWidget(QtGui.QLabel("Plot Style"))
        plotStyleLayout.addWidget(self.line_select)
        plotStyleLayout.addWidget(self.scatter_select)
        masterLayout.addLayout(plotStyleLayout)

        # Marker character selector
        markerLayout = QtGui.QHBoxLayout()
        markerLayout.addWidget(QtGui.QLabel("Marker"))
        self.markerSelector = QtGui.QComboBox(self)
        self.markerSelector.addItems(MarkerStyle.markers.keys())
        # FIXME: Fix the nothings
        markerLayout.addWidget(self.markerSelector)
        masterLayout.addLayout(markerLayout)

        # Markersize layout
        markerSizeLayout = QtGui.QHBoxLayout()
        markerSizeLayout.addWidget(QtGui.QLabel("Marker Size"))
        self.markerSizeSelector = QtGui.QLineEdit(self)
        self.markerSizeSelector.setValidator(QtGui.QDoubleValidator())
        markerSizeLayout.addWidget(self.markerSizeSelector)
        masterLayout.addLayout(markerSizeLayout)

        # ColorPicker
        # Default color
        self.color = 'b'
        colorSelectorBtn = QtGui.QPushButton("Colors")
        colorSelectorBtn.clicked.connect(self.showColorPicker)
        self.colorPicker = QtGui.QColorDialog(self)
        masterLayout.addWidget(colorSelectorBtn)

        # Grid bool
        gridSelectorLayout = QtGui.QHBoxLayout()
        gridSelectorLayout.addWidget(QtGui.QLabel("Show Grid"))
        self.gridSelector = QtGui.QCheckBox()
        self.gridSelector.setChecked(True)
        gridSelectorLayout.addWidget(self.gridSelector)
        masterLayout.addLayout(gridSelectorLayout)

        # Ok/Cancel layout
        ok_pb = QtGui.QPushButton("OK")
        ok_pb.clicked.connect(self.accept)
        no_pb = QtGui.QPushButton("Cancel")
        no_pb.clicked.connect(self.reject)
        okCancelLayout = QtGui.QHBoxLayout()
        okCancelLayout.addWidget(ok_pb)
        okCancelLayout.addWidget(no_pb)
        masterLayout.addLayout(okCancelLayout)

        self.setLayout(masterLayout)

    def accept(self):
        self.getKwargs()
        super(PlotPropertiesDialog, self).accept()

    def getKwargs(self):
        # Marker
        ix = self.markerSelector.currentIndex()
        marker = MarkerStyle.markers.keys()[ix]
        # Marker size
        markerSize = float(self.markerSizeSelector.text())
        # Plot style
        if self.line_select.isChecked():
            style = "line"
            self.plotKwargs = dict(style=style, marker=marker,
                                   markersize=markerSize, color=self.color,
                                   grid=self.gridSelector.isChecked())
        else:
            style = "scatter"
            self.plotKwargs = dict(style=style, marker=marker,
                                   s=markerSize, c=self.color,
                                   grid=self.gridSelector.isChecked())

    def showColorPicker(self):
        if self.colorPicker.exec_() == QtGui.QDialog.Accepted:
            self.color = self.colorPicker.currentColor().name()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = PlotPropertiesDialog()
    if window.exec_() == QtGui.QDialog.Accepted:
        print window.plotKwargs
    app.exec_()
    sys.exit()
