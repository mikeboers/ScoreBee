# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/status_window.ui'
#
# Created: Sat Feb  6 11:48:22 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_status_window(object):
    def setupUi(self, status_window):
        status_window.setObjectName("status_window")
        status_window.setWindowModality(QtCore.Qt.NonModal)
        status_window.resize(247, 132)
        status_window.setMaximumSize(QtCore.QSize(247, 132))
        self.verticalLayout = QtGui.QVBoxLayout(status_window)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(8, 8, 8, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.time = QtGui.QLabel(status_window)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(48)
        font.setWeight(75)
        font.setBold(True)
        self.time.setFont(font)
        self.time.setAutoFillBackground(False)
        self.time.setTextFormat(QtCore.Qt.PlainText)
        self.time.setScaledContents(False)
        self.time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.time.setObjectName("time")
        self.verticalLayout.addWidget(self.time)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.speed = QtGui.QLabel(status_window)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        font.setItalic(True)
        self.speed.setFont(font)
        self.speed.setObjectName("speed")
        self.horizontalLayout_2.addWidget(self.speed)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.sync = QtGui.QLabel(status_window)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.sync.setFont(font)
        self.sync.setStyleSheet("color: rgb(125, 0, 9)")
        self.sync.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sync.setObjectName("sync")
        self.horizontalLayout_2.addWidget(self.sync)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(-1, 6, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.go_to_start = QtGui.QToolButton(status_window)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/sweetie/24-arrow-first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.go_to_start.setIcon(icon)
        self.go_to_start.setIconSize(QtCore.QSize(24, 24))
        self.go_to_start.setAutoRaise(False)
        self.go_to_start.setObjectName("go_to_start")
        self.horizontalLayout.addWidget(self.go_to_start)
        self.rewind = QtGui.QToolButton(status_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/sweetie/24-arrow-back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rewind.setIcon(icon1)
        self.rewind.setIconSize(QtCore.QSize(24, 24))
        self.rewind.setAutoRaise(False)
        self.rewind.setObjectName("rewind")
        self.horizontalLayout.addWidget(self.rewind)
        self.play_backwards = QtGui.QToolButton(status_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/sweetie/24-arrow-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play_backwards.setIcon(icon2)
        self.play_backwards.setIconSize(QtCore.QSize(24, 24))
        self.play_backwards.setAutoRaise(False)
        self.play_backwards.setObjectName("play_backwards")
        self.horizontalLayout.addWidget(self.play_backwards)
        self.play = QtGui.QToolButton(status_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/sweetie/24-arrow-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.play.setIcon(icon3)
        self.play.setIconSize(QtCore.QSize(24, 24))
        self.play.setAutoRaise(False)
        self.play.setObjectName("play")
        self.horizontalLayout.addWidget(self.play)
        self.fast_forward = QtGui.QToolButton(status_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/sweetie/24-arrow-forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fast_forward.setIcon(icon4)
        self.fast_forward.setIconSize(QtCore.QSize(24, 24))
        self.fast_forward.setAutoRaise(False)
        self.fast_forward.setObjectName("fast_forward")
        self.horizontalLayout.addWidget(self.fast_forward)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(status_window)
        QtCore.QMetaObject.connectSlotsByName(status_window)

    def retranslateUi(self, status_window):
        status_window.setWindowTitle(QtGui.QApplication.translate("status_window", "ScoreBee Status", None, QtGui.QApplication.UnicodeUTF8))
        self.time.setText(QtGui.QApplication.translate("status_window", "00:00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.speed.setText(QtGui.QApplication.translate("status_window", "speed: 1.0x", None, QtGui.QApplication.UnicodeUTF8))
        self.sync.setText(QtGui.QApplication.translate("status_window", "SYNC", None, QtGui.QApplication.UnicodeUTF8))

import status_window_rc
