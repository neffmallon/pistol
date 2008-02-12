
from itertools import count
#from Utils import issquare
from sets import Set

def sqpairs(N):
    for y in range(1,N):
        for z in range(1,y):
            if issquare(y-z) and issquare(y+z):
                yield y,z
    return

def all3():
    for x in count(3):
        for y,z in sqpairs(x):
            if issquare(x-y) and issquare(x-z) and issquare(x+y) \
               and issquare(x+z):
                print x,y,z
    return

def trips_sat3(N):
    #yield triplets that satisfy issquare(y+z),issquare(y-z),issquare(x+y)
    for k in xrange(1,N):
        k2 = k*k
        for j in xrange(1,k):
            j2 = j*j
            for i in xrange(1,j):
                i2 = i*i
                if (j2+i2)%2: continue # if the sum is odd, so is the diff
                y = (j2+i2)/2
                z = (j2-i2)/2
                x = k2-y                
                yield x,y,z
    return

def test_trips_sat3(N=100):
    for x,y,z in trips_sat3(N):
        assert issquare(y+z) and issquare(y-z) and issquare(x+y)
    return

def main(N=1000):
    sqs = Set(i*i for i in range(1,N))
    def issq(x): return x in sqs
    #yield triplets that satisfy issquare(y+z),issquare(y-z),issquare(x+y)
    for x,y,z in trips_sat3(N):
        if issq(x-y) and issq(x-z) and issq(x+z):
            print x,y,z

if __name__ == '__main__': main()

    
