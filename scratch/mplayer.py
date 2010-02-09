
import os
import sys
import time
from subprocess import Popen, PIPE
import string

printable = set(string.printable) - set('\n\r')


assert len(sys.argv) > 1, 'Not enough arguments.'

proc = Popen('mplayer -slave -identify -framedrop'.split() + [sys.argv[1]],
    stdout=PIPE)

stdout = os.fdopen(proc.stdout.fileno(), 'rU')

while True:
    line = stdout.readline()
    if not line:
        break
    
    line = ''.join(x if x in printable else '?' for x in line)
    
    print
    print ' ' + ''.join('%d' % (i/10) for i in range(len(line)))    
    print ' ' + ''.join('%d' % (i%10) for i in range(len(line)))
    print repr(line)