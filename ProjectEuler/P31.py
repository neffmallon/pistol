
from itertools import izip
from pprint import pprint
def dot(a,b):
    val = 0
    for ia,ib in izip(a,b): val += ia*ib
    return val

vals = 200,100,50,20, 10,5,2,1

partitions = {(1,0,0,0, 0,0,0,0): 1}

for i2 in range(101):
    total2 = 2*i2
    for i5 in range( (200-total2)/5 + 1 ):
        total5 = total2 + 5*i5
        for i10 in range((200-total5)/10 + 1):
            total10 = total5 + 10*i10
            for i20 in range((200-total10)/20 + 1):
                total20 = total10 + i20*20
                for i50 in range((200-total20)/50 + 1):
                    total50 = total20 + i50*50
                    for i100 in range((200-total50)/100 + 1):
                        trial = (0,i100,i50,i20, i10,i5,i2,0)
                        value = dot(trial,vals)
                        if value <= 200:
                            partitions[(0,i100,i50,i20,
                                        i10,i5,i2,200-value)] = 1

ps = partitions.keys()
ps.sort()
print len(ps)
pprint(ps)


