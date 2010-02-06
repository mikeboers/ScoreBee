
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
