"""
A googol (10^100) is a massive number: one followed by one-hundred
zeros; 100^100 is almost unimaginably large: one followed by
two-hundred zeros. Despite their size, the sum of the digits in each
number is only 1.

Considering natural numbers of the form, a^b, where a, b < 100, what is
the maximum digital sum?
"""

def num_to_digits(n): return map(int,str(n))

N = 100

maxsum = 0
for i in range(1,N):
    for j in range(1,N):
        num = pow(i,j)
        maxsum = max(maxsum,sum(num_to_digits(num)))
print maxsum

