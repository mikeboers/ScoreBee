
from .qt import *


class Event(QObject):
    
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
        
        # This will hold the ui objects.
        self.ui = None
    
    @property
    def length(self):
        return self.end - self.start if self.end is not None else None
    
    def __repr__(self):
        return 'Event(%r, %r)' % (self.start, self.end)


class Track(QObject):
    
    def __init__(self, name, key, events):
        self.name = name
        self.key = key
        self._events = sorted(events) or []
    
    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, v):
        assert isinstance(v, str)
        assert len(v) == 1
        self._key = v.upper()
    
    @property
    def key_code(self):
        return ord(self._key)
    
    def __iter__(self):
        return iter(self._events)


class Document(QObject):
    
    def __init__(self, src, tracks=None):
        self.src = src
        self._tracks = tracks or []
    
    def __iter__(self):
        return iter(self._tracks)
    
    def __len__(self):
        return len(self._tracks)
    
    def add_track(self, track):
        self._tracks.append(track)



