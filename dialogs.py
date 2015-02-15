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


class PlotPropertiesDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(PlotPropertiesDialog, self).__init__(parent)

        masterLayout = QtGui.QVBoxLayout()

        # Plot Style
        plotStyleLayout = QtGui.QHBoxLayout()
        line_select = QtGui.QRadioButton("Line", self)
        scatter_select = QtGui.QRadioButton("Scatter", self)
        plotStyleLayout.addWidget(QtGui.QLabel("Plot Style"))
        plotStyleLayout.addWidget(line_select)
        plotStyleLayout.addWidget(scatter_select)
        masterLayout.addLayout(plotStyleLayout)

        # Marker character selector
        markerLayout = QtGui.QHBoxLayout()
        markerLayout.addWidget(QtGui.QLabel("Marker"))
        markerSelector = QtGui.QComboBox(self)
        markerSelector.addItems(MarkerStyle.markers.values())
        markerLayout.addWidget(markerSelector)
        masterLayout.addLayout(markerLayout)

        # Markersize layout
        markerSizeLayout = QtGui.QHBoxLayout()
        markerSizeLayout.addWidget(QtGui.QLabel("Marker Size"))
        markerSizeSelector = QtGui.QLineEdit(self)
        markerSizeSelector.setValidator(QtGui.QDoubleValidator())
        markerSizeLayout.addWidget(markerSizeSelector)
        masterLayout.addLayout(markerSizeLayout)

        # ColorPicker
        colorSelectorBtn = QtGui.QPushButton("Colors")
        colorSelectorBtn.clicked.connect(self.showColorPicker)
        self.colorPicker = QtGui.QColorDialog(self)
        masterLayout.addWidget(colorSelectorBtn)

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
        pass

    def showColorPicker(self):
        if self.colorPicker.exec_() == QtGui.QDialog.Accepted:
            self.getColors()

    def getColors(self):
        pass

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = PlotPropertiesDialog()
    window.show()
    app.exec_()
    sys.exit()
