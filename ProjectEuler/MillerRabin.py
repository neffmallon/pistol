"""The Miller-Rabin primality test.

http://snippets.dzone.com/posts/show/4200

MillerRabin(n, s = 1000) -> bool Checks whether n is prime or not.
This is an extremley fast algorithm designed to test very large
numbers.

s is the number of tests to perform. The chance that Rabin-Miller is
mistaken about a number (i.e. thinks it's prime, but it's not) is
2^(-s). So, a value of 50 for s is more than enough for any imaginable
goal (2^(-50) is 8.8817841970012523e-16).
"""

import sys
import random

def isprime(n):
    return n > 1 and MillerRabin(n)

def toBinary(n):
  r = []
  while (n > 0):
    r.append(n % 2)
    n = n / 2
  return r

def test(a, n):
  """
  test(a, n) -> bool Tests whether n is complex.

  Returns:
    - True, if n is complex.
    - False, if n is probably prime.

  This function computes the witnesses, which are of the form:
  a**(n-1) % n == 1 -> True
  """
  b = toBinary(n - 1)
  d = 1
  for i in xrange(len(b) - 1, -1, -1):
    x = d
    d = (d * d) % n
    if d == 1 and x != 1 and x != n - 1:
      return True # Complex
    if b[i] == 1:
      d = (d * a) % n
  if d != 1:
    return True # Complex
  return False # Prime

def MillerRabin(n, s = 50):
  """
    MillerRabin(n, s = 1000) -> bool Checks whether n is prime or not

    Returns:
      - True, if n is probably prime.
      - False, if n is complex.
  """
  for j in xrange(1, s + 1):
    a = random.randint(1, n - 1)
    if (test(a, n)):
      return False # n is complex
  return True # n is prime

def RickTests(nmax=200,ntrials=15):
    """\
    Check Mersenne primes up to nmax for primality
    """
    two_to_n = 2
    for i in range(2,nmax):
        two_to_n *= 2
        n = two_to_n - 1
        if MillerRabin(i,ntrials*2):
            print i,n,MillerRabin(n,ntrials)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        RickTests()
        sys.exit()
    if len(sys.argv) >= 2:
        n = int(sys.argv[1])
        s = 50
    if len(sys.argv) > 2:
        s = int(sys.argv[2])
    print MillerRabin(n,s)
    
