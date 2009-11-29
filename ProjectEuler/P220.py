"""
Let D_(0) be the two-letter string 'Fa'. For n>=1, derive D_(n) from
D_(n-1) by the string-rewriting rules:

'a' -> 'aRbFR'
'b' -> 'LFaLb'

Thus, D_(0) = 'Fa', D_(1) = 'FaRbFR', D_(2) = 'FaRbFRRLFaLbFR', and so
on.

These strings can be interpreted as instructions to a computer
graphics program, with 'F' meaning 'draw forward one unit', 'L'
meaning 'turn left 90 degrees', 'R' meaning 'turn right 90 degrees',
and 'a' and 'b' being ignored. The initial position of the computer
cursor is (0,0), pointing up towards (0,1).

Then D_(n) is an exotic drawing known as the Heighway Dragon of order
n. For example, D_(10) is shown below; counting each 'F' as one step,
the highlighted spot at (18,16) is the position reached after 500
steps.
"""

from itertools import islice

from pylab import plot,show

def update_string(s):
    """
    Use the Heigway Dragon rules to update a string
    >>> update_string('Fa')
    'FaRbFR'
    >>> update_string('FaRbFR')
    'FaRbFRRLFaLbFR'
    """
    news = []
    for c in s:
        if c == 'a':
            news.append('aRbFR')
        elif c == 'b':
            news.append('LFaLb')
        else:
            news.append(c)
    return ''.join(news)

def count_occurrences(c,s):
    """
    Return the number of occurrances of character c in string s
    >>> count_occurrences('R','Rick')
    1
    """
    return sum(1 for d in s if d == c)

def walk(s,n):
    """
    Walk n steps along string.
    """
    R = {(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1)}
    L = {(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0),(1,0):(0,1)}
    x,y = 0,0
    dx,dy = 0,1
    istep = 0
    for c in s:
        if c == 'F':
            x,y = x+dx,y+dy
            istep += 1
        elif c == 'R':
            dx,dy = R[dx,dy]
        elif c == 'L':
            dx,dy = L[dx,dy]
        if istep == n:
            break
    return x,y

def compress(s,tonum=False):
    tr = {'A':0,'B':1,'C':2,'D':3}
    s = s.replace('FaRbFRRL','A') #FRFR
    s = s.replace('FaLbFRRL','B') #FLFR
    s = s.replace('FaRbFRLL','C') #FRFL
    s = s.replace('FaLbFRLL','D') #FLFL
    if tonum: return [tr[c] for c in s]
    return s

def limit(s,n=10):
    if len(s) > n: return s[:n]
    return s

def find_period(s):
    """
    Find the minimum period of a string of characters
    >>> find_period('AAAA')
    1
    >>> find_period('ABABABAB')
    2
    >>> find_period('ABCABC')
    3
    >>> find_period('ABCDABCDABCDABCE')
    0
    >>> find_period('ABCDABCDABCDABCD')
    4
    """
    n = len(s)
    for per in range(1,n/2+1):
        isper = True
        for i in range(1,n/per):
            for j in range(per):
                if s[j] != s[j+i*per]: isper = False
        if isper: return per
    return 0

def startsame(s1,s2):
    """
    Find the length that the two strings are the same at the start
    >>> startsame('a','abcdef')
    1
    >>> startsame('a','bcdef')
    0
    """
    n = min(len(s1),len(s2))
    for i in range(n):
        if s1[i] != s2[i]: return i
    return n

def heigh_iter(nmax=None):
    D = 'Fa'
    while True:
        yield D
        nchar = len(D)
        Dnew = update_string(D)
        D = subtract_from_start(Dnew,D)
    return

def subtract_from_start(s,subset):
    """\
    Subtract a subset from the start of s, assuming
    that s starts with subset
    >>> subtract_from_start('abcdefg','abc')
    'defg'

    If s doesn't start with subset, return None
    >>> subtract_from_start('abcdefg','abq')
    """
    if not s.startswith(subset):
        return None
    return s[len(subset):]

def main():
    D = 'Fa'
    Dincr = ''
    hi = heigh_iter()
    for i in range(4):
        Dincr += hi.next()
        print D,Dincr
        D = update_string(D)
        
    #walk(D,500) # gives (18,16)

    # No period found
    #print find_period(limit(compress(D),500))

    # Observation: Dn *always* starts with Dn-1.
    # However, this doesn't help me make a generator for only the next
    #  portion

    # Observation: 
    return

if __name__ == '__main__':
    import doctest; doctest.testmod()
    main()
    
    
