#!/usr/bin/env python2.6

"""Lab video organizer.

USAGE: python sort_raw_videos.py src_dir dst_dir 

"""

date_to_count = {
    '2010-10-12': 4,
    '2010-01-19': 8,
    '2010-01-20': 10,
    '2010-01-24': 11,
    '2010-01-26': 12,
    '2010-01-27': 2,
    '2010-01-29': 15,
    '2010-02-04': 4,
}

cam_no_to_letter = {
    8: 'F',
    5: 'E',
    6: 'D',
    1: 'A',
    4: 'B',
    3: 'C',
}

trials_to_ignore = '''




'''.strip().split()

from glob import glob
import os
import sys
from subprocess import call

assert len(sys.argv) >= 3

src_dirs = sys.argv[1:-1]
dst_dir   = sys.argv[-1]

src_dirs  = [os.path.abspath(x) for x in src_dirs]
dst_dir   = os.path.abspath(dst_dir)

print 'From: %r' % src_dirs
print 'Into: %r' % dst_dir

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

warnings = []

def process_folder(src_dir, dst_dir):
    print 'Opening %r.' % src_dir
    for path in glob(os.path.join(src_dir, 'C*.rcd')):
        cam_id = os.path.splitext(os.path.basename(path))[0]
        cam_no = int(cam_id[1:])
        cam_letter = cam_no_to_letter[cam_no + 1] # Cause people count from 1 this this case.
        print '\tProcessing camera %d.' % cam_no
        last_end_time = None
        current_dir = None
        current_time_stamp = None
        for line in open(path):
            _, start_date, raw_start_time, end_date, end_time, name = line.strip().split(',')
            start_date = start_date.replace('/', '-')
            h, m, s = raw_start_time.split(':')
            start_time = '%02d-%s-%s' % (int(h) + 1, m, s)
            time_stamp = '%s_%s_cam-%s' % (start_date, start_time, cam_letter)
            print '\t\t%s' % time_stamp,
            if raw_start_time != last_end_time:
                print '- Starting new trial.'
                current_dir = os.path.join(dst_dir, time_stamp)
                current_time_stamp = time_stamp
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)
            else:
                print
            last_end_time = end_time
            
            src_path = os.path.join(src_dir, cam_id, name)
            dst_path = os.path.join(current_dir, '%s.mp4' % time_stamp)
            if not os.path.exists(src_path):
                warnings.append('%s - %s does not exist' % (current_time_stamp, src_path))
                continue
            elif os.path.exists(dst_path):
                dst_size = os.path.getsize(dst_path)
                src_size = os.path.getsize(src_path)
                if dst_size != src_size:
                    warnings.append('%s - %s - sizes differ' % (current_time_stamp, dst_path))
                continue
            ret = call(['ln',
                src_path,
                dst_path
            ])
            if ret:
                warnings.append('%s - %s - ln returned %d' % (current_time_stamp, src_path, ret))

for src_dir in src_dirs:
    for name in os.listdir(src_dir):
        src = os.path.join(src_dir, name)
        dst = os.path.join(dst_dir)
        if os.path.isdir(src):
            if not os.path.exists(dst):
                os.makedirs(dst)
            process_folder(src, dst)

last_stamp = None
count = 0
for x in sorted(warnings):
    stamp = x.split()[0]
    if last_stamp != stamp:
        last_stamp= stamp
        print count, 'warnings'
        print
        count = 0
        print stamp
    count += 1
    print '\t', x
if count:
    print count, 'warnings'