from math import sqrt

def ndivisors(n):
    "just count the divisors of n"
    s = 0
    lim = int(sqrt(n)+1)
    for i in xrange(1,lim):
        if n%i == 0: s+=2
    return s

def main(nmax=10**7):
    ndivm = -1
    succ = 0
    for i in xrange(2,nmax):
        ndiv = ndivisors(i)
        if ndiv == ndivm:
            succ += 1
        ndivm = ndiv
        if i%10**5 == 0: print i,succ
    print succ
    return

if __name__ == '__main__': main()

# 986451 was incorrect, as were 986450 and 986452
