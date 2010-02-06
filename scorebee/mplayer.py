
from subprocess import Popen, PIPE
from select import select


def make_property(name, conformer=str):
    
    get_cmd = 'pausing_keep_force get_property %s' % name
    set_cmd = 'pausing_keep_force set_property %s' % name
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
        self._cmd(cmd, 0)
    
    return prop
    
class MPlayer(object):
    
    def __init__(self, src):
        
        self.proc = Popen(['mplayer', '-slave', '-quiet', src], stdin=PIPE,
            stderr=None, stdout=PIPE)
        
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        
        self.clear_read_buffer(0.1)
    
    @property
    def is_running(self):
        return self.proc.poll() is None
    
    def __del__(self):
        if self.is_running:
            self.stdin.write('quit\n')
            self.proc.kill()
    
    def readable(self, pipe, timeout=0):
        if not self.is_running:
            raise ValueError('proc has stopped')
        r, w, x = select([pipe], (), (), timeout)
        return bool(r)
    
    def clear_read_buffer(self, timeout=0):
        while self.readable(self.stdout, timeout):
            self.stdout.readline()
    
    def _cmd(self, cmd, timeout=0.1):
        self.clear_read_buffer()
        self.stdin.write(cmd + '\n')
        if self.readable(self.stdout, timeout):
            return self.stdout.readline().strip()
    
    speed = make_property('speed', float)
    fps = make_property('fps', float)
    time = make_property('time_pos', float)
    percent = make_property('percent_pos', float)
    length = make_property('length', float)
    