#!/usr/bin/python
"""\
 scribe.py: Markov chain algorithm for generating text from 2 word prefixes

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import re

MaxGen = 10000
NonWord = "\n"

def GetDict(filenames):
    dict = {}
    numpat = re.compile('\d')
    for filename in filenames:
        file = open(filename)
        w1 = w2 = NonWord
        for line in file.readlines():
            for word in line.split():
                if numpat.search(word): continue
                if dict.has_key((w1,w2)):
                    dict[(w1,w2)].append(word)
                else:
                    dict[(w1,w2)] = [word]
                w1,w2 = w2,word
    return dict

def MakeChain(dict):
    from random import choice
    chain = ""
    w1 = w2 = NonWord
    for i in range(MaxGen):
        if dict.has_key((w1,w2)):
            word = choice(dict[(w1,w2)])
        else:
            break
        if word == NonWord: break
        chain = chain + " " + word
        w1,w2 = w2,word
    return chain

def main(filenames):
    dict = GetDict(filenames)
    chain = MakeChain(dict)
    print chain
    return

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

