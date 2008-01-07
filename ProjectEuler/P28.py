"""
Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of both diagonals is 101.

What is the sum of both diagonals in a 1001 by 1001 spiral formed in the same way?
"""

from Utils import spiral_matrix

def primes(n):
    """\
    From python cookbook
    returns a list of prime numbers from 2 to < n

    >>> primes(2)
    [2]
    >>> primes(10)
    [2, 3, 5, 7]
    """
    if n==2: return [2]
    elif n<2: return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]


def main(**kwargs):
    """\
    Make a nxn prime spiral.
    """
    n = kwargs.get('n',5)
    p = spiral_matrix(n)
    if n < 15: print p
    dsum1 = 0
    dsum2 = 0
    for i in range(n):
        dsum1 += p[i,i]
        dsum2 += p[n-i-1,i]
    print "diagonal sums: ",dsum1,dsum2,dsum1+dsum2-p[n/2,n/2]
    return None

def test():
    from doctest import testmod
    testmod()

if __name__ == '__main__':
    #test()
    main(n=1001)
