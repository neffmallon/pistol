# Testing the solution to P31 to find the partitions of a dollar

from itertools import izip
from pprint import pprint

def dot(a,b):
    val = 0
    for ia,ib in izip(a,b): val += ia*ib
    return val

vals = 100,50,25, 10,5,1

partitions = {(1,0,0, 0,0,0): 1}

for i5 in range(21):
    total5 = 5*i5
    for i10 in range((100-total5)/10 + 1):
        total10 = total5 + 10*i10
        for i25 in range((100-total10)/25 + 1):
            total25 = total10 + i25*25
            for i50 in range((100-total25)/50 + 1):
                trial = (0,i50,i25, i10,i5,0)
                value = dot(trial,vals)
                if value <= 100:
                    partitions[(0,i50,i25,i10,i5,100-value)] = 1

ps = partitions.keys()
ps.sort()
print len(ps)
pprint(ps)


