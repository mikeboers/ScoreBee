
import time
from fractions import Fraction
import random

from .qt import *
from .util import time_to_frame, frame_to_time

class UIData(object):
    pass


# TODO: calculate this for more platforms. can be done with:
#       QScrollBar(Qt.Horizontal).sizeHint().height()
SCROLLBAR_WIDTH = 15

RULER_HEIGHT = 25
TRACK_HEIGHT = 32


class EventUI(QWidget):
    
    def __init__(self, timeline, event, parent):
        QWidget.__init__(self, parent)
        self.timeline = timeline
        self.event = event
        
        self.pen_color = QColor(*tuple(random.randrange(128) for x in range(3)))
        # self.setStyleSheet('background-color:rgb(%d, %d, %d)' % tuple(random.randrange(128) for x in range(3)))
    
    def layout(self):
        x = self.timeline.apply_zoom(self.event.start)
        width = self.timeline.apply_zoom(self.event.length)
        self.setGeometry(x - 8, 0, width + 15, TRACK_HEIGHT)
    
    
    def paintEvent(self, event):
        
        x = self.timeline.apply_zoom(self.event.start)
        width = self.timeline.apply_zoom(self.event.length)
        
        p = QtGui.QPainter(self)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
        
            pen = QPen()
            pen.setColor(self.pen_color)
            pen.setWidth(3)
            p.setPen(pen)
        
            p.setBrush(self.pen_color.lighter(125))
            
            p.drawLine(8, TRACK_HEIGHT/2, 8 + width, TRACK_HEIGHT/2)
            p.drawLine(8 + width + 1, 12, 8 + width + 1, TRACK_HEIGHT - 12)
            
            pen.setWidth(2)
            p.setPen(pen)
            p.drawEllipse(QPoint(8, TRACK_HEIGHT/2), 5, 5)
        
        finally:
            p.end()
        


