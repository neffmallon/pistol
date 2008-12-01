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

def rollsum(ntimes=1,nsides=6):
    return sum(dice(nsides) for i in xrange(ntimes))

def avg(seq):
    s = 0
    n = 0
    for i in seq:
        s += seq.next()
        n += 1
    return s/float(n)

def main(ntries=1e8):
    c = Counter(57320085, 100000000)
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
    

if __name__ == '__main__': main()


        
