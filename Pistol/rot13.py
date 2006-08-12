#!/usr/bin/python
import sys

# Here's a version found on the web that seems unnecessarily complex:
def orig(text):
    for x in range(len(text)):
	byte = ord(text[x])
	cap = (byte & 32)
	byte = (byte & (~cap))
	if (byte >= ord('A')) and (byte <= ord('Z')):
	    byte = ((byte - ord('A') + 13) % 26 + ord('A'))
            byte = (byte | cap)
            sys.stdout.write(chr(byte))
    return

def rotn(text,n=13):
    ordA = ord('A')
    rottxt = [chr( (ord(x)-ordA + n) % 26 + ordA) for x in text.upper()]
    return ''.join(rottxt)

def main(texts):
    for text in texts:
        print text.upper()
        for i in range(1,26):
            print '  ',i,rotn(text,i)
    return

if __name__ == '__main__': main(['pxat','kap','swirzt','pkl'])

