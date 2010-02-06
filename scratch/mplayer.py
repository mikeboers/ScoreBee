
import os
import sys
import time

sys.path.append('.')

from scorebee.mplayer import MPlayer


assert len(sys.argv) > 1, 'Not enough arguments.'


mp = MPlayer(sys.argv[1])
print mp

time.sleep(0.5)

names = 'time fps speed'.split()
while True:
    time.sleep(1)
    start_time = time.time()
    for name in names:
        v = getattr(mp, name)
        print name, repr(v)
    print '\tin %.2fms, each' % (1000 * (time.time() - start_time) / len(names))