class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        self.app = app
        
        self.tracks = []
        
        # At zoom level 0, 1 frame will take up 1 pixel.
        self.zoom_level = 0
        
        self.build_base_gui()
        
        # Need to track if a click was registered in the ruler or not, cause
        # I was not able to get the mouse events working on the ruler itslef.
        # Ie. I hacked it together.
        self.clicked_in_ruler = False
        
        connect(self.app, SIGNAL('time_changed'), self.handle_time_change_event)
        connect(self.app, SIGNAL('time_mode_changed'), self.handle_time_mode_change_event)
        connect(self.app, SIGNAL('doc_changed'), self.handle_doc_changed_event)
        connect(self.app, SIGNAL('new_event'), self.handle_new_event_signal)
        connect(self.app, SIGNAL('updated_event'), self.handle_updated_event_signal)
    
    @property
    def zoom_factor(self):
        return Fraction(2, 1) ** self.zoom_level
    
    def zoom_in(self, event=None):
        self.zoom_level = min(4, self.zoom_level - 1)
        self.layout()
    
    def zoom_out(self, event=None):
        self.zoom_level = max(-4, self.zoom_level + 1)
        self.layout()
        
    def apply_zoom(self, value):
        """Apply the current zoom level to some data."""
        return float(value * Fraction(2, 1) ** self.zoom_level)
    
    def unapply_zoom(self, value):
        return float(value / Fraction(2, 1) ** self.zoom_level)
        
    def frame_to_x(self, frame):
        """Get the x-coord for a given frame."""
        return int(self.apply_zoom(float(frame)) - self.h_scrollbar.value())
    
    def x_to_frame(self, x):
        """Get the frame number of a n x-coord"""
        return int(self.unapply_zoom(float(x) + self.h_scrollbar.value()))
    
    def time_to_x(self, time):
        return self.frame_to_x(time * self.app.mp.fps)
    
    def x_to_time(self, x):
        return self.x_to_frame(x) / self.app.mp.fps
    
    def build_base_gui(self):
          
        self.resize(600, 300)
        
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
        # Force it off the screen until it is layed out.
        self.playhead_container.move(-100, 0)
        
        self.header_line = QtGui.QFrame(self)
        self.header_line.setFrameShape(QFrame.VLine)
        self.header_line.setFrameShadow(QFrame.Sunken)
        self.header_line.setLineWidth(2)
        self.header_line.setCursor(Qt.SizeHorCursor)
        self.header_line.mousePressEvent = lambda e: None # Trick it into giving us the drag.
        self.header_line.mouseMoveEvent = self.header_line_mouseMoveEvent
        
        self.layout()
    
    def handle_doc_changed_event(self):
        
        # TODO: Delete them with deleteLater (or something)
        for track in self.tracks:
            track.ui.container.destroy()
            
        self.tracks = list(self.app.doc)
        
        for i, track in enumerate(self.tracks):
            
            track.ui = ui = UIData() # This is just a generic object.
            ui.container = QWidget(self.track_container)
            ui.container.setStyleSheet('background-color:rgb(%d, %d, %d)' % tuple(random.randrange(200, 256) for i in range(3)))
            ui.header = QLineEdit(ui.container)
            ui.data_container = QWidget(ui.container)
            ui.data = QWidget(ui.data_container)
            
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
            dw = self.apply_zoom(self.app.mp.frame_count)
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
        
        # Track headers and data
        for i, track in enumerate(self.tracks):
            track.ui.container.setGeometry(0, i * TRACK_HEIGHT, w, TRACK_HEIGHT)
            track.ui.header.setGeometry(0, 0, hw, TRACK_HEIGHT)
            track.ui.data_container.setGeometry(hw, 0, tw, TRACK_HEIGHT)
            track.ui.data.setGeometry(-h_offset, 0, dw, TRACK_HEIGHT)
            
            for event in track:
                if event.ui is None:
                    self.handle_new_event_signal(track, event)
                event.ui.layout()
        
        self.playhead_layout()
    
    def handle_new_event_signal(self, track, event):
        event.ui = ui = EventUI(self, event, track.ui.data)
        ui.show()
        ui.layout()
    
    def handle_updated_event_signal(self, event):
        event.ui.layout()

    def header_line_mouseMoveEvent(self, event):
        self.header_width = min(self.header_max_width, max(self.header_min_width, self.header_line.pos().x() + event.x()))
        self.layout()
    
    def handle_time_change_event(self):
        self.time.setText(self.app.format_time())
        self.playhead_layout()
        
    def handle_time_mode_change_event(self):
        self.ruler.repaint()
    
    def ruler_paintEvent(self, event):
        
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        
        label_width = QFontMetrics(font).width('00:00:00')
        size_needed = label_width + 10
        
        # Pick an appropriate spacing.
        fps = self.app.mp.fps
        frame_sizes = (1, 2) + tuple(fps / x for x in (2, 4, 5, 8, 10)) + tuple(fps * x for x in (1, 2, 4, 5, 10, 15, 20, 30, 60, 5 * 60, 10 * 60))
        frame_sizes = sorted(set(frame_sizes))
        frame_sizes = (int(x) for x in frame_sizes if int(x) == x)
        zoom_sizes = ((x, int(self.apply_zoom(x))) for x in frame_sizes)
        for step, size in zoom_sizes:
            if size > size_needed:
                break
        
        # Figure out how many sub ticks to make.
        ticks = 1
        while ticks < 4 and not step % (2 ** ticks):
            ticks += 1
        
        # TODO: This does not use the zoom.
        FPS = int(self.app.mp.fps)
        x = event.rect().x()
        w = event.rect().width()
        
        min_f = int(self.unapply_zoom(x))
        min_f = min_f / step * step
        max_f = int(self.unapply_zoom(x + w)) + 10
        
        p = QtGui.QPainter(self.ruler)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            
            p.setFont(font)
            
            for f in xrange(min_f, max_f, step / ticks):
                tick = (f % step) / (step / ticks)
                x = int(self.apply_zoom(f))
                
                if tick == 0:
                    p.drawLine(x, 4, x, RULER_HEIGHT)
                    p.setPen(QColor(0))
                    txt = self.app.format_time(frame_to_time(f, fps))
                    p.drawText(QPoint(x + 2, 10), txt)
                    
                elif ticks == 2 or ticks == 4 and tick == 2:    
                    p.drawLine(x, RULER_HEIGHT - 8, x, RULER_HEIGHT)
                    
                else:
                    p.drawLine(x, RULER_HEIGHT - 4, x, RULER_HEIGHT)
        finally:
            p.end
    
    def mousePressEvent(self, event):
        # This is a hack. This should be on the ruler... not here.
        x = event.pos().x()
        y = event.pos().y()
        
        self.clicked_in_ruler = x > self.header_width and y < RULER_HEIGHT
        
        if self.clicked_in_ruler:
            self.was_playing = not self.app.mp.is_paused
            if self.was_playing:
                self.app.mp.pause()
            self.ruler_mouseMoveEvent(event)
    
    def mouseMoveEvent(self, event):
        x = event.pos().x()
        if x > self.header_width:
            self.ruler_mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):        
        if self.clicked_in_ruler and self.was_playing:
            self.app.mp.play()
    
    def ruler_mouseMoveEvent(self, event):
        # We only need to suptrack the header width cause this is not directly
        # recieving the mouse event.
        t = self.x_to_time(event.pos().x() - self.header_width)
        if t < self.app.mp.length:
            self.app.time = self.app.mp.time = t
            self.app.sync() # HUGE HACK!
    
        
    def playhead_layout(self):
        if self.app.doc is not None:            
            x = self.time_to_x(self.app.time)
            
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
  