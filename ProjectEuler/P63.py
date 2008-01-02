"""
The 5-digit number, 16807=7^5, is also a fifth power. Similarly, the
9-digit number, 134217728=8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""

def num_to_digits(n): return map(int,str(n))
def ndigits(n): return len(num_to_digits(n))

emax = 1000
vs = []
for e in range(1,emax):
    for i in range(1,10000):
        v = pow(i,e)
        if ndigits(v) == e:
            vs.append(v)
        elif ndigits(v) > e:
            break
print len(vs),vs
