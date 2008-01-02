"""
The fraction 49/98 is a curious fraction, as an inexperienced
mathematician in attempting to simplify it may incorrectly believe
that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction,
less than one in value, and containing two digits in the numerator and
denominator.

If the product of these four fractions is given in its lowest common
terms, find the value of the denominator.
"""
from copy import copy
def num_to_digits(n): return map(int,str(n))
def farey(v, lim):
  '''Named after James Farey, an English surveyor.
  No error checking on args -- lim = max denominator,
  results are (numerator, denominator), (1,0) is infinity
  '''
  if v < 0:
    n,d = farey(-v, lim)
    return -n,d
  z = lim-lim	# get 0 of right type for denominator
  lower, upper = (z,z+1), (z+1,z)
  while 1:
    mediant = (lower[0] + upper[0]), (lower[1]+upper[1])
    if v * mediant[1] > mediant[0]:
        if lim < mediant[1]: return upper
        lower = mediant
    elif v * mediant[1] == mediant[0]:
        if lim >= mediant[1]: return mediant
        if lower[1] < upper[1]: return lower
        return upper
    else:
        if lim < mediant[1]: return lower
        upper = mediant
  return None

nmax = 100
results = []
for i in range(10,nmax):
    for j in range(10,i):
        val = j/float(i)
        numerator_digits = num_to_digits(j)
        denominator_digits = num_to_digits(i)
        for nd in numerator_digits:
            
            if nd not in denominator_digits or nd == 0: continue
            digs = copy(numerator_digits)
            digs.remove(nd)
            num = digs[0]
            digs = copy(denominator_digits)
            digs.remove(nd)
            den = digs[0]
            if den == 0: continue
            vval = num/float(den)
            if vval == val: results.append((j,i))
np = 1
dp = 1
for n,d in results:
    np *= n
    dp *= d
print np,dp
print np/32.,dp/32.


