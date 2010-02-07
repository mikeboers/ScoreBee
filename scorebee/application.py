
import sys
import json
import os
import logging
import time

from .qt import *
from .timeline import TimelineWindow
from .status import StatusWindow
from .info import InfoWindow
from .document import Document, Track, Event
from .mplayer import MPlayer
from .util import next_time_mode, format_time
from . import config as cfg


log = logging.getLogger(__name__)


WINDOW_NAMES = 'status', 'info', 'timeline'



class Application(QObject):
    
    def __init__(self, argv):
        
        QObject.__init__(self)
        
        self.app = QtGui.QApplication(argv)
        
        # The document is accessed through a property because we need to
        # signal rebuilding the api whenever it is changed.
        self._doc = None
        self._mp = None
        
        # Build up the three windows.
        self.timeline = TimelineWindow(self)
        self.status   = StatusWindow(self, self.timeline)
        self.info     = InfoWindow(self, self.timeline)
        
        self.setup_menu()
        
        # Setup our main loop timer.
        self.idle_timer = QTimer()
        self.idle_timer.setInterval(10) # milliseconds
        self.idle_timer.timerEvent = self.main_loop
        
        self.last_loop_time = 0
        
        self.time = 0 # Our guess for the current time.
        self.mp_sync_time = 0 # Last time we synced to mplayer's time.
        self.mp_time_at_sync = 0 # What the time was when we synced.
        
        # The global time representation mode. Rotate this by calling
        # self.next_time_mode()
        self.time_mode = next_time_mode()
        
        # Some state to keep track of which keys are pressed.
        self.pressed_keys = set()
        self.key_to_track = {}
        self.key_to_open_event = {}
    
    def setup_menu(self):
        menubar = self.timeline.menuBar()
        window_menu = menubar.addMenu("Window")
        def make_handler(name):
            def handler():
                window = getattr(self, name)
                window.show()
                window.repaint()
                window.raise_()
            return handler
        for name in WINDOW_NAMES:
            action = QtGui.QAction(name.capitalize(), self.timeline)
            connect(action, SIGNAL('triggered()'), make_handler(name))
            window_menu.addAction(action)
            
    @property
    def mp(self):
        """Always a good (ie. running) mplayer."""
        if self._mp is None or not self._mp.is_running:
            self._mp = MPlayer(self.doc.src)
        return self._mp
    
    def format_time(self, time=None):
        """Format a time with the current time format mode."""
        return format_time(self.time if time is None else time, self.mp.fps, self.time_mode)
    
    def next_time_mode(self):
        """Rotate the time format mode."""
        self.time_mode = next_time_mode(self.time_mode)
        self.emit(SIGNAL('time_mode_changed'))
    
    @property
    def doc(self):
        """The open document.
        
        Setting this has major side effects."""
        return self._doc
    
    @doc.setter
    def doc(self, doc):
        
        self._doc = doc
        self._mp = None # Forces a new mplayer with the new video.
        self.mp.time = 0
        
        self.key_to_track = dict((track.key_code, track) for track in doc)
        self.emit(SIGNAL('doc_changed'))
        
        # We need the interface to be updated. This is the likely the best way
        # That I know.
        self.sync()
    
    def run(self):
        
        # Load and apply all of the window settings.
        # TODO: move this onto the window class itself.
        if os.path.exists('settings/windows.json'):
            window_prefs = json.load(open('settings/windows.json'))
            for name, data in window_prefs.iteritems():
                window = getattr(self, name)
                window.move(*data['pos'])
                window.resize(*data['size'])
            
        self.status.show()
        self.info.show()
        self.timeline.show()
        
        # Collect all of the key press events here.
        for name in WINDOW_NAMES:
            window = getattr(self, name)
            window.keyPressEvent = self.keyPressEvent
            window.keyReleaseEvent = self.keyReleaseEvent
        
        # Load a document.
        # We absolutely MUST have the document constructed fully BEFORE
        # setting it here. There are side effects to setting it.
        # HACK: This is just a hack for now.
        doc = Document('/Users/mikeboers/Desktop/example.MOV')
        # self.doc = Document('/Users/mikeboers/Desktop/C00000S00A20091231112932302.avi')
        doc.add_track(Track('A behaviour', 'q', [
            Event(10, 15), Event(50, 65), Event(500, 600)
        ]))
        doc.add_track(Track('Nothin here', 'w', []))
        doc.add_track(Track('Better one', 'e', [
            Event(25, 26), Event(70, 71), Event(700, 701)
        ]))
        
        self.doc = doc
        
        # Run the main loops.
        self.idle_timer.start()
        self.app.exec_()
        
        # HACK: Kill the MPlayer
        self.doc._mp = None
        
        # Save window sizes and locations for the next startup.
        window_prefs = {}
        for name in WINDOW_NAMES:
            window_prefs[name] = dict(
                pos=tuple(getattr(self, name).pos()),
                size=tuple(getattr(self, name).size()),
            )
        json.dump(window_prefs, open('settings/windows.json', 'w'), indent=4)
    
    @property
    def frame(self):
        return int(self.time * self.mp.fps)
    
    def main_loop(self, event=None, force_sync=False):
        """Event that is triggered every couple milliseconds.

        Treat this as our main loop.

        """
        now = time.time()
        time_delta = now - self.mp_sync_time

        if force_sync or now - self.mp_sync_time > cfg.SYNC_INTERVAL:
            self.sync()

        elif not self.mp.is_paused:
            self.time = self.mp_time_at_sync + self.mp.speed * time_delta
            self.emit(SIGNAL('time_changed'))
            
        for event in self.key_to_open_event.values():
            event.end = self.frame
            self.emit(SIGNAL('updated_event'), event)


    def sync(self):
        """Sync up our time keeping with the actual time in the media player.

        We also use this to measure what the real speed is.

        """
        new_time = self.mp.time
        delta = new_time - self.time

        self.mp_time_at_sync = self.time = new_time
        self.mp_sync_time    = time.time()

        if delta:
            self.emit(SIGNAL('time_changed'), delta)
        self.emit(SIGNAL('synced'), delta)
        
    def keyPressEvent(self, event):
        key = event.key()
        self.pressed_keys.add(key)
        
        if key in self.key_to_track and key not in self.key_to_open_event:
            track = self.key_to_track[key]
            self.sync()
            frame = self.frame
            event = Event(frame, frame)
            track.add_event(event)
            self.key_to_open_event[key] = event
            self.emit(SIGNAL('new_event'), track, event)
            

    def keyReleaseEvent(self, event):
        
        key = event.key()
        if not (key in self.key_to_track and Qt.Key_Shift in self.pressed_keys):
            self.pressed_keys.remove(key)
            event = self.key_to_open_event.pop(key, None)
            if event is not None:
                self.sync()
                event.end = self.frame
                self.emit(SIGNAL('updated_event'), event)
            
        print 'still..:', self.pressed_keys


