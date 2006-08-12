#!/usr/bin/env python
"Bank Queue model from Dewdney's Turning Omnibus"

from math import log
import random
import biggles

avgArrive = 2.0   # average time between arrivals
avgService = 2.0  # average time of service

def bankQueue(timeMax = 600): # t in minutes
    ta = 0       # time to next arrival in minutes
    ts = 0       # time to end of next service in minutes
    q = 1        # number of people in the queue
    c = 0        # time on the clock in minutes
    nserved = 0  # total number of people served
    cs = []
    ss = []
    qs = []
    while c < timeMax:
        if q == 0:
            c += ta
            q += 1
            ta = random.expovariate(1./avgArrive)
        elif ta<ts:
            ts -= ta
            c += ta
            q += 1
            ta = random.expovariate(1./avgArrive)
        else:
            ta -= ts
            c += ts
            q -= 1
            ts = random.expovariate(1./avgService)
            nserved += 1
        cs.append(c/60.)
        ss.append(nserved)
        qs.append(q)
    # end while
    p = biggles.FramedPlot()
    c1 = biggles.Curve(cs,ss,color='red')
    c2 = biggles.Curve(cs,qs,color='blue')
    p.add(c1,c2)
    p.show()
if __name__ == '__main__': bankQueue()
