def num_to_digits(n): return map(int,str(n))

def isPandigitalN(i):
    ijk = num_to_digits(i)
    ndig = len(ijk)
    ijk.sort()
    return ijk == [1,2,3,4,5,6,7,8,9][:ndig]

def primes(n):
    # From python cookbook
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

for p in primes(100000000):
    if isPandigitalN(p): print p


