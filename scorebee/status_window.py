
import logging

from .qt import *
from .ui.status_window import Ui_status_window


log = logging.getLogger(__name__)


class StatusWindow(QtGui.QDialog):

    def __init__(self, app, *args):
        QtGui.QDialog.__init__(self, *args)
        self.app = app
        
        self.ui = Ui_status_window()
        self.ui.setupUi(self)
        
        # Connect all the buttons.
        for name in 'pause play play_backwards fast_forward rewind go_to_start'.split():
            connect(getattr(self.ui, name), SIGNAL('clicked()'), getattr(self, '%s_button' % name))
        
    def pause_button(self):
        log.debug('pause')
    
    def play_button(self):
        log.debug('play')
    
    def play_backwards_button(self):
        log.debug('play_backwards')
    
    def fast_forward_button(self):
        log.debug('fast_forward')
    
    def rewind_button(self):
        log.debug('rewind')
    
    def go_to_start_button(self):
        log.debug('go_to_start')