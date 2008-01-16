#!/usr/bin/env python
from math import sqrt

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
    results = []
    sqs = [i*i for i in range(1,int(sqrt(nmax))+1)]
    nsq = len(sqs)
    for l in range(2,nsq):
        for i in range(0,nsq-l+1):
            n = sum(sqs[i:(i+l)])
            if is_palindrome_list(str(n)) and n<nmax:
                results.append(n)
    print len(results),sum(results)


if __name__ == '__main__': main(100000000)
    
