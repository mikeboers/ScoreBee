
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
        
        self.ui.time.mousePressEvent = self.time_mousePress
        
        # Connect all the buttons.
        for name in 'pause play step fast_forward rewind go_to_start'.split():
            connect(getattr(self.ui, name), SIGNAL('clicked()'), getattr(self, '%s_button' % name))
    
    @property
    def mp(self):
        return self.app.mp
    
    def pause_button(self):
        log.debug('pause')
        self.mp.pause()
    
    def play_button(self):
        log.debug('play')
        self.mp.play()
    
    def step_button(self):
        log.debug('step')
        if not self.mp.is_paused:
            self.mp.pause()
        self.mp._cmd('frame_step')
        self.app.sync()
        
    def fast_forward_button(self):
        if abs(self.speed) >= 8:
            log.debug('too fast already')
        elif self.speed > 0:
            self.speed *= 2
        else:
            self.speed /= 2
        self.app.speed = self.speed
        log.debug('fast_forward %r' % self.speed)
    
    def rewind_button(self):
        if abs(self.speed) * 8 <= 1:
            log.debug('too slow already')
        elif self.speed > 0:
            self.speed /= 2
        else:
            self.speed *= 2
        self.app.speed = self.speed
        log.debug('rewind %r' % self.speed)
    
    def go_to_start_button(self):
        log.debug('go_to_start')
        self.mp.time = 0
        self.app.time = 0
    
    @property
    def speed(self):
        return self.mp.speed
    
    @speed.setter
    def speed(self, value):
        self.mp.speed = value
        self.ui.speed.setText('speed: %sx' % self.speed)
    
    def time_changed(self):
        time = self.app.time
        self.ui.time.setText(self.app.format_time())
        
    def time_mousePress(self, event):
        log.debug('time clicked')
        self.app.next_time_mode()

