
import collections

from .qt import *
from .ui.info_window import Ui_info_window



class InfoWindow(QtGui.QWidget):

    def __init__(self, app, *args):
        QtGui.QWidget.__init__(self, *args)
        self.app = app
        self.ui = Ui_info_window()
        self.ui.setupUi(self)
        
        # DEV: This is only for development.
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
        
        self.update(data)
    
    def update(self, sets):
        text = []
        for header, data in sets:    
            text.append('<h3>' + header + '</h3>')
            text.append('<table>')
            for pair in data:
                text.append('<tr><td><b><pre>  %s</pre></b></td><td>:</td><td>%s</td></tr>' % (pair))
            text.append('</table>')
            # text.append('<br />')
        
        self.ui.textarea.setText(''.join(text))