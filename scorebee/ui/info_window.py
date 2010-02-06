# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/info_window.ui'
#
# Created: Sat Feb  6 11:56:25 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_info_window(object):
    def setupUi(self, info_window):
        info_window.setObjectName("info_window")
        info_window.setWindowModality(QtCore.Qt.NonModal)
        info_window.resize(325, 295)
        info_window.setAutoFillBackground(False)
        info_window.setStyleSheet("background-color: white")
        self.gridLayout = QtGui.QGridLayout(info_window)
        self.gridLayout.setMargin(8)
        self.gridLayout.setObjectName("gridLayout")
        self.textarea = QtGui.QTextBrowser(info_window)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        self.textarea.setFont(font)
        self.textarea.setFrameShape(QtGui.QFrame.NoFrame)
        self.textarea.setAcceptRichText(False)
        self.textarea.setObjectName("textarea")
        self.gridLayout.addWidget(self.textarea, 0, 0, 1, 1)

        self.retranslateUi(info_window)
        QtCore.QMetaObject.connectSlotsByName(info_window)

    def retranslateUi(self, info_window):
        info_window.setWindowTitle(QtGui.QApplication.translate("info_window", "ScoreBee - Info", None, QtGui.QApplication.UnicodeUTF8))
        self.textarea.setHtml(QtGui.QApplication.translate("info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Courier\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">fruit:</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">apple</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">key:</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">a long value; a long value; a long value; a long value; a long value; </p></td></tr></table></body></html>", None, QtGui.QApplication.UnicodeUTF8))

