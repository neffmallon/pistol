#!/usr/bin/env python
"""
Peter has nine four-sided (pyramidal) dice, each with faces numbered
1, 2, 3, 4. Colin has six six-sided (cubic) dice, each with faces
numbered 1, 2, 3, 4, 5, 6.

Peter and Colin roll their dice and compare totals: the highest total
wins. The result is a draw if the totals are equal.

What is the probability that Pyramidal Pete beats Cubic Colin? Give
your answer rounded to seven decimal places in the form 0.abcdefg
"""

class Counter:
    def __init__(self,hits=0,total=0):
        self.hits = hits
        self.total = total
        return

    def hit(self):
        self.hits += 1
        self.total += 1
        return
    
    def miss(self): self.total += 1
    def curr(self): return self.hits/float(self.total)
    def summary(self):
        return self.hits/float(self.total), self.hits, self.total

def dice(nsides=6):
    from random import randint
    return randint(1,nsides)

def rollsum(nrolls=1,nsides=6):
    return sum(dice(nsides) for i in xrange(nrolls))

def avg(seq):
    s = 0
    n = 0
    for i in seq:
        s += seq.next()
        n += 1
    return s/float(n)

def dist4():
    """
    Compute the distribution of 9 rolls of a 4-sided dice.
    """
    d = [0]*37
    res = range(1,5)
    for i in res:
        for j in res:
            for k in res:
                for l in res:
                    for m in res:
                        for n in res:
                            for o in res:
                                for p in res:
                                    for q in res:
                                        d[i+j+k+l+m+n+o+p+q] += 1
    return d

def dist6():
    """
    Compute the distribution of 6 rolls of a 6-sided dice.
    """
    d = [0]*37
    res = range(1,7)
    for i in res:
        for j in res:
            for k in res:
                for l in res:
                    for m in res:
                        for n in res:
                            d[i+j+k+l+m+n] += 1
    return d

def naive(ntries=1e8):
    c = Counter(171944695, 300000000)
    for i in xrange(int(ntries)):
        roll6 = rollsum(6,6)
        roll4 = rollsum(9,4)
        if roll6 < roll4:
            c.hit()
        else:
            c.miss()
        if i % 3e5 == 0: print i/1e5,c.curr()
    print c.summary()
    return

def main():
    d4 = dist4()
    sum4 = sum(d4)
    d6 = dist6()
    sum6 = sum(d6)
    print d4
    print d6
    print sum4,sum6
    N = len(d4)
    prob = 0.0
    denom = float(sum4*sum6)
    for i in range(N):
        for j in range(i+1,N):
            prob += d6[i]*d4[j]/denom
    print prob
            
    

if __name__ == '__main__': main()


        
