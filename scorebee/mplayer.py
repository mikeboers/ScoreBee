
from subprocess import Popen, PIPE
from select import select
import math
import os
from fractions import Fraction
import logging
import time


log = logging.getLogger(__name__)




class MPlayerEOF(ValueError):
    pass

class MPlayerDied(ValueError):
    pass

class MPlayerBadFile(ValueError):
    pass


class MPlayer(object):
    
    # _id_keys is required by the __getattr__ and __setattr__. Unfortunately,
    # me make requests to thos methods before _id_keys would naturally be set.
    # I am putting a default here so we don't drop into infinite recursion. 
    _id_keys = set()
    
    def __init__(self, path, conf=None, autoplay=False):
        
        self._init_data()
        self._path = path
        
        cmd = ['mplayer', '-slave', '-quiet', '-framedrop', '-identify', ]
        if conf:
            cmd.extend(['-input', 'conf=' + conf])
        cmd.append(path)
        
        self.proc = Popen(cmd, stdin=PIPE, stdout=PIPE)
        
        self._stdin  = self.proc.stdin
        self._stdout = self.proc.stdout
        
        if not autoplay:
            self.pause()
            self.time = 0
            
        self._read(timeout=0.1)
        if self.data == dict(exit='EOF'):
            raise MPlayerBadFile(path)
    
    def _init_data(self):
        
        # All data read in.
        self.data = {}
        
        # The names of data that is constant.
        self._id_keys = set()
        
        # The current speed.
        self._speed = Fraction(1, 1)
        
        # It starts automatically playing.
        self._is_paused = False

    def __del__(self):
        try:
            if self.is_running:
                self._cmd('quit')
        except:
            pass
    
    is_eof = property(lambda self: 'exit' in self.data)
    is_running = property(lambda self: self.proc.poll() is None)
    
    def _assert_video(self):
        """Make sure the process is still running or throw an error."""
        if not self.is_running:
            raise MPlayerDied('mplayer has died')
        if self.is_eof:
            raise MPlayerEOF('mplayer hit EOF')

    def _readable(self, timeout=0):
        """Determine if we can read from mplayer without blocking."""
        if not self.is_running:
            return False
        r, w, x = select([self._stdout], (), (), timeout)
        return bool(r)

    def _read(self, timeout=0, key=None):
        """Read until we cannot anymore, or find the key we want.
        
        The timeout applies for every line read, so we can easily wait many
        times the supplied timeout.
        
        """
        desired_key = key
        while self._readable(timeout):
            key = None
            line = self._stdout.readline().strip()
            # log.debug(line)
            
            if line.startswith('ANS_'):
                key, value = line[4:].split('=')
                try:
                    value = float(value)
                except:
                    pass
            elif line.startswith('ID_'):
                key, value = line[3:].split('=')
                self._id_keys.add(key.lower())
                try:
                    value = int(value)
                except:
                    try:
                        value = float(value)
                    except:
                        pass
            if key is not None:
                key = key.lower()
                self.data[key] = value
                if key == desired_key:
                    return value

    def _cmd(self, cmd):
        """Makes a request to mplayer.

        We do not expect a response from this one.

        """
        self._stdin.write(cmd + '\n')
        self._stdin.flush()
    
    def get_property(self, name, timeout=1.0, pausing_keep_force=True):
        self._assert_video()
        self._cmd('%s get_property %s' % ('pausing_keep_force' if pausing_keep_force else 'pausing_keep', name))
        return self._read(timeout=timeout, key=name)
    
    def set_property(self, name, value, pausing_keep_force=True):
        self._assert_video()
        self._cmd('%s set_property %s %s' % ('pausing_keep_force' if pausing_keep_force else 'pausing_keep', name, value))


    is_paused = property(lambda self: self._is_paused)
    is_playing = property(lambda self: not self._is_paused)
    

    def pause(self):
        """Pause if playing."""
        if not self._is_paused:
            self._cmd('pausing_keep_force pause')
            self._is_paused = True

    def play(self):
        """Play if paused."""
        if self._is_paused:
            self._cmd('pause')
            self._is_paused = False
    
    def toggle_pause(self):
        """Toggle pause state. Play if paused and pause if playing."""
        self._cmd('pause')
        self._is_paused = not self._is_paused
    
    def step(self):
        """Pause and step to the next frame."""
        self._is_paused = True
        self._cmd('pausing frame_step')

    def stop(self):
        """Stop playing."""
        self._cmd('stop')


    time = property(lambda self: self.get_property('time_pos'))
    time = time.setter(lambda self, v: self.set_property('time_pos', v, pausing_keep_force=False))
    
    fps = property(lambda self: self.data['video_fps'])
    
    frame = property(lambda self: int(self.fps * self.time + 0.5))
    @frame.setter
    def frame(self, value):
        """This is not exact. It will only get close."""
        self.time = float(value) / float(self.fps)

    frame_count = property(lambda self: int(self.fps * self.length))

    speed = property(lambda self: self._speed)
    @speed.setter
    def speed(self, value):
        self._speed = Fraction(value)
        self.set_property('speed', float(value))
    
    def __getattr__(self, name):
        if name in self._id_keys:
            return self.data[name]
        return object.__getattribute__(self, name)
    # 
    # def __setattr__(self, name, value):
    #     print 'set', repr(name)
    #     if name in self._id_keys:
    #         raise ValueError('cannot set property %r' % name)
    #     
    #     # This should be a list of properies we will let you set.
    #     if False: #name in ():
    #         self.set_property(name[5:] if name.startswith('_raw_') else name, value)
    #     else:
    #         object.__setattr__(self, name, value)


if __name__ == '__main__':
    mp = MPlayer('/Users/mikeboers/Desktop/drives.txt')
