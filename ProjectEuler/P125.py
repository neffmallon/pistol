#!/usr/bin/env python
from pprint import pprint
from math import sqrt
from sets import Set

def is_palindrome_list(l):
    """
    >>> is_palindrome_list([1,2,3,4])
    False
    >>> is_palindrome_list([1,2,3,2,1])
    True
    >>> is_palindrome_list('madam')
    True
    >>> is_palindrome_list('madame')
    False
    """
    n = len(l)
    for i in range(n/2):
        if l[i] != l[-(i+1)]:
            return False
    return True

def main(nmax=1000):
    import time
    t0 = time.time()
    results = []
    nsq = int(sqrt(nmax))+1
    for i in range(1,nsq):
        s = i*i
        for l in range(1,nsq-i):
            s += (i+l)**2
            if s >= nmax: break
            if is_palindrome_list(str(s)):
                results.append(s)
    print time.time()-t0
    print len(results),sum(results),sum(Set(results))
    results.sort()
    pprint(results)


if __name__ == '__main__': main(100000000)
# 2906969179 was the final correct answer    
