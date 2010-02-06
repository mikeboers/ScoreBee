
import sys

from scorebee.qt import *

from scorebee.status_window import StatusWindow


class Controller(object):
    
    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        self.status_window = StatusWindow()
    
    def run(self):
        self.status_window.show()
        self.app.exec_()

controller = Controller(sys.argv)

if __name__ == '__main__':
    controller.run()
