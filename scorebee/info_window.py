
from .qt import *
from .ui.info_window import Ui_info_window


class InfoWindow(QtGui.QDialog):

    def __init__(self, *args):
        QtGui.QDialog.__init__(self, *args)
        self.ui = Ui_info_window()
        self.ui.setupUi(self)