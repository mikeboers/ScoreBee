#!/usr/bin/env python2.6

"""Lab video organizer.

USAGE: python sort_raw_videos.py [-r] source_dir dest_dir 

"""

from glob import glob
import os
import sys
from subprocess import call

assert len(sys.argv) >= 3

source_dir = sys.argv[-2]
dest_dir   = sys.argv[-1]

recurse_once = sys.argv[1] == '-r'

source_dir = os.path.abspath(source_dir)
dest_dir   = os.path.abspath(dest_dir)

print 'From: %r' % source_dir
print 'Into: %r' % dest_dir

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

def process_folder(source_dir, dest_dir):
    print 'Opening %r.' % source_dir
    for path in glob(os.path.join(source_dir, 'C*.rcd')):
        cam_id = os.path.splitext(os.path.basename(path))[0]
        cam_no = int(cam_id[1:])
        print '\tProcessing camera %d.' % cam_no
        last_end_time = None
        current_dir = None
        i = 0
        for line in open(path):
            _, start_date, raw_start_time, end_date, end_time, name = line.strip().split(',')
            start_date = start_date.replace('/', '-')
            start_time = raw_start_time.replace(':', '-')
            print '\t\t%sT%s' % (start_date, start_time), 
            if raw_start_time != last_end_time:
                print '- NEW!'
                i = 0
                current_dir = os.path.join(dest_dir, '%s_%s_cam-%d' % (start_date, start_time, cam_no))
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
            else:
                print
            last_end_time = end_time
            i += 1
            call(['cp',
                os.path.join(source_dir, cam_id, name),
                os.path.join(current_dir, '%s_%s_cam-%d.mp4' % (start_date, start_time, cam_no))
            ])


if recurse_once:
    for name in os.listdir(source_dir):
        source = os.path.join(source_dir, name)
        dest = os.path.join(dest_dir)
        if os.path.isdir(source):
            if not os.path.exists(dest):
                os.makedirs(dest)
            process_folder(source, dest)
else:
    process_folder(source_dir, dest_dir)
