

from .mplayer import MPlayer


class Event(list):
    
    def __init__(self, start, end=None):
        list.__init__(self, [start, end])
    
    def __repr__(self):
        return 'Event(%s, %s)' % tuple(self)
    
    @property
    def start(self):
        return self[0]
    
    @start.setter
    def start(self, value):
        self[0] = value
    
    @property
    def end(self):
        return self[1]
    
    @end.setter
    def end(self, value):
        self[1] = value


class Track(list):
    
    def __init__(self, name, key, data=None):
        self.name = name
        self.key = key
        self.key_code = ord(key.upper())
        if data:
            list.__init__(self, data)


class Document(list):
    
    def __init__(self, src, tracks=None):
        self.src = src
        self._mp = None
        if tracks:
            list.__init__(self, tracks)
    
    @property
    def mp(self):
        if self._mp is None or not self._mp.is_running:
            self._mp = MPlayer(self.src)
        return self._mp

