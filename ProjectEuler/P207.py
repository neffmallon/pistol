"""
For some positive integers k, there exists an integer partition of the
form 4^(t) = 2^(t) + k, where 4^(t), 2^(t), and k are all positive
integers and t is a real number.

The first two such partitions are 4^(1) = 2^(1) + 2 and
4^(1.5849625...) = 2^(1.5849625...) + 6.

Partitions where t is also an integer are called perfect. For any m >=
1 let P(m) be the proportion of such partitions that are perfect with
k <= m. Thus P(6) = 1/2.

In the following table are listed some values of P(m)

   P(5) = 1/1
   P(10) = 1/2
   P(15) = 2/3
   P(20) = 1/2
   P(25) = 1/2
   P(30) = 2/5
   ...
   P(180) = 1/4
   P(185) = 3/13

Find the smallest m for which P(m) < 1/12345
"""

from Utils import Rational
from itertools import count
from sets import Set

def main():
    powers2 = Set(2**i for i in range(100))
    hits = 0
    total = 0
    for i in count(2):
        if i in powers2: hits += 1
        total += 1
        k = i*(i-1)
        val = Rational(hits,total)
        print i*(i-1),val
        if val.float() < 1/float(12345):
            print "GOAL REACHED"
            break
    return

if __name__ == '__main__':
    main()

