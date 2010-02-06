
from .qt import *
from .ui.timeline_window import Ui_timeline_window


class TimelineWindow(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)
        self.ui = Ui_timeline_window()
        self.ui.setupUi(self)
    
    def set_canvas_height(self, height):    
        self.ui.canvas.setMinimumSize(0, height)
        
    def resizeEvent(self, event):
        print 'resized', event,
        size = event.size()
        width = size.width()
        print width
        self.set_canvas_height(width/4)
        