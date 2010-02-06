
from .qt import *
from .ui.status_window import Ui_status_window


class StatusWindow(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_status_window()
        self.ui.setupUi(self)