"""
A Hamming number is a positive number which has no prime factor larger
than 5. So the first few Hamming numbers are 1, 2, 3, 4, 5, 6, 8, 9,
10, 12, 15. There are 1105 Hamming numbers not exceeding 10^(8).

We will call a positive number a generalised Hamming number of type n,
if it has no prime factor larger than n. Hence the Hamming numbers are
the generalised Hamming numbers of type 5.

How many generalised Hamming numbers of type 100 are there which don't
exceed 10^(9)?
"""

def hamming_type(n=5,nmax=10**6,doprint=True):
    from Utils import primes
    from BitVector import BitVector
    ps = [1] + primes(n)
    N = nmax+1
    data = BitVector(size=N)
    np = len(ps)
    for i in range(n):
        for p in ps:
            if p*i < nmax:
                data[p*i] = 1
    if doprint:
        print [i for i in range(1,N) if data[i]]
    print "There are %d hamming numbers of type %d that don't exceed %d" % (
        sum(data),n,nmax)
    return

if __name__ == '__main__':
    hamming_type()
