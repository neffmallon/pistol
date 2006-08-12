#!/usr/bin/env python
"""\
 mlist - experimenting with an overloaded list that does some simple
 math functions.
"""

import operator

class mlist(list):
    def __add__(self,other):
        assert len(self) == len(other)
        return [self[i]+other[i] for i in range(len(self))]

    def __mul__(self,other):
        assert len(self) == len(other)
        return [self[i]*other[i] for i in range(len(self))]

    def dot(self,other):
        assert len(self) == len(other)
        #return reduce(operator.add,[self[i]*other[i] for i in range(len(self))])
        # this is a little faster
        sum = 0
        for i in range(len(self)): sum += self[i]*other[i]
        return sum
        

if __name__ == '__main__':
    from random import randrange
    from Numeric import array,dot
    import time
    l = [randrange(10) for i in range(100000)]
    m = mlist(l)
    a = array(l)
    t1 = time.time()
    a2 = dot(a,a)
    t2 = time.time()
    m2 = m.dot(m)
    t3 = time.time()
    print t2-t1,t3-t2

    


    
