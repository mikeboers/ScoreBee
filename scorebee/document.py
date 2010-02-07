

from bisect import bisect, insort


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
    
    def __lt__(self, other):
        if isinstance(other, Event):
            return self.start < other.start
        return self.start < other
        
    def __gt__(self, other):
        if isinstance(other, Event):
            return self.start > other.start
        return self.start > other
        


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
    
    def add_event(self, event):
        assert isinstance(event, Event)
        insert(self._events, event)
    
    def search_index(self, value):
        return bisect(self._events, value)


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



if __name__ == '__main__':
    import time
    start_time = time.time()
    
    l = []
    insort(l, Event(1))
    insort(l, Event(2))
    insort(l, Event(3))
    insort(l, Event(1.5))
    insort(l, Event(2.5))
    insort(l, Event(4))
    
    print l
    print bisect(l, 1.75)
    print time.time() - start_time