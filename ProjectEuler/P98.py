#!/usr/bin/env python
"""\
By replacing each of the letters in the word CARE with 1, 2, 9, and 6
respectively, we form a square number: 1296 = 36**2. What is
remarkable is that, by using the same digital substitutions, the
anagram, RACE, also forms a square number: 9216 = 96**2. We shall call
CARE (and RACE) a square anagram word pair and specify further that
leading zeroes are not permitted, neither may a different letter have
the same digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text
file containing nearly two-thousand common English words, find all the
square anagram word pairs (a palindromic word is NOT considered to be
an anagram of itself).

What is the largest square number formed by any member of such a pair?

"""

from doctest import testmod
from sets import Set
from Utils import isqrt

def getwords(fname="words.txt"):
    words = []
    for line in open(fname):
        words.extend(line.split(","))
    words2 = [word.replace('"','') for word in words]
    return words2

def strsort(word): return "".join(sorted(list(word)))

def getpalindromes(words):
    pdict = {}
    for word in words:
        key = strsort(word)
        pdict.setdefault(key,[]).append(word)
    return [vals for key,vals in pdict.items() if len(vals) > 1]

def longestword(palindromes):
    l = 0
    for ps in palindromes:
        for p in ps:
            l = max(l,len(p))
    return l

def psquares(nmax):
    squares = (i*i for i in range(1,nmax))
    strsquares = (str(i) for i in squares)
    return getpalindromes(strsquares)

def wordsoflength(n,lwords):
    """
    Given a list of lists of words that are palindromes (and thus
    are all the same length), return the list of lists of length n.
    >>> wordsoflength(1,[['a']])
    [['a']]
    >>> wordsoflength(1,[['a'],['1'],['a','b']])
    [['a'], ['1'], ['a', 'b']]
    >>> wordsoflength(2,[['a'],['1'],['a','b']])
    []
    """
    return [l for l in lwords if len(l[0]) == n]

def maketranslation(a,b):
    """\
    Define a translation table that will map a -> b:
    >>> maketranslation('car','rat')
    {'a': 'a', 'c': 'r', 'r': 't'}
    """
    assert len(a) == len(b),"len(%s) != len(%s) " % (a,b)
    trans = {}
    for i in range(len(a)):
        if b[i] in trans.values(): return None
        trans[a[i]] = b[i]
    return trans

def applytranslation(a,trans):
    """\
    Given a translation table *trans* that maps a->b, return b.
    >>> applytranslation('car',{'a': 'a', 'c': 'r', 'r': 't'})
    'rat'
    """
    return "".join(trans[ai] for ai in a)

def find_psquare_pairs(a,b,psqs):
    """
    Given two palindromes a + b, see whether there are any mappings
    that map both a and b onto squares
    """
    assert len(a) == len(b)
    assert strsort(a) == strsort(b)
    selsquares = wordsoflength(len(a),psqs)
    s = Set()
    for lsqs in selsquares:
        for sq in lsqs:
            trans = maketranslation(a,sq)
            if not trans: continue
            test = applytranslation(b,trans)
            if test in lsqs:
                print a,b,sq,test
                s.add(int(sq))
                s.add(int(test))
    return s

def pairs(l):
    "Generate unique pairs from a list l"
    for i in xrange(len(l)):
        for j in xrange(i):
            yield l[i],l[j]
    return

def main():
    testmod()
    words = getwords()
    palindromes = getpalindromes(words)
    nchar = longestword(palindromes)
    print "Longest word is %d characters" % nchar
    psqs = psquares(100000)

    res = Set()
    #for lwords in wordsoflength(3,palindromes):
    for lwords in palindromes:
        for a,b in pairs(lwords):
            s = find_psquare_pairs(a,b,psqs)
            if s:
                res = res | s
    print sorted(res)
    
            
        
if __name__ == '__main__': main()




