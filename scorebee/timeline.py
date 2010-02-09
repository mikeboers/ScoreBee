
import time
from fractions import Fraction
import random
import logging

from .qt import *
from .util import time_to_frame, frame_to_time

class UIData(object):
    pass


# TODO: calculate this for more platforms. can be done with:
#       QScrollBar(Qt.Horizontal).sizeHint().height()
SCROLLBAR_WIDTH = 15

RULER_HEIGHT = 25
TRACK_HEIGHT = 24


log = logging.getLogger(__name__)


class TrackUI(QWidget):
    
    def __init__(self, timeline, track, parent):
        QWidget.__init__(self, parent)
        self.timeline = timeline
        self.track = track
        
        self.setStyleSheet('background-color:rgb(%d, %d, %d)' % tuple(random.randrange(200, 256) for i in range(3)))
        self.data = QWidget(self)
        
        self.header = QLabel(self)
        self.header.setText('%s %s[%s]' % (track.name, '(%s) ' % track.group if track.group else '', track.key.upper()))
        self.header.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.header.setMargin(8)
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(12)
        font.setBold(True)
        self.header.setFont(font)
    
    def layout(self):
        
        width = self.timeline.size().width()
        header_width = self.timeline.header_width
        h_offset = self.timeline.h_scrollbar.value()
        
        self.resize(width, TRACK_HEIGHT)
        self.header.setGeometry(0, 0, header_width, TRACK_HEIGHT)
        self.data.setGeometry(header_width, 0, width, TRACK_HEIGHT)
        
        for event in self.track.events:
            if event.ui is None:
                self.timeline.handle_event_created_signal(self.track, event)
            event.ui.layout()
    
    def mousePressEvent(self, event):
        print 'track', event


class EventUI(QWidget):
    
    def __init__(self, timeline, track, event, parent):
        QWidget.__init__(self, parent)
        self.timeline = timeline
        self.track = track
        self.event = event
        
        self.pen_color = QColor(*tuple(random.randrange(128) for x in range(3)))
    
    def layout(self):
        x = self.timeline.apply_zoom(self.event.start - self.timeline.h_scrollbar.value())
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
            p.drawLine(8 + width + 1, TRACK_HEIGHT/2 - 4, 8 + width + 1, TRACK_HEIGHT/2 + 4)
            
            pen.setWidth(2)
            p.setPen(pen)
            p.drawEllipse(QPoint(8, TRACK_HEIGHT/2), 5, 5)
        
        finally:
            p.end()
    
    def mousePressEvent(self, event):
        if int(event.modifiers()) & Qt.AltModifier:
            self.timeline.app.delete_event(self.track, self.event)
        


