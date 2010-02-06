
import sys

from scorebee.qt import *

from scorebee.status_window import StatusWindow
from scorebee.info_window import InfoWindow


class App(object):
    
    def __init__(self, argv):
        self.app = QtGui.QApplication(argv)
        
        self.status = StatusWindow()
        self.info = InfoWindow(self.status)
        
        textarea = self.info.ui.textarea
        
        text = []
        for header, data in [
            ('General Info', [
                ('fruit', 'apple'),
                ('key', 'a long value; ' * 5),
                ('red', '<span style="color:red">ARRGHHH</span>')
            ]),
            ('General Info', [
                ('fruit', 'apple'),
                ('key', 'a long value; ' * 5),
                ('red', '<span style="color:red">ARRGHHH</span>')
            ])
        ]:    
            text.append('<h3>' + header + '</h3>')
            text.append('<table>')
            for pair in data:
                text.append('<tr><td><b><pre>  %s</pre></b></td><td>:</td><td>%s</td></tr>' % (pair))
            text.append('</table>')
            # text.append('<br />')
        
        textarea.setText(''.join(text))
        
    def run(self):
        self.status.show()
        self.info.show()
        self.app.exec_()

app = App(sys.argv)

if __name__ == '__main__':
    app.run()
