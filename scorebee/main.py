
import sys
import json
import os

from scorebee.qt import *

from scorebee.timeline_window import TimelineWindow
from scorebee.status_window import StatusWindow
from scorebee.info_window import InfoWindow


class App(object):
    
    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        
        self.timeline = TimelineWindow()
        self.status = StatusWindow(self.timeline)
        self.info = InfoWindow(self.timeline)


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
        self.app.exec_()
        
        window_prefs = {}
        for name in 'status', 'info', 'timeline':
            window_prefs[name] = dict(
                pos=tuple(getattr(self, name).pos()),
                size=tuple(getattr(self, name).size()),
            )
        json.dump(window_prefs, open('settings/windows.json', 'w'), indent=4)

app = App(sys.argv)

if __name__ == '__main__':
    app.run()
