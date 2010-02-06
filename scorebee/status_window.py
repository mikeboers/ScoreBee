
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
        for name in 'pause play fast_forward rewind go_to_start'.split():
            connect(getattr(self.ui, name), SIGNAL('clicked()'), getattr(self, '%s_button' % name))
    
    @property
    def mp(self):
        return self.app.doc.mp
    
    def pause_button(self):
        log.debug('pause')
        self.mp.pause()
    
    def play_button(self):
        log.debug('play')
        self.mp.play()
    
    def fast_forward_button(self):
        if abs(self.mp.speed) >= 8:
            log.debug('too fast already')
        elif self.mp.speed > 0:
            self.mp.speed *= 2
        else:
            self.mp.speed /= 2
        self.app.speed = self.mp.speed
        log.debug('fast_forward %r' % self.mp.speed)
    
    def rewind_button(self):
        if abs(self.mp.speed) * 8 <= 1:
            log.debug('too slow already')
        elif self.mp.speed > 0:
            self.mp.speed /= 2
        else:
            self.mp.speed *= 2
        self.app.speed = self.mp.speed
        log.debug('rewind %r' % self.mp.speed)
    
    def go_to_start_button(self):
        log.debug('go_to_start')
        self.mp.time = 0
    
    
    def time_clicked(self):
        log.debug('time clicked')

