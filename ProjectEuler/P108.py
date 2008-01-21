#!/usr/bin/env python
"""
In the following equation x, y, and n are positive integers.
1/x + 1/y = 1/n

For n = 4 there are exactly three distinct solutions:
1/5 + 1/20 = 1/4
1/6 + 1/12 = 1/4
1/8+1/8 = 1/4

What is the least value of n for which the number of distinct
solutions exceeds one-thousand?
"""
import psyco; psyco.full()
from pprint import pprint
from Utils import Rational

def brute(nmax = 50000):
    # 10,000 only lead to items that had 58 solutions (1/840),
    #  so I have to find a smarter method
    results = {}
    for i in range(1,nmax+1):
        ri = Rational(1,i)
        for j in range(1,i+1):
            rj = Rational(1,j)
            rs = ri.add(rj).inverse()
            if rs.isint():
                v = rs.int()
                if v in results:
                    results[v].append((i,j))
                else:
                    results[v] = [(i,j)]

    sortable = [(len(results[k]),k) for k in results]
    sortable.sort()
    pprint(sortable[-3:])
    return


