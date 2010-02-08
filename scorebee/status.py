
import logging

from .qt import *
from .ui.status_window import Ui_status_window as UI


log = logging.getLogger(__name__)


class StatusWindow(QtGui.QDialog):

    def __init__(self, app, *args):
        QtGui.QDialog.__init__(self, *args)
        self.app = app
        
        self.ui = UI()
        self.ui.setupUi(self)
        
        self.ui.time.mousePressEvent = self.time_mousePress
        
        # Connect all the buttons.
        for name in 'play step fast_forward rewind go_to_start'.split():
            connect(getattr(self.ui, name), SIGNAL('clicked()'), getattr(self, '%s_button' % name))
        
        connect(self.app, SIGNAL('time_changed'), self.handle_time_change_signal)
        connect(self.app, SIGNAL('time_mode_changed'), self.handle_time_change_signal)
        connect(self.app, SIGNAL('synced'), self.handle_synced_signal)
        
        self.play_icon = QIcon(":/icons/sweetie/24-arrow-next.png")
        self.pause_icon = QIcon(":/icons/sweetie/24-control-pause.png")
        
        connect(self.app, SIGNAL('pause_toggled'), self.handle_pause_toggled_signal)
    
    @property
    def mp(self):
        return self.app.video
    
    def play_button(self):
        log.debug('play/pause')
        self.app.toggle_pause()
    
    def handle_pause_toggled_signal(self):
        if self.app.video.is_paused:
            self.ui.play.setIcon(self.play_icon)
        else:
            self.ui.play.setIcon(self.pause_icon)
        
    
    def step_button(self):
        log.debug('step')
        self.app.video.step()
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
        self.app.video.time = 0
        self.app.time = 0
    
    @property
    def speed(self):
        return self.app.video.speed
    
    @speed.setter
    def speed(self, value):
        self.app.video.speed = value
        self.ui.speed.setText('speed: %sx' % self.speed)
    
    def handle_time_change_signal(self):
        time = self.app.time
        self.ui.time.setText(self.app.format_time())
    
    def handle_synced_signal(self, delta):
        self.ui.sync.setText('sync: %3dms' % abs(1000 * delta))
        
    def time_mousePress(self, event):
        log.debug('time clicked')
        self.app.next_time_mode()

