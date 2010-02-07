
import time
from fractions import Fraction
import random

from .qt import *
from .ui.timeline_window import Ui_timeline_window


class UIData(object):
    pass


# TODO: calculate this for more platforms. can be done with:
#       QScrollBar(Qt.Horizontal).sizeHint().height()
SCROLLBAR_WIDTH = 15

RULER_HEIGHT = 25
TRACK_HEIGHT = 32

class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, app):
        
    
        QtGui.QMainWindow.__init__(self)
        self.app = app
        
        self.tracks = []
        
        self.zoom_level = 0
        self.build_base_gui()
        
        self.clicked_in_ruler = False
    
    def zoom(self, v):
        return int(v * Fraction(2, 1) ** self.zoom_level)
    
    def unzoom(self, v):
        return float(float(v) / Fraction(2, 1) ** self.zoom_level)
    
    def build_base_gui(self):
          
        
        # Remove the stupid status bar. This may need to go back for other
        # platforms.
        self.setStatusBar(None)
        
        # Initial constants for the header. These should be updated depending
        # on the data that gets preresented (ie. the width of the text).
        self.header_width = 200
        self.header_min_width = 100
        self.header_max_width = 300
    
        self.track_container = QWidget(self)
        self.track_container.setStyleSheet('background-color:rgb(255, 255, 200)')
        
        self.time = QLineEdit(self)
        self.time.setText('31:41:59')
        self.time.setAlignment(Qt.AlignRight)
        self.time.setReadOnly(True)
        self.time.setFrame(False)
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        self.time.setFont(font)
        
        self.ruler_container = QWidget(self)
        # self.header_line.setFrameShape(QFrame.VLine)
        # self.header_line.setFrameShadow(QFrame.Sunken)
        self.ruler_container.setStyleSheet('background-color:rgb(255, 138, 0)')
        self.ruler = QWidget(self.ruler_container)
        self.ruler.paintEvent = self.ruler_paintEvent
    
        self.v_scrollbar = QScrollBar(Qt.Vertical, self)
        self.v_scrollbar.setMaximum(0) # Disable it.
        connect(self.v_scrollbar, SIGNAL('valueChanged(int)'), self.layout)
        self.h_scrollbar = QScrollBar(Qt.Horizontal, self)
        self.h_scrollbar.setMaximum(0) # Disable it.
        connect(self.h_scrollbar, SIGNAL('valueChanged(int)'), self.layout)
        
        self.ruler_line = QFrame(self)
        self.ruler_line.setFrameShape(QFrame.HLine)
        self.ruler_line.setFrameShadow(QFrame.Sunken)
        self.ruler_line.setLineWidth(2)
        
        self.playhead_container = QWidget(self)
        self.playhead = QWidget(self.playhead_container)
        self.playhead.paintEvent = self.playhead_paintEvent
        
        self.header_line = QtGui.QFrame(self)
        self.header_line.setFrameShape(QFrame.VLine)
        self.header_line.setFrameShadow(QFrame.Sunken)
        self.header_line.setLineWidth(2)
        self.header_line.setCursor(Qt.SizeHorCursor)
        self.header_line.mousePressEvent = lambda e: None # Trick it into giving us the drag.
        self.header_line.mouseMoveEvent = self.header_line_mouseMoveEvent
        
        
        self.resize(600, 300)
        
    @property
    def doc(self):
        return self.app.doc
    
    @property
    def mp(self):
        return self.app.doc.mp
    
    def doc_changed(self):
        # TODO: detroy the old tracks
        self.tracks = list(self.app.doc)
        for i, track in enumerate(self.tracks):
            
            track.ui = ui = UIData() # This is just a generic object.
            ui.container = QWidget(self.track_container)
            ui.container.setStyleSheet('background-color:rgb(%d, %d, %d)' % tuple(random.randrange(200, 256) for i in range(3)))
            ui.header = QLineEdit(ui.container)
            ui.data = QWidget(ui.container)
            
            ui.header.setText('%s (%s)' % (track.name, track.key.upper()))
            ui.header.setAlignment(Qt.AlignRight)
            ui.header.setReadOnly(True)
            ui.header.setFrame(False)
            font = QFont()
            font.setFamily("Courier New")
            font.setPointSize(12)
            font.setBold(True)
            ui.header.setFont(font)
        
        self.layout()
        
        for track in self.tracks:
            track.ui.container.show()
    
    def resizeEvent(self, event):
        self.layout()
    
    def time_changed(self):
        self.playhead_layout()
    
    def layout(self, event=None):
        
        # Some convenient sizes.
        w = self.size().width()
        h = self.size().height()
        hw = self.header_width # Header width
        tw = w - hw - SCROLLBAR_WIDTH # Track width
        th = h - RULER_HEIGHT - SCROLLBAR_WIDTH
        h_offset = self.h_scrollbar.value()
        v_offset = self.v_scrollbar.value()
        
        # Data height/width.
        if self.app.doc:
            dh = TRACK_HEIGHT * len(self.app.doc)
            dw = self.zoom(self.app.doc.mp.frame_count)
        else:
            dh = dw = 0
    
        self.setMinimumSize(self.header_width + 200, 100)
    
        
        self.track_container.setGeometry(0, RULER_HEIGHT, w, dh)
        
        # Adjust the time display and the ruler container width.
        self.time.setGeometry(0, 0, hw, RULER_HEIGHT)
        self.ruler_container.setGeometry(hw, 0, tw, RULER_HEIGHT)
        self.ruler.setGeometry(-h_offset, 0, dw, RULER_HEIGHT) # This only need happen once.
        
        self.header_line.setGeometry(self.header_width - 2, -2, 4, h + 4)
        self.ruler_line .setGeometry(0, RULER_HEIGHT - 2, w, 4)
        # Scroll bars should be along the bottom and the right side.
        self.h_scrollbar.setGeometry(self.header_width, h-SCROLLBAR_WIDTH, w - self.header_width - SCROLLBAR_WIDTH, SCROLLBAR_WIDTH)
        self.v_scrollbar.setGeometry(w-SCROLLBAR_WIDTH, RULER_HEIGHT, SCROLLBAR_WIDTH, h - SCROLLBAR_WIDTH - RULER_HEIGHT)
        
        # Update the scrollbar maximums and step sizes to go along with the
        # new size and data that we have.
        self.h_scrollbar.setMaximum(dw - tw if dw > tw else 0)
        self.h_scrollbar.setPageStep(tw)
        self.v_scrollbar.setMaximum(dh - th if dh > th else 0)
        self.v_scrollbar.setPageStep(th)
        
        # Track headers
        for i, track in enumerate(self.tracks):
            track.ui.container.setGeometry(0, i * TRACK_HEIGHT, w, TRACK_HEIGHT)
            track.ui.header.setGeometry(0, 0, hw, TRACK_HEIGHT)
            track.ui.data.setGeometry(hw, 0, tw, TRACK_HEIGHT)
        
        self.playhead_layout()
    


    def header_line_mouseMoveEvent(self, event):
        self.header_width = min(self.header_max_width, max(self.header_min_width, self.header_line.pos().x() + event.x()))
        self.layout()
    
    def ruler_paintEvent(self, event):
        
        # TODO: This does not use the zoom.
        FPS = int(self.app.doc.mp.fps)
        STEP = FPS
        x = event.rect().x()
        w = event.rect().width()
        
        min_t = x / STEP / 2 * 2 - 2
        min_x = min_t * STEP
        
        steps = w / STEP + 6
        
        p = QtGui.QPainter(self.ruler)
        
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            
            font = QFont()
            font.setFamily("Courier New")
            font.setPointSize(12)
            p.setFont(font)
            
            for i in xrange(steps):
                x = min_x + STEP * i
                if i % 2:
                    p.drawLine(x, RULER_HEIGHT/2, x, RULER_HEIGHT)
                else:    
                    p.drawLine(x, 4, x, RULER_HEIGHT)
                    p.setPen(QColor(0))
                    txt = str(min_t + i)
                    p.drawText(QPoint(x + 2, 12), txt)
        finally:
            p.end
    
    def mousePressEvent(self, event):
        # This is a hack. This should be on the ruler... not here.
        x = event.pos().x()
        y = event.pos().y()
        
        self.clicked_in_ruler = x > self.header_width and y < RULER_HEIGHT
        
        if self.clicked_in_ruler:
            self.was_playing = not self.app.doc.mp.is_paused
            if self.was_playing:
                self.app.doc.mp.pause()
            self.ruler_mouseMoveEvent(event)
    
    def mouseMoveEvent(self, event):
        x = event.pos().x()
        if x > self.header_width:
            self.ruler_mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):        
        if self.clicked_in_ruler and self.was_playing:
            self.app.doc.mp.play()
    
    def ruler_mouseMoveEvent(self, event):
        # We only need to suptrack the header width cause this is not directly
        # recieving the mouse event.
        f = event.pos().x() - self.header_width + self.h_scrollbar.value()
        f = self.unzoom(f)
        t = f / self.app.doc.mp.fps
        self.app.time = self.app.doc.mp.time = t
        self.app.idleEvent(None) # HUGE HACK!
    
        
    def playhead_layout(self):
        if self.app.doc is not None:
            # self.playhead.setStyleSheet('background-color:red')
            frame = int(self.app.time * self.app.doc.mp.fps)
            
            x = self.zoom(frame - self.h_scrollbar.value())
            
            self.playhead_container.setGeometry(
                self.header_width,
                0,
                self.size().width() - self.header_width - SCROLLBAR_WIDTH,
                self.size().height() - SCROLLBAR_WIDTH
            )
            self.playhead.setGeometry(x - 8, 0, 8*2 + 1, self.size().height())
    
    def playhead_paintEvent(self, event):
        p = QtGui.QPainter(self.playhead)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            p.setPen(QColor(128, 0, 0))
            p.setBrush(QColor(128, 0, 0, 128))
            
            p.drawPolygon(
                QPoint(0, 15),
                QPoint(8*2+1, 15),
                QPoint(8, RULER_HEIGHT - 2)            
            )
            p.drawLine(8, RULER_HEIGHT - 1, 8, self.size().height())
            
        finally:
            p.end

