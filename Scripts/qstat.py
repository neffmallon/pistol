#!/usr/bin/env python
"""\
 Wrapper around the qstat utility that sorts the jobs by user.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os

def qstat():
    qs = os.popen('qstat')
    jobs = {}
    lines = qs.readlines()
    for line in lines[2:]:
        pid,job,user,time,status,queue = line.split()
        if jobs.has_key(user):
            jobs[user].append((pid,job,time))
        else:
            jobs[user] = [(pid,job,time)]

    users = jobs.keys()
    users.sort()
    for user in users:
        print user, len(jobs[user])
        for job in jobs[user]:
            print "       %-6s    %-20s    %-10s" % job

if __name__ == '__main__': qstat()

