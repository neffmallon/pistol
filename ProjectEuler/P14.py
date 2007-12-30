"""
The following iterative sequence is defined for the set of positive integers:

n -> n/2 (n is even)
n -> 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
13 40 20 10 5 16 8 4 2 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?
"""

def next(n):
    if n%2 == 0: return n/2
    return 3*n+1

def sequence(n):
    s = [n]
    while 1:
        n = next(n)
        s.append(n)
        if n == 1: break
    return s

def sequence_length(n): return len(sequence(n))

iis = range(1,1000000)
ls = [sequence_length(i) for i in iis]

zs = zip(ls,iis)
zs.sort()

print zs[-10:]


