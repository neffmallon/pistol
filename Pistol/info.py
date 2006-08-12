#!/usr/bin/env python
"Playing with information theory"

from math import log
from random import choice

log_2 = log(2)
def log2(x): return log(x)/log_2

# Shannon information contents of the letters a-z in English
#  From Mackay table 2.9
letter_probs = {'a':.0575, 'b':.0128, 'c':.0263, 'd':.0285, 'e':.0913,
                'f':.0173, 'g':.0133, 'h':.0313, 'i':.0599, 'j':.0006,
                'k':.0084, 'l':.0335, 'm':.0235, 'n':.0596, 'o':.0689,
                'p':.0192, 'q':.0008, 'r':.0508, 's':.0567, 't':.0706,
                'u':.0334, 'v':.0069, 'w':.0119, 'x':.0073, 'y':.0164,
                'z':.0007, ' ':.1928}
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
           'p','q','r','s','t','u','v','w','x','y','z',' ']

def shannon_info_content(sequence,probs):
    sic = 0
    for item in sequence: sic += probs[item]*log2(1/probs[item])
    return sic

def digits_to_list(a):
    stra = str(abs(a)).replace('.','') # make a string and remove decimal
    return map(int,list(stra))

def test_pi():
    from gmpy import pi # import the Gnu Multiprecision library pi function
    val = pi(1000000) # ~300,000 digits of pi
    digpi = digits_to_list(val)

def test_letters():
    # Random sequence
    #seq = []
    #for i in range(1000): seq.append(choice(letters))
    #seq = [' ']*1000
    seq = list('once upon a midnight dreary while i pondered weak '+
               'and weary over a many quaint and curious volume of '+
               'forgotten lore while i nodded nearly napping suddenly '+
               'i heard a tapping as if someone was gently rapping '+
               'rapping at my chamber door this it is and nothing more '+
               'ah distinctly i remember it was in the bleak december and '+
               'each separate dying ember wrought its ghost upon the floor '+
               'eagerly i wished the morrow vainly i had sought to borrow '+
               'from my books surcease of sorrow sorrow for the lost lenore '+
               'nameless here forever more')
              
    print shannon_info_content(seq,letter_probs)/len(seq)

if __name__ == '__main__': test_letters()

