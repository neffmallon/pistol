#!/usr/bin/env python
"Playing with anagrams"

def sort(string):
    l = list(string)
    l.sort()
    return ''.join(l)

def getwordlist(fname):
    lines = open(fname).readlines()
    for i in range(len(lines)): lines[i] = lines[i].strip()
    return lines

def builddict():
    words = getwordlist('/usr/share/dict/words')
    propernames = getwordlist('/usr/share/dict/propernames')
    connectives = getwordlist('/usr/share/dict/connectives')
    print len(words),len(propernames),len(connectives)
    anags = {}
    for word in words:
        aword = sort(word)
        anags.setdefault(aword,[]).append(word)
        #for con in connectives:
        #    aword = sort(word+con)
        #    anags.setdefault(aword,[]).append('%s %s' % (con,word))
    return anags

if __name__ == '__main__':
    anags = builddict()
    aword = sort('tess pallozzi')
    if anags.has_key(aword): print anags[aword]
    


    
