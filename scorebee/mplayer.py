
from subprocess import Popen, PIPE
from select import select
import math
import os
from fractions import Fraction
import logging


log = logging.getLogger(__name__)


def make_property(name, conformer=str, force_get=True, force_set=True):
    
    get_cmd = 'pausing_keep%s get_property %s' % ('_force' if force_get else '', name)
    set_cmd = 'pausing_keep%s set_property %s' % ('_force' if force_set else '', name)
    res_prefix = 'ANS_%s=' % name
    res_prefix_len = len(res_prefix)
    
    @property
    def prop(self):
        raw = self._cmd(get_cmd)
        if raw:
            try:
                v = conformer(raw[res_prefix_len:])
            except:
                v = None
            return v
    
    @prop.setter
    def prop(self, *args):
        cmd = set_cmd + ' ' + ' '.join(str(x) for x in args)
        # print cmd
        self._cmd(cmd, 0)
    
    return prop


class MPlayerDied(ValueError):
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
        
        self._fps = None
        self._speed = Fraction(1, 1)
        
        while self.length is None:
            self.clear_read_buffer()
    
    @property
    def frame_count(self):
        return int(self.fps * self.length)
    
    @property
    def is_running(self):
        return self.proc.poll() is None
    
    def assert_running(self):
        if self.proc.poll() is not None:
            raise MPlayerDied('mplayer has died')
    
    def stop(self):
        if self.is_running:
            self._cmd('exit', 0)
            self.proc.kill()
    
    def __del__(self):
        self.stop()
    
    def readable(self, pipe, timeout=0):
        self.assert_running()
        r, w, x = select([pipe], (), (), timeout)
        return bool(r)
    
    def clear_read_buffer(self, timeout=0):
        while self.readable(self.stdout, timeout):
            self.stdout.readline()
    
    def _cmd(self, cmd, timeout=0.1):
        self.clear_read_buffer()
        # log.debug('cmd %r' % cmd)
        self.stdin.write(cmd + '\n')
        self.stdin.flush()
        if self.readable(self.stdout, timeout):
            return self.stdout.readline().strip()
    
    @property
    def is_paused(self):
        return self._is_paused
    
    def pause(self):
        if not self._is_paused:
            self._cmd('pausing_keep_force pause', 0)
            self._is_paused = True
    
    def play(self):
        if self._is_paused:
            self._cmd('pause', 0)
            self._is_paused = False
    
    @property
    def fps(self):
        if self._fps is None:
            self._fps = self.__fps
        return self._fps
    
    @property
    def frame(self):
        time = self.time
        if time is not None:
            return int(math.ceil(self.fps * time))
    
    @frame.setter
    def frame(self, value):
        """This is not exact. It will only get close."""
        # print float(value) / float(self.fps)
        self.time = float(value) / float(self.fps)
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = Fraction(value)
        self.__speed = float(value)
    
    __speed = make_property('speed', float)
    
    __fps = make_property('fps', float)
    time = make_property('time_pos', float, force_set=False)
    percent = make_property('percent_pos', float)
    length = make_property('length', float)
    