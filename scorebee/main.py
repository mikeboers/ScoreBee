
import sys

from scorebee.qt import *

from scorebee.status_window import StatusWindow
from scorebee.info_window import InfoWindow


class App(object):
    
    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        
        self.status = StatusWindow()
        self.info = InfoWindow(self.status)


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
        self.status.show()
        self.info.show()
        self.app.exec_()

app = App(sys.argv)

if __name__ == '__main__':
    app.run()
