
import sys
import json
import os
import logging
import time

from scorebee.qt import *

from scorebee.timeline_window import TimelineWindow
from scorebee.status_window import StatusWindow
from scorebee.info_window import InfoWindow
from scorebee.data import Document, Track, Event


log = logging.getLogger(__name__)


WINDOW_NAMES = 'status', 'info', 'timeline'

SYNC_INTERVAL = 0.5

TIME_MODE_SECONDS = 'seconds'
TIME_MODE_FRAMES = 'frames'
time_mode_next = {
    TIME_MODE_SECONDS: TIME_MODE_FRAMES,
    TIME_MODE_FRAMES: TIME_MODE_SECONDS
}

class App(object):
    
    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        
        self.timeline = TimelineWindow()
        self.status = StatusWindow(self, self.timeline)
        self.info = InfoWindow(self.timeline)

        self.doc = None
        
        data = [
            ('General Info', [
                ('fruit', 'apple'),
                ('key', 'a long value; ' * 5),
                ('sync', '<span style="color:red">RESYNCING...</span>'),
                ('sync', '<span style="color:orange">TESTING...</span>'),
                ('sync', '<span style="color:green">OK</span>'),
            ]),
            ('General Info', [
                ('fruit', 'apple'),
                ('key', 'a long value; ' * 5),
                ('red', '<span style="color:red">ARRGHHH</span>'),
            ])
        ]
        self.info.update(data)
        
        self.setup_menu()
        
        
        self.idle_timer = QTimer()
        self.idle_timer.setInterval(10)
        self.idle_timer.timerEvent = self.idleEvent
        self.last_idle = 0
        self.last_sync = 0
        self.sync_offset = 0
        self.needs_sync = True
        
        # This will be updated by the status window.
        self.speed = 1
        self.time = 0
        self.time_mode = TIME_MODE_FRAMES
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = value
    
    def idleEvent(self, event):
        this_time = time.time()
        time_delta = this_time - self.last_idle
        self.last_idle = this_time
        
        if this_time - self.last_sync > SYNC_INTERVAL:
            self.needs_sync = True
        
        if not self.doc.mp.is_paused:
            self.time += self.speed * time_delta
            if self.needs_sync:
                
                # SYNC!
                new_time = self.doc.mp.time
                self.sync_offset = new_time - self.time
                self.status.ui.sync.setText('sync: %5.1fms' % abs(1000 * self.sync_offset))
                self.time = new_time
                
                self.needs_sync = False
                self.last_sync = this_time
        
        self.status.ui.time.setText('%.3fs' % self.time)
        self.status.ui.speed.setText('speed: %sx' % self.doc.mp.speed)
    
    def setup_menu(self):
        
        video = QtGui.QAction(QtGui.QIcon('ui/silk/accept.png'), 'Open Video', self.timeline)
        data = QtGui.QAction(QtGui.QIcon('icons/data.png'), 'Choose Datafile', self.timeline)
        # exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self.timeline)
        #self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        #self.connect(video, QtCore.SIGNAL('triggered()'), self.videodialog)
        #self.connect(data, QtCore.SIGNAL('triggered()'), self.datadialog)
        menubar = self.timeline.menuBar()
        file = menubar.addMenu("&File")
        help = menubar.addMenu("Help")
        file.addAction(video)
        file.addAction(data)
        # file.addAction(exit)
        
        window_menu = menubar.addMenu("Window")
        def make_handler(name):
            def handler():
                window = getattr(self, name)
                window.show()
                window.raise_()
            return handler
        for name in WINDOW_NAMES:
            action = QtGui.QAction(name.capitalize(), self.timeline)
            connect(action, SIGNAL('triggered()'), make_handler(name))
            window_menu.addAction(action)
                
        #Help menu
        # about = QtGui.QAction(QtGui.QIcon('icons/about.png'), 'About CowLog', self.timeline)
        #self.connect(about, QtCore.SIGNAL('triggered()'), self.aboutAction)
        # manual = QtGui.QAction(QtGui.QIcon('icons/help.png'), 'CowLog Help', self.timeline)
        #self.connect(manual, QtCore.SIGNAL('triggered()'), self.helpAction)
        # help.addAction(manual)
        # help.addAction(about)
    
        
    def run(self):
        
        if os.path.exists('settings/windows.json'):
            window_prefs = json.load(open('settings/windows.json'))
            for name, data in window_prefs.iteritems():
                window = getattr(self, name)
                window.move(*data['pos'])
                window.resize(*data['size'])
            
        self.status.show()
        self.info.show()
        self.timeline.show()
        
        
        
        
        # This is just a hack for now.
        self.doc = Document('/Users/mikeboers/Desktop/example.MOV')
        # self.doc = Document('/Users/mikeboers/Desktop/C00000S00A20091231112932302.avi')
        self.doc.append(Track('A behaviour', 'q', [
            (10, 15), (50, 65)
        ]))
        self.doc.append(Track('Nothin here', 'w', []))
        self.doc.append(Track('Better one', 'e', [
            (25, 26), (70, 71)
        ]))
        # This starts up the player.
        log.debug('%d frames' % self.doc.mp.frame_count)
        
        self.idle_timer.start()
        self.app.exec_()
        
        # HACK: Kill the MPlayer
        self.doc._mp = None
        
        window_prefs = {}
        for name in WINDOW_NAMES:
            window_prefs[name] = dict(
                pos=tuple(getattr(self, name).pos()),
                size=tuple(getattr(self, name).size()),
            )
        json.dump(window_prefs, open('settings/windows.json', 'w'), indent=4)

app = App(sys.argv)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run()
