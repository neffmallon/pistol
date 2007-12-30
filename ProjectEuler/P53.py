def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)

def C(n,r): return factorial(n)/factorial(r)/factorial(n-r)

from sets import Set
works = Set()
for i in range(1,101):
    for j in range(1,i):
        if C(i,j) > 1000000:
            works.add((i,j))
            if j != i-j:
                works.add((i,i-j))
print len(works)
print works
