

from bisect import bisect, insort
import json

from .qt import *


class Event(QObject):
    
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
        
        # This will hold the ui objects.
        self.ui = None
    
    @property
    def length(self):
        return self.end - self.start if self.end is not None else 0
    
    def __repr__(self):
        return 'Event(%r, %r)' % (self.start, self.end)
    
    def __iter__(self):
        return iter((self.start, self.end))
    
    def __lt__(self, other):
        if isinstance(other, Event):
            return self.start < other.start
        return self.start < other
        
    def __gt__(self, other):
        if isinstance(other, Event):
            return self.start > other.start
        return self.start > other
        


class Track(QObject):
    
    def __init__(self, name, key, group=None, events=None):
        self.name = name
        self.key = key
        self.group = group
        self.ui = None
        self.events = sorted(events or [])
    
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
    
    def add_event(self, event):
        assert isinstance(event, Event)
        insort(self.events, event)
    
    def search_index(self, value):
        return bisect(self.events, value)


class Document(QObject):
    
    def __init__(self, video_path=None, tracks=None):
        self.video_path = video_path
        self.path = None # This is where it was stored. Set by the controller.
        self.tracks = tracks or []
    
    @property
    def is_ready(self):
        return self.video_path is not None
    
    def add_track(self, track):
        self.tracks.append(track)
    
    def as_string(self):
        tracks = []
        for track in self.tracks:
            events = []
            for event in track.events:
                events.append(tuple(event))
            tracks.append(dict(
                name=track.name,
                group=track.group,
                key=track.key,
                events = events
            ))
        data = dict(
            version=1,
            video_path=self.video_path,
            tracks=tracks
        )
        return json.dumps(data, indent=4, sort_keys=True)
    
    @classmethod
    def from_string(cls, raw):
        data = json.loads(raw)
        return getattr(cls, 'from_string_v%s' % data['version'])(data)
    
    @classmethod
    def from_string_v1(cls, data):
        tracks = []
        for raw_track in data['tracks']:
            events = []
            for raw_event in raw_track['events']:
                events.append(Event(*raw_event))
            tracks.append(Track(
                name=raw_track['name'],
                key=str(raw_track['key']),
                group=raw_track['group'],
                events=events
            ))
        return cls(
            video_path=data['video_path'],
            tracks=tracks
        )



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