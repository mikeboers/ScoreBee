
from subprocess import Popen, PIPE
from select import select


def make_property(name, conformer=str):
    
    cmd = 'pausing_keep_force get_property %s' % name
    res_prefix = 'ANS_%s=' % name
    res_prefix_len = len(res_prefix)
    
    @property
    def prop(self):
        raw = self._cmd(cmd, 1)
        if raw:
            # assert raw.startswith(res_prefix)
            try:
                v = conformer(raw[res_prefix_len:])
            except:
                v = None
            return (raw, v)
    
    @prop.setter
    def prop(self, value):
        return None
    
    return prop
    
class MPlayer(object):
    
    def __init__(self, src):
        
        self.proc = Popen(['mplayer', '-slave', '-quiet', src], stdin=PIPE,
            stderr=None, stdout=PIPE)
        
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        
        self.clear_read_buffer(0.1)
    
    def __del__(self):
        self.stdin.write('quit')
        self.stdin.flush()
        self.proc.kill()
    
    def readable(self, pipe, timeout=0):
        r, w, x = select([pipe], (), (), timeout)
        return bool(r)
    
    def clear_read_buffer(self, timeout=0):
        while self.readable(self.stdout, timeout):
            self.stdout.readline()
    
    def _cmd(self, cmd, timeout=0.1):
        self.clear_read_buffer()
        self.stdin.write(cmd + '\n')
        self.stdin.flush()
        if self.readable(self.stdout, timeout):
            return self.stdout.readline().strip()
    
    speed = make_property('speed', float)
    fps = make_property('fps', float)
    time = make_property('time_pos', float)
    percent = make_property('percent_pos', float)
    length = make_property('length', float)
    