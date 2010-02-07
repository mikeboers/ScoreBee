
import time
from fractions import Fraction

from .qt import *
from .ui.timeline_window import Ui_timeline_window




# TODO: calculate this for more platforms. can be done with:
#       QScrollBar(Qt.Horizontal).sizeHint().height()
SCROLLBAR_WIDTH = 15

RULER_HEIGHT = 25
TRACK_HEIGHT = 32

class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, app):
        
    
        QtGui.QMainWindow.__init__(self)
        self.app = app
        
        self.build_base_gui()
    
    def build_base_gui(self):
          
        
        # Remove the stupid status bar. This may need to go back for other
        # platforms.
        self.setStatusBar(None)
        
        # Initial constants for the header. These should be updated depending
        # on the data that gets preresented (ie. the width of the text).
        self.header_width = 100
        self.header_min_width = 100
        self.header_max_width = 200
    
        self.canvas = QWidget(self)
        self.canvas.setStyleSheet('background-color:rgb(255, 255, 200)')
        
        self.time = QLineEdit(self.canvas)
        self.time.setText('31:41:59')
        self.time.setAlignment(Qt.AlignRight)
        self.time.setReadOnly(True)
        self.time.setFrame(False)
        self.time.setStyleSheet('background-color:rgb(200, 200, 200)')
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.time.setFont(font)
        
        
        self.ruler_container = QWidget(self.canvas)
        self.ruler_container.setStyleSheet('background-color:rgb(255, 138, 0)')
        self.ruler = QWidget(self.ruler_container)
    
        self.v_scrollbar = QScrollBar(Qt.Vertical, self)
        self.v_scrollbar.setMaximum(0) # Disable it.
        self.h_scrollbar = QScrollBar(Qt.Horizontal, self)
        self.h_scrollbar.setMaximum(0) # Disable it.
    
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
        print 'doc changed'
    
    def resizeEvent(self, event):
        self.layout()

    def layout(self):
        w = self.size().width()
        h = self.size().height()
        
        # Track width.
        hw = self.header_width
        tw = w - hw
    
        self.setMinimumSize(self.header_width + 200, 100)
    
        
        self.canvas.         setGeometry(0, 0, w, h)
        
        self.time.setGeometry(0, 0, hw, RULER_HEIGHT)
        self.ruler_container.setGeometry(hw, 0, tw - SCROLLBAR_WIDTH, RULER_HEIGHT)
        self.ruler.          setGeometry(0, 0, 1000, RULER_HEIGHT)
        
        self.header_line.       setGeometry(self.header_width - 2, -2, 4, h + 4)
        self.h_scrollbar.setGeometry(self.header_width, h-SCROLLBAR_WIDTH, w - self.header_width - SCROLLBAR_WIDTH, SCROLLBAR_WIDTH)
        self.v_scrollbar.setGeometry(w-SCROLLBAR_WIDTH, RULER_HEIGHT, SCROLLBAR_WIDTH, h - SCROLLBAR_WIDTH - RULER_HEIGHT)

    def header_line_mouseMoveEvent(self, event):
        self.header_width = min(self.header_max_width, max(self.header_min_width, self.header_line.pos().x() + event.x()))
        self.layout()
    

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