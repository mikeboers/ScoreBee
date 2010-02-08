
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


WINDOW_NAMES = 'timeline', 'status', 'info'


COMBINE_MODE_REPLACE = 'replace'
COMBINE_MODE_ADD = 'add'


class Application(QObject):
    
    def __init__(self, argv):
        
        QObject.__init__(self)
        
        self.app = QtGui.QApplication(argv)
        
        # The document is accessed through a property because we need to
        # signal rebuilding the api whenever it is changed.
        self._doc = None
        self._video = None
        
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
        self.video_sync_time = 0 # Last time we synced to mplayer's time.
        self.video_time_at_sync = 0 # What the time was when we synced.
        
        # The global time representation mode. Rotate this by calling
        # self.next_time_mode()
        self.time_mode = next_time_mode()
        
        # Some state to keep track of which keys are pressed.
        self.pressed_keys = set()
        self.key_to_track = {}
        self.key_to_open_event = {}
    
    def setup_menu(self):
        menubar = self.timeline.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        new = QAction("New", self.timeline)
        new.setShortcut('Ctrl+N')
        connect(new, SIGNAL('triggered()'), self.handle_file_new)
        file_menu.addAction(new)
        
        open_ = QAction("Open...", self.timeline)
        open_.setShortcut('Ctrl+O')
        connect(open_, SIGNAL('triggered()'), self.handle_file_open)
        file_menu.addAction(open_)
        
        file_menu.addSeparator()
        
        save = QAction("Save", self.timeline)
        save.setShortcut('Ctrl+S')
        connect(save, SIGNAL('triggered()'), self.handle_file_save)
        file_menu.addAction(save)
        
        save_as = QAction("Save As...", self.timeline)
        save_as.setShortcut('Ctrl+Shift+S')
        connect(save_as, SIGNAL('triggered()'), self.handle_file_save_as)
        file_menu.addAction(save_as)
        
        quit = QAction("Quit", self.timeline)
        quit.setShortcut('Ctrl+Q')
        connect(quit, SIGNAL('triggered()'), self.handle_file_quit)
        file_menu.addAction(quit)
        
        edit_menu = menubar.addMenu("Edit")
        
        undo = QAction("Undo", self.timeline)
        undo.setShortcut("Ctrl+Z")
        connect(undo, SIGNAL('triggered()'), self.handle_edit_undo)
        edit_menu.addAction(undo)
        
        view_menu = menubar.addMenu("View")
        
        zoom_in = QAction("Zoom In", self.timeline)
        zoom_in.setShortcut('Ctrl+-')
        connect(zoom_in, SIGNAL('triggered()'), self.timeline.zoom_in)
        view_menu.addAction(zoom_in)
        
        zoom_out = QAction("Zoom Out", self.timeline)
        zoom_out.setShortcut("Ctrl++")
        connect(zoom_out, SIGNAL('triggered()'), self.timeline.zoom_out)
        view_menu.addAction(zoom_out)
        
        window_menu = menubar.addMenu("Window")
        def make_handler(name):
            def handler():
                window = getattr(self, name)
                window.show()
                if name == 'timeline':
                    window.layout()
                else:
                    window.repaint()
                window.raise_()
            return handler
        for i, name in enumerate(WINDOW_NAMES):
            action = QtGui.QAction(name.capitalize(), self.timeline)
            action.setShortcut('Ctrl+%d' % (i + 1))
            connect(action, SIGNAL('triggered()'), make_handler(name))
            window_menu.addAction(action)

    def ask_to_save_if_required(self):
        if self.doc:
            dialog = QMessageBox()
            dialog.setText("The document (has) have been modified.");
            dialog.setInformativeText("Do you want to save your changes?");
            dialog.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel);
            dialog.setDefaultButton(QMessageBox.Save);
            res = dialog.exec_()
            if res == QMessageBox.Cancel:
                raise ValueError('cancel')
            return res == QMessageBox.Save
    
    def handle_file_new(self):
        log.debug('File > New')
        try:
            if self.ask_to_save_if_required():
                self.save()
            doc = Document.from_string(open('template.scorb').read())
            self.doc = doc
        except ValueError:
            pass
    
    def handle_file_open(self):
        log.debug('File > Open')
        try:
            if self.ask_to_save_if_required():
                self.save()
            path = str(QFileDialog.getOpenFileName(self.timeline,
                caption="Pick a file to open.",
                directory="~",
                filter="ScoreBee (*.scorb)",
            ))
            if not path:
                raise ValueError('user cancelled')
            doc = Document.from_string(open(path).read())
            doc.path = path
            
            self.doc = doc
        except ValueError:
            pass
    
    def handle_file_save(self):
        log.debug('File > Save')
        self.save()
    
    def handle_file_save_as(self):
        log.debug('File > Save As')
        self.save(save_as=True)
    
    def handle_file_quit(self):
        log.debug('File > Quit')
        try:
            if self.ask_to_save_if_required():
                self.save()
            self.app.quit()
        except ValueError:
            pass
        
    def handle_edit_undo(self):
        log.debug('Edit > Undo')
        pass    
    
    def save(self, save_as=False):
        if self.doc.path is None or save_as:
            path = str(QFileDialog.getSaveFileName(self.timeline,
                caption="Save File",
                directory='/Users/mikeboers/Desktop',
                filter="ScoreBee (*.scorb)",
            ))
            if not len(path):
                raise ValueError('user canceled')
        else:
            path = self.doc.path
        
        # Make a backup if it already exists:
        if os.path.exists(path):
            backup_dir = os.path.dirname(path) + '/backup'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            backup_path = backup_dir + '/' + time.strftime('%Y-%m-%dT%H-%M-%S') + '.' + os.path.basename(path)
            open(backup_path, 'w').write(open(path, 'r').read())
        
        # Do the saving
        open(path, 'w').write(self.doc.as_string())
        self.doc.path = path
    
    
    @property
    def video(self):
        """Always a good (ie. running) mplayer."""
        if self._video is None or not self._video.is_running:
            if self.doc.is_ready:
                self._video = MPlayer(
                    path=self.doc.video_path,
                    conf=os.path.abspath(__file__ + '/../../settings/mplayer.txt')
                )
        return self._video
    
    def format_time(self, time=None):
        """Format a time with the current time format mode."""
        return format_time(self.time if time is None else time, self.video.fps, self.time_mode)
    
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
        self._video = None # Forces a new mplayer with the new video.
        if doc.is_ready:
            self.video.time = 0
        
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
            
        # Start up the document
        # self.doc = Document()
        
        # Run the main loops.
        self.idle_timer.start()
        try:
            self.app.exec_()
        finally:
            # HACK: Kill the MPlayer
            self._video = None
        
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
        return int(self.time * self.video.fps)
    
    def main_loop(self, event=None, force_sync=False):
        """Event that is triggered every couple milliseconds.

        Treat this as our main loop.

        """
        
        if not self.doc:
            return
        
        now = time.time()
        time_delta = now - self.video_sync_time

        if force_sync or now - self.video_sync_time > cfg.SYNC_INTERVAL:
            self.sync()

        elif not self.video.is_paused:
            self.time = self.video_time_at_sync + self.video.speed * time_delta
            self.emit(SIGNAL('time_changed'))
            
        for event in self.key_to_open_event.values():
            event.end = self.frame
            self.emit(SIGNAL('event_updated'), event)

        
    def sync(self, threshold=1.0/30, verbose=False):
        """Sync up our time keeping with the actual time in the media player.

        We also use this to measure what the real speed is.

        """
        
        start_time = time.time()
        
        if start_time - self.video_sync_time < threshold:
            if verbose:
                log.debug('sync under threshold')
            return
            
        new_time = self.video.time
        delta = new_time - self.time
        
        self.video_time_at_sync = self.time = new_time
        self.video_sync_time    = start_time

        if delta:
            self.emit(SIGNAL('time_changed'), delta)
        self.emit(SIGNAL('synced'), delta)
        
        if verbose:
            log.debug('synced in %.2fms' % (1000 * (time.time() - start_time)))
    
    def toggle_pause(self):
        if self.video.is_paused:
            self.video.play()
        else:
            self.video.pause()
        self.emit(SIGNAL('pause_toggled'))
    
    @property
    def event_redo_mode(self):
        return COMBINE_MODE_REPLACE if Qt.Key_CapsLock in self.pressed_keys else COMBINE_MODE_ADD
        
    def keyPressEvent(self, event):
        key = event.key()
        # log.debug('keyPressEvent %d' % key)
        
        # Track the key press.
        self.pressed_keys.add(key)
        
        if key == Qt.Key_Space:
            self.toggle_pause()
        
        # If this key is a trigger for a track and there isn't already an
        # open event (ie one in progress already), then make a new one.
        elif key in self.key_to_track and key not in self.key_to_open_event:
            track = self.key_to_track[key]
            
            # Make sure we are getting an acurate time here. There may be
            # issues if the sync itself takes some time to complete.
            #
            # We could time how long this takes to complete and then subtract
            # that from the time value we get, but we don't know if the delay
            # is on the front or the back. I'm not going to bother for now.
            self.sync(threshold=1.0/30, verbose=True)
            
            # Create the new event, store it in all the right places, and
            # signal to everyone else that it exists.
            frame = self.frame
            event = Event(frame, frame)
            track.add_event(event)
            self.key_to_open_event[key] = event
            self.emit(SIGNAL('event_created'), track, event)
            

    def keyReleaseEvent(self, event):
        key = event.key()
        # log.debug('keyReleaseEvent %d' % key)
        
        # Ignore the release event if it is a track trigger, and the shift
        # button is held down. This effectively makes the keys sticky. One can
        # cancel it by hitting it normally.
        if not (key in self.key_to_track and Qt.Key_Shift in self.pressed_keys):   
            # Discard doesn't error if the key isn't in there.
            self.pressed_keys.discard(key)
            
            if key in self.key_to_open_event:
                event = self.key_to_open_event.pop(key)
            
                # Make sure we are getting an accurate time. See my note in
                # the keyPressEvent for why this can be wrong.
                self.sync(threshold=1.0/30, verbose=True)
                event.end = self.frame
            
                # Let everyone know...
                self.emit(SIGNAL('event_updated'), event)



