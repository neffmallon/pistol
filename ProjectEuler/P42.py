"""
The nth term of the sequence of triangle numbers is given by, tn =
1/2 n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its
alphabetical position and adding these values we form a word value.
For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the
word value is a triangle number then we shall call the word a triangle
word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text
file containing nearly two-thousand common English words, how many are
triangle words?
"""

import string
from sets import Set

data = open("words.txt").read()
data = data.replace('"','')
words = data.split(",")

letters = string.uppercase

def num_to_digits(n): return map(int,str(n))

def tostring(n):
    digits = num_to_digits(n)
    return "".join([letters[i] for i in digits])

def wordindices(word):
    return [letters.index(w)+1 for w in word]

nmax=100000
tris = [n*(n+1)/2 for n in range(1,nmax+1)]
triset = Set(tris)

triwords = []
for word in words:
    dsum = sum(wordindices(word))
    if dsum in triset:
        triwords.append(word)
print len(triwords),triwords



