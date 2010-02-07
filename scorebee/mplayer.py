
from subprocess import Popen, PIPE
from select import select
import math
import os
from fractions import Fraction
import logging


log = logging.getLogger(__name__)


def make_property(name, parser=str, force_get=True, force_set=True, buffer=False):
    
    get_cmd = 'pausing_keep%s get_property %s' % ('_force' if force_get else '', name)
    set_cmd = 'pausing_keep%s set_property %s %%s' % ('_force' if force_set else '', name)
    
    buffer_attr_name = '_' + name + '_buffer'
    
    res_prefix = 'ANS_%s=' % name
    res_prefix_len = len(res_prefix)
    
    @property
    def prop(self):
        x = getattr(self, buffer_attr_name, None) if buffer else None
        if x is not None:
            return x
            
        raw = self._cmd_read(get_cmd)
        try:
            if not raw.startswith(res_prefix):
                raise MPlayerComFailure('wrong parameter; got %r, expected %r' % (raw, res_prefix))
            v = parser(raw[res_prefix_len:])
        except:
            log.exception('error while parsing response')
            raise
        if buffer:
            setattr(self, buffer_attr_name, v)
        return v
        
    @prop.setter
    def prop(self, v):
        self._cmd(set_cmd % v)
        setattr(self, buffer_attr_name, v)
        
    return prop




class MPlayerDied(ValueError):
    pass


class MPlayerComFailure(ValueError):
    pass


class MPlayer(object):
    
    def __init__(self, src, autoplay=False):
        
        self.proc = Popen(['mplayer', '-slave', '-quiet', '-framedrop', 
            '-input', 'conf=' + os.path.abspath(__file__ + '/../../settings/mplayer.txt'),
            src], stdin=PIPE, stderr=None, stdout=PIPE)
        
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        
        self._is_paused = False
        if not autoplay:
            self.pause()
        
        self._speed = Fraction(1, 1)
        
        self._clear_read_buffer(0.1)
    
    def __del__(self):
        self.stop()
    
    @property
    def frame_count(self):
        return int(self.fps * self.length)
    
    
    def assert_running(self):
        """Make sure the process is still running or throw an error."""
        if self.proc.poll() is not None:
            raise MPlayerDied('mplayer has died')
            
    @property
    def is_running(self):
        return self.proc.poll() is None
    
    def stop(self):
        """Stop playing and kill the process."""
        if self.is_running:
            self._cmd('exit')
            self.proc.kill()
    
    
    def readable(self, pipe, timeout=0):
        self.assert_running()
        r, w, x = select([pipe], (), (), timeout)
        return bool(r)
    
    def _clear_read_buffer(self, timeout=0):
        """Clear out the read buffer before we issue a command."""
        while self.readable(self.stdout, timeout):
            log.info('cleared %r' % self.stdout.readline().strip())

    def _cmd(self, cmd):
        """Makes a request to mplayer.
        
        We do not expect a response from this one.
        
        """
        self.stdin.write(cmd + '\n')
        self.stdin.flush()
    
    def _cmd_read(self, cmd, timeout=1.0):
        """Makes a request and waits for a response."""
        self._clear_read_buffer()
        self.stdin.write(cmd + '\n')
        self.stdin.flush()
        if self.readable(self.stdout, timeout):
            return self.stdout.readline().strip()
    
    @property
    def is_paused(self):
        return self._is_paused
    
    @property
    def is_playing(self):
        return not self._is_paused
    
    def pause(self):
        if not self._is_paused:
            self._cmd('pausing_keep_force pause')
            self._is_paused = True
    
    def play(self):
        if self._is_paused:
            self._cmd('pause')
            self._is_paused = False
    
    @property
    def frame(self):
        return int(math.ceil(self.fps * self.time))
    
    @frame.setter
    def frame(self, value):
        """This is not exact. It will only get close."""
        self.time = float(value) / float(self.fps)
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = Fraction(value)
        self._raw_speed = float(value)
    
    
    _raw_speed  = make_property('speed', float)
    fps    = make_property('fps', float, buffer=True)
    length = make_property('length', float, buffer=True)
    
    time = make_property('time_pos', float, force_set=False)
    percent = make_property('percent_pos', float)
    