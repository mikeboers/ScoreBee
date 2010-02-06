
import pdb

from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4.QtGui import *

connect = QObject.connect


def debug():
    pyqtRemoveInputHook()
    pdb.set_trace()
    pyqtRestoreInputHook()


def patch(class_):
    def patcher(method):
        setattr(class_, method.__name__, method)
    return patcher


@patch(QPoint)
def __iter__(self):
    return iter((self.x(), self.y()))


@patch(QPoint)
def __getitem__(self, i):
    if i == 0:
        return self.x()
    elif i == 1:
        return self.y()
    raise IndexError(i)

  
@patch(QSize)
def __iter__(self):
    return iter((self.width(), self.height()))


@patch(QSize)
def __getitem__(self, i):
    if i == 0:
        return self.width()
    elif i == 1:
        return self.height()
    raise IndexError(i)