class TimelineWindow(QtGui.QMainWindow):

    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        self.app = app
        
        # At zoom level 0, 1 frame will take up 1 pixel.
        self.zoom_level = 0
        
        self.build_base_gui()
        
        # Need to track if a click was registered in the ruler or not, cause
        # I was not able to get the mouse events working on the ruler itslef.
        # Ie. I hacked it together.
        self.clicked_in_ruler = False
        
        connect(self.app, SIGNAL('doc_changed'), self.layout)
        
        connect(self.app, SIGNAL('time_changed'), self.handle_time_change_event)
        connect(self.app, SIGNAL('time_mode_changed'), self.handle_time_mode_change_event)
        
        connect(self.app, SIGNAL('event_created'), self.handle_event_created_signal)
        connect(self.app, SIGNAL('event_updated'), self.handle_event_updated_signal)
        
        connect(self.app, SIGNAL('track_created'), self.handle_track_created_signal)
        
    
    @property
    def zoom_factor(self):
        return Fraction(2, 1) ** self.zoom_level
    
    def zoom_in(self, event=None):
        """Everything gets twice as big."""
        self.zoom_level = min(4, self.zoom_level - 1)
        self.layout()
    
    def zoom_out(self, event=None):
        """Everything gets half as big."""
        self.zoom_level = max(-4, self.zoom_level + 1)
        self.layout()
        
    def apply_zoom(self, value):
        """Get the a zoomed value.
        
        Converts a duration in frames to the number of pixels wide they must
        be drawn.
        
        """
        return float(value * Fraction(2, 1) ** self.zoom_level)
    
    def unapply_zoom(self, value):
        """Convert a zoomed value back to normal.
        
        Converts a pixel width on the screen to the duration in frames it
        represents.
        
        """
        return float(value / Fraction(2, 1) ** self.zoom_level)
    
    
    def frame_to_position(self, frame):
        """Get the x-coord for a given frame.
        
        This returns the x coord relative to the track container.
        
        """
        return int(self.apply_zoom(frame) - self.h_scrollbar.value())
    
    def position_to_frame(self, x):
        """Get the frame that is at a given x-coord.
        
        This takes the x coord relative to the track container.
        
        """
        return int(self.unapply_zoom(x + self.h_scrollbar.value()))
    
    def time_to_position(self, time):
        return self.frame_to_position(time * self.app.video.fps)
    
    def position_to_time(self, x):
        return self.position_to_frame(x) / self.app.video.fps
    
    def build_base_gui(self):
          
        self.resize(600, 300)
        
        # Remove the stupid status bar. This may need to go back for other
        # platforms.
        self.setStatusBar(None)
        
        # Initial constants for the header. These should be updated depending
        # on the data that gets preresented (ie. the width of the text).
        self.header_width = 250
        self.header_min_width = 100
        self.header_max_width = 400
    
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
        
        self.ruler = QWidget(self)
        self.ruler.paintEvent = self.ruler_paintEvent
        self.ruler.mousePressEvent = self.ruler_mousePressEvent
        self.ruler.mouseMoveEvent  = self.ruler_mouseMoveEvent
        self.ruler.mouseReleaseEvent  = self.ruler_mouseReleaseEvent
    
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
        
        self.playhead = QWidget(self)
        self.playhead.paintEvent = self.playhead_paintEvent
        
        self.header_line = QtGui.QFrame(self)
        self.header_line.setFrameShape(QFrame.VLine)
        self.header_line.setFrameShadow(QFrame.Sunken)
        self.header_line.setLineWidth(2)
        self.header_line.setCursor(Qt.SizeHorCursor)
        self.header_line.mousePressEvent = lambda e: None # Trick it into giving us the drag.
        self.header_line.mouseMoveEvent = self.header_line_mouseMoveEvent
        
        self.layout()
        
    def resizeEvent(self, event):
        self.layout()
    
    def layout(self, event=None):
        
        # Some convenient sizes.
        width = self.size().width()
        height = self.size().height()
        header_width = self.header_width # Header width
        tracks_width = width - header_width - SCROLLBAR_WIDTH # Track width
        tracks_height = height - RULER_HEIGHT - SCROLLBAR_WIDTH
        h_offset = self.h_scrollbar.value()
        v_offset = self.v_scrollbar.value()
        
        # Dimensions of the data we have.
        data_height = TRACK_HEIGHT * len(self.app.doc.tracks)
        data_width = 0
        if self.app.is_ready:
            data_width = self.app.video.frame_count
        for track in self.app.doc.tracks:
            if track.events:
                data_width = max(data_width, track.events[-1].end)
        data_width = self.apply_zoom(data_width)
        # log.debug('data_width %d' % data_width)
    
        self.setMinimumSize(self.header_width + 200, 100)
    
        self.track_container.setGeometry(0, RULER_HEIGHT, self.header_width + data_width, data_height)
        
        # Adjust the time display and the ruler container width.
        self.time.setGeometry(0, 0, header_width, RULER_HEIGHT)
        self.ruler.setGeometry(header_width, 0, tracks_width, RULER_HEIGHT)
        self.ruler.repaint()
        
        self.header_line.setGeometry(self.header_width - 2, -2, 4, height + 4)
        self.ruler_line .setGeometry(0, RULER_HEIGHT - 2, width, 4)
        # Scroll bars should be along the bottom and the right side.
        self.h_scrollbar.setGeometry(self.header_width, height-SCROLLBAR_WIDTH, width - self.header_width - SCROLLBAR_WIDTH, SCROLLBAR_WIDTH)
        self.v_scrollbar.setGeometry(width-SCROLLBAR_WIDTH, RULER_HEIGHT, SCROLLBAR_WIDTH, height - SCROLLBAR_WIDTH - RULER_HEIGHT)
        
        # Update the scrollbar maximums and step sizes to go along widthith the
        # new size and data that widthe have.
        self.h_scrollbar.setMaximum(data_width - tracks_width if data_width > tracks_width else 0)
        self.h_scrollbar.setPageStep(tracks_width)
        self.v_scrollbar.setMaximum(data_height - tracks_height if data_height > tracks_height else 0)
        if self.app.video:
            self.h_scrollbar.setSingleStep(self.app.video.fps * self.zoom_factor)
            self.v_scrollbar.setPageStep(self.app.video.fps * self.zoom_factor)
        
        # Track headers and data
        if self.app.doc is not None:
            for i, track in enumerate(self.app.doc.tracks):
                if track.ui is None:
                    self.handle_track_created_signal(track)
                track.ui.move(0, i * TRACK_HEIGHT - self.v_scrollbar.value())
                track.ui.layout()
        
        self.playhead_layout()
    
    def handle_event_created_signal(self, track, event):
        event.ui = EventUI(self, track, event, track.ui.data)
        event.ui.layout()
        event.ui.show()
    
    def handle_event_updated_signal(self, event):
        event.ui.layout()
        
    def handle_track_created_signal(self, track):
        track.ui = TrackUI(self, track, self.track_container)
        track.ui.layout()
        track.ui.show()

    def header_line_mouseMoveEvent(self, event):
        self.header_width = min(self.header_max_width, max(self.header_min_width, self.header_line.pos().x() + event.x()))
        self.layout()
    
    def handle_time_change_event(self):
        self.time.setText(self.app.format_time())
        self.playhead_layout()
        self.ruler.repaint()
        
    def handle_time_mode_change_event(self):
        self.time.setText(self.app.format_time())
        self.ruler.repaint()
    
    def ruler_paintEvent(self, event):
        
        font = QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        
        label_width = QFontMetrics(font).width('00:00:00')
        size_needed = label_width + 10
        
        # Pick an appropriate spacing.
        fps = self.app.video.fps
        frame_sizes = (1, 2) + tuple(fps / x for x in (2, 4, 5, 8, 10)) + tuple(fps * x for x in (1, 2, 4, 5, 10, 15, 20, 30, 60, 5 * 60, 10 * 60))
        frame_sizes = sorted(set(frame_sizes))
        frame_sizes = (int(x) for x in frame_sizes if int(x) == x)
        zoom_sizes = ((x, int(self.apply_zoom(x))) for x in frame_sizes)
        for step, size in zoom_sizes:
            if size > size_needed:
                break
        
        # Figure out how many sub ticks to make.
        ticks = 1
        while ticks < 4 and not step % ticks:
            ticks *= 2
        
        # TODO: This does not use the zoom.
        FPS = int(self.app.video.fps)
        offset = self.h_scrollbar.value()
        x = event.rect().x()
        w = event.rect().width()
        
        min_f = int(self.unapply_zoom(x + offset))
        min_f = min_f / step * step
        max_f = int(self.unapply_zoom(x + offset + w)) + 10
        
        
        p = QtGui.QPainter(self.ruler)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            
            p.setFont(font)
            
            for f in xrange(min_f, max_f, step / ticks):
                tick = (f % step) / (step / ticks)
                x = int(self.apply_zoom(f)) - offset
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
    
    def ruler_mousePressEvent(self, event, offset=0):
        print 'ruler', event
        self.was_playing = self.app.video.is_playing
        if self.was_playing:
            self.app.video.pause()
        self.ruler_mouseMoveEvent(event, offset)
    
    def ruler_mouseMoveEvent(self, event, offset=0):
        # print 'move'
        f = self.unapply_zoom(event.pos().x() + self.h_scrollbar.value() - offset)
        t = frame_to_time(f, self.app.video.fps)
        t = max(0, t)
        if t < self.app.video.length:
            self.app.time = self.app.video.time = t
            self.app.sync() # HUGE HACK!
    
    def mousePressEvent(self, event):
        self.ruler_mousePressEvent(event, self.header_width)
    def mouseMoveEvent(self, event):
        self.ruler_mouseMoveEvent(event, self.header_width)
    
    def ruler_mouseReleaseEvent(self, event):
        # print 'release'
        if self.was_playing:
            self.app.video.play()
    
        
    def playhead_layout(self):
        if not self.app.is_ready:
            self.playhead.hide()
        else:     
            x = self.time_to_position(self.app.time)
            if x < 0:
                self.playhead.hide()
            else:
                self.playhead.setGeometry(self.header_width + x - 8, 0, 8*2 + 1, self.size().height() - SCROLLBAR_WIDTH)
                self.playhead.show()
    
    def playhead_paintEvent(self, event):            
        p = QtGui.QPainter(self.playhead)
        try:
            p.setRenderHint(QtGui.QPainter.Antialiasing)
            left = self.playhead.pos().x() - self.header_width
            p.setClipRect(-left, 0, left + 17, self.size().height())
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
    
    def wheelEvent(self, event):
        if event.orientation() == Qt.Horizontal:
            self.h_scrollbar.setValue(self.h_scrollbar.value() - event.delta())
        else:
            self.v_scrollbar.setValue(self.v_scrollbar.value() - event.delta())
            
  