# 
# class TimelineWindow(QtGui.QMainWindow):
# 
#     def __init__(self, app, *args):
#         QtGui.QMainWindow.__init__(self, *args)
#         self.app = app
#         
#         self.ui = Ui_timeline_window()
#         self.ui.setupUi(self)
#         
#         # Kill the status bar.
#         self.setStatusBar(None)
#         
#         self.ui.canvas.paintEvent = self.canvas_paintEvent
#         connect(self.ui.scrollbar, SIGNAL('valueChanged(int)'), self.scrolled)
#     
#     def set_canvas_height(self, height):    
#         self.ui.canvas.setMinimumSize(0, height)
#     
#     @property
#     def mp(self):
#         return self.app.doc.mp
#     
#     def doc_changed(self):    
#         height = RULER_HEIGHT + TRACK_HEIGHT * len(self.app.doc)
#         self.set_canvas_height(height)
#         self.ui.scrollbar.setMinimum(0)
#         self.ui.scrollbar.setMaximum(self.mp.frame_count)
#         self.ui.scrollbar.setPageStep(self.size().width())
#     
#     def scrolled(self, value):
#         self.ui.canvas.repaint()
#         
#     def canvas_paintEvent(self, event):
#         
#         if not self.app.doc:
#             return
#         
#         start_time = time.time()
#         
#         width, height = self.size()
#         track_width = width - HEADER_WIDTH
#         
#         p = QtGui.QPainter(self.ui.canvas)
#         try:
#             p.setRenderHint(QtGui.QPainter.Antialiasing)
#             
#             # The header line.
#             p.drawLine(HEADER_WIDTH, 0, HEADER_WIDTH, height)
#             
#             fps = int(self.mp.fps)
#             frame = int(self.app.time * fps)
#             frame_scroll_offset = self.ui.scrollbar.value()
#             
#             # The play head.
#             head_pos = HEADER_WIDTH + frame - frame_scroll_offset
#             if frame + 1 > frame_scroll_offset: # It is visible 
#                 p.setPen(QColor(128, 0, 0, 200))
#                 p.setBrush(QColor(128, 0, 0, 100))
#                 p.drawPolygon(
#                     QPoint(head_pos, RULER_HEIGHT),
#                     QPoint(head_pos - 7, 0),
#                     QPoint(head_pos + 7, 0)
#                 )
#                 p.drawLine(head_pos, RULER_HEIGHT, head_pos, height)
#             
#             # The ruler...
#             p.setPen(QColor(0))
#             p.drawLine(0, RULER_HEIGHT, width, RULER_HEIGHT)
#             start_frame = frame_scroll_offset
#             end_frame = start_frame + width
#             for i in xrange((start_frame + fps) / fps * fps, end_frame, fps):
#                 x = HEADER_WIDTH + i - frame_scroll_offset
#                 s = i / fps
#                 if not s % 2:
#                     p.setPen(QColor(0))
#                     txt = str(s)
#                     txt_width = p.fontMetrics().width(txt)
#                     p.drawText(QPoint(x - txt_width/2, RULER_HEIGHT - 4), str(s))
#                 p.setPen(QColor(200,200,200))
#                 p.drawLine(x, 0, x, RULER_HEIGHT - 6)
#             
#             # The tracks themselves
#             for track_i, track in enumerate(self.app.doc):
#                 print track.name
#                 y_offset = RULER_HEIGHT + track_i * TRACK_HEIGHT
#                 
#                 # The bottom border.
#                 p.setPen(QColor(100, 100, 100))
#                 p.drawLine(0, y_offset + TRACK_HEIGHT, self.size().width(), y_offset + TRACK_HEIGHT)
#                 
#                 # The name and key
#                 p.setPen(QColor(0))
#                 p.drawText(10, y_offset + TRACK_HEIGHT - 6, "%s (%s)" % (track.name, track.key))
#                 
#                 # The data
#                 for event in track:
#                     if event.end < frame_scroll_offset:
#                         continue
#                     if event.start > width + frame_scroll_offset:
#                         break
#                     p.drawLine(
#                         HEADER_WIDTH + event.start - frame_scroll_offset,
#                         y_offset + TRACK_HEIGHT/2,
#                         HEADER_WIDTH + event.end - frame_scroll_offset,
#                         y_offset + TRACK_HEIGHT/2
#                     )
#                     p.drawEllipse(QPoint(
#                             HEADER_WIDTH + event.start - frame_scroll_offset,
#                             y_offset + TRACK_HEIGHT/2),
#                         6, 6
#                     )
#             
#         finally:
#             p.end()
#         
#         print 'painted in %.3fms' % (1000 * (time.time() - start_time))
#         