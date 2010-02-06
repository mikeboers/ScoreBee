
from .qt import *
from .ui.timeline_window import Ui_timeline_window


class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.ui = Ui_timeline_window()
        self.ui.setupUi(self)
        
        # Kill the status bar.
        self.setStatusBar(None)
    
    def set_canvas_height(self, height):    
        self.ui.canvas.setMinimumSize(0, height)
        
    def resizeEvent(self, event):
        size = event.size()
        width = size.width()
        self.set_canvas_height(width/4)
        