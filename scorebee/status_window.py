
from .qt import *
from .ui.status_window import Ui_status_window


class StatusWindow(QtGui.QDialog):

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        self.ui = Ui_status_window()
        self.ui.setupUi(self)