# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/timeline_window.ui'
#
# Created: Sat Feb  6 12:38:53 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_timeline_window(object):
    def setupUi(self, timeline_window):
        timeline_window.setObjectName("timeline_window")
        timeline_window.resize(772, 361)
        self.verticalLayout = QtGui.QVBoxLayout(timeline_window)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(timeline_window)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.canvas = QtGui.QWidget(self.scrollArea)
        self.canvas.setGeometry(QtCore.QRect(0, 0, 757, 200))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMinimumSize(QtCore.QSize(0, 200))
        self.canvas.setBaseSize(QtCore.QSize(0, 0))
        self.canvas.setStyleSheet("background-color:red")
        self.canvas.setObjectName("canvas")
        self.scrollArea.setWidget(self.canvas)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(200, 16, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalScrollBar = QtGui.QScrollBar(timeline_window)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalLayout.addWidget(self.horizontalScrollBar)
        spacerItem1 = QtGui.QSpacerItem(16, 16, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(timeline_window)
        QtCore.QMetaObject.connectSlotsByName(timeline_window)

    def retranslateUi(self, timeline_window):
        timeline_window.setWindowTitle(QtGui.QApplication.translate("timeline_window", "ScoreBee - Timeline", None, QtGui.QApplication.UnicodeUTF8))

