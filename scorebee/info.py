
import collections

from .qt import *
from .ui.info_window import Ui_info_window



class InfoWindow(QtGui.QDialog):

    def __init__(self, app, *args):
        QtGui.QDialog.__init__(self, *args)
        self.app = app
        self.ui = Ui_info_window()
        self.ui.setupUi(self)
    
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