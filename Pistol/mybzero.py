#!/usr/bin/env python
"""\
 This contains my hacks for using bzero to run a blog. It makes a
 bzero post file for when I'm away from my home machine, so that I can
 later upload the file and post from there.
"""

import os
import glob
import time

HOME_DEFAULT = '/home/rmuller'
BLOG_DEFAULT = 'fts'

post_template = """\
#date %s
%%topics %s
%%title %s
%%format html
%s
"""

def write_new_post(fname,date,topics='',title='',body=''):
    open(fname,'w').write(post_template % (date,topics,title,body))
    return

def get_home():
    home = os.getenv('HOME')
    if not home: home = HOME_DEFAULT
    return home

def newpost():
    home = get_home()
    data_dir = os.path.join(home,'Desktop')
    date = time.localtime()
    year = date[0]
    month = date[1]
    day = date[2]

    fname = None
    for i in range(1,100):
        test_fname = os.path.join(data_dir,'bzero_%d.txt' % i)
        if os.path.exists(test_fname):
            print test_fname," exists"
            continue
        else:
            print test_fname," does not exist"
            fname = test_fname
            break
    if not fname: raise "Warning: exceeded maximum number of posts in a day"
    write_new_post(fname,date)
    print "File %s may now be edited manually" % fname
    return

if __name__ == '__main__': newpost()
