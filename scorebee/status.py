
import logging

from .qt import *
from .ui.status_window import Ui_status_window


log = logging.getLogger(__name__)


TIME_MODE_SECONDS = 'seconds'
TIME_MODE_FRAMES = 'frames'
time_mode_next = {
    TIME_MODE_SECONDS: TIME_MODE_FRAMES,
    TIME_MODE_FRAMES: TIME_MODE_SECONDS
}


class StatusWindow(QtGui.QDialog):

    def __init__(self, app, *args):
        QtGui.QDialog.__init__(self, *args)
        self.app = app
        
        self.ui = Ui_status_window()
        self.ui.setupUi(self)
        
        self.time_mode = TIME_MODE_FRAMES
        self.ui.time.mousePressEvent = self.time_mousePress
        
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
    
    def set_time(self, time):
        if self.time_mode == TIME_MODE_FRAMES:
            frames = int(time * self.mp.fps)
            seconds, frames = divmod(frames, self.mp.fps)
            minutes, seconds = divmod(seconds, 60)
            self.ui.time.setText('%02d:%02d:%02d' % (minutes, seconds, frames))
        else:
            self.ui.time.setText('%.2f' % time)
    
    
    def time_mousePress(self, event):
        log.debug('time clicked')
        self.time_mode = time_mode_next[self.time_mode]

