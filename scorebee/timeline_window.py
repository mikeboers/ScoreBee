
from .qt import *
from .ui.timeline_window import Ui_timeline_window


HEADER_WIDTH = 200
RULER_HEIGHT = 20
TRACK_HEIGHT = 32

class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, app, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.app = app
        
        self.ui = Ui_timeline_window()
        self.ui.setupUi(self)
        
        # Kill the status bar.
        self.setStatusBar(None)
        
        self.ui.canvas.paintEvent = self.canvas_paintEvent
        connect(self.ui.scrollbar, SIGNAL('valueChanged(int)'), self.scrolled)
    
    def set_canvas_height(self, height):    
        self.ui.canvas.setMinimumSize(0, height)
    
    @property
    def mp(self):
        return self.app.doc.mp
    
    def doc_changed(self):    
        height = RULER_HEIGHT + TRACK_HEIGHT * len(self.app.doc)
        self.set_canvas_height(height)
        self.ui.scrollbar.setMinimum(0)
        self.ui.scrollbar.setMaximum(self.mp.frame_count)
        self.ui.scrollbar.setPageStep(self.size().width())
    
    def scrolled(self, value):
        self.ui.canvas.repaint()
        
    def canvas_paintEvent(self, event):
        
        if not self.app.doc:
            return
        
        # Resize myself. This need not be done here.
        
        width, height = self.size()
        track_width = width - HEADER_WIDTH
        
        p = QtGui.QPainter(self.ui.canvas)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            
            # The header line.
            p.drawLine(HEADER_WIDTH, 0, HEADER_WIDTH, height)
            
            fps = self.mp.fps
            frame = int(self.app.time * fps)
            frame_scroll_offset = self.ui.scrollbar.value()
            
            # The play head.
            head_pos = HEADER_WIDTH + frame - frame_scroll_offset
            if frame > frame_scroll_offset: # It is visible 
                p.setPen(QColor(128, 0, 0, 200))
                p.setBrush(QColor(128, 0, 0, 100))
                p.drawPolygon(
                    QPoint(head_pos, RULER_HEIGHT),
                    QPoint(head_pos - 7, 0),
                    QPoint(head_pos + 7, 0)
                )
                p.drawLine(head_pos, RULER_HEIGHT, head_pos, height)
            
            # The ruler...
            p.setPen(QColor(0))
            p.drawLine(0, RULER_HEIGHT, width, RULER_HEIGHT)
            start_frame = frame_scroll_offset
            end_frame = start_frame + width
            for i in xrange((start_frame + fps) / fps * fps, end_frame, fps):
                x = HEADER_WIDTH + i - frame_scroll_offset
                s = i / fps
                if not s % 2:
                    p.setPen(QColor(0))
                    txt = str(s)
                    txt_width = p.fontMetrics().width(txt)
                    p.drawText(QPoint(x - txt_width/2, RULER_HEIGHT - 4), str(s))
                p.setPen(QColor(200,200,200))
                p.drawLine(x, 0, x, RULER_HEIGHT - 6)
            
            # The tracks themselves
            for track_i, track in enumerate(self.app.doc):
                print track.name
                y_offset = RULER_HEIGHT + track_i * TRACK_HEIGHT
                
                # The bottom border.
                p.setPen(QColor(100, 100, 100))
                p.drawLine(0, y_offset + TRACK_HEIGHT, self.size().width(), y_offset + TRACK_HEIGHT)
                
                # The name and key
                p.setPen(QColor(0))
                p.drawText(10, y_offset + TRACK_HEIGHT - 6, "%s (%s)" % (track.name, track.key))
            
        finally:
            p.end()
        
        