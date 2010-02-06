
import pdb

from PyQt4.QtCore import *
from PyQt4 import QtGui


connect = QObject.connect


def debug():
    pyqtRemoveInputHook()
    pdb.set_trace()
    pyqtRestoreInputHook()
