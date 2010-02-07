

class Event(Qobject):
    
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return 'Event(%r, %r)' % (self.start, self.end)


class Track(Qobject):
    
    def __init__(self, name, key, events):
        self.name = name
        self.key = key
        self.events = events or []
    
    @property
    def key(self):
        return self.key
    
    @key.setter
    def key(self, v):
        assert isinstance(v, str)
        assert len(v) == 1
        self._str = v.upper()
    
    @property
    def key_code(self):
        return ord(self._key


class Document(Qobject):
    
    def __init__(self, src, tracks=None):
        self.src = src
        self.tracks = tracks or []

