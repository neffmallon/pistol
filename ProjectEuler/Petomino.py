"""\
Not part of Project Euler, but a Pentomino code from the
book Chasing Vermeer.
"""

key = {"F":"AMY","I":"BNZ","L":"CO","N":"DP","P":"EQ","T":"FR",
       "U":"GS","V":"HT","W":"IU","X":"JV","Y":"KW","Z":"LX"}

letter1 = """\
L1 F1 Z1 N1 P1 T2
I2 F1 F2 P1
L2 T1
Y1 W1 N1
I2 P1 Z2 V2
N1 L2 L2 T2
W1 U2
T1 T2 L2 U1
X2 F1 I2 W1 U2 V1 P1 N1
Z1 F1 U2 V2
Y2 P1 P1 Y1
W1
V2 V1 W1 I2 Y1
Y1 W1 N1 I2 F1 N2 N2 P1 N1
V1 F1 X2 P1
V2 L2
U2 V2 F1 F3
W1 I2 U2 W1 N1 P1
F2 L2 F2
F1 T1 T2 F1 W1 N1
I2 P1 Y2
F3 L2 T2 Y1
U2 V2 W1 I2 Y1 U2
V2 L2 F2 F2 F3
"""

letter2 = """\
V2 L2 F2 F2 F3
U2 L2
U2 L2 T2 T2 F3
F1 I1 L2 W2 V2
T1 T2 L2 U1
F2 F1 F3 I1 P1
F3 L2 W2
L1 F1 I2
U2 L2 Z1 X2 P1
F2 F3 U2 V2 P1 T2 F3
F1 I2 N1
I1 P1
V1 P1 T2 L2
I1 P1
L1 F1 T2 P1 T1 W2 Z1
L1 F1 Z1 N1 P1 T2
"""

letter3="""\
L1 F1 Z1 N1 P1 T2
T1 T2 P1 N1
L1 F1 W2 U1 V1 V2
F2 P1
Z1 L2 L2 Y1 W1 I2 U1
T1 L2 T2
L1 Z1 W2 P1 U2
L2 I2
T1 T2 L2 U1
U1 L2 V2
F2 P1 F1 I2
V2 L2 L2 Y1
F2 F3
I1 W1 Y1 P1
F2 L2 F2
F1 I2 N1
T1 T2 P1 N1
T1 W1 U1 V1 V2 W1 I2 U1
"""

letter4="""\
L1 F1 Z1 N1 P1 T2
T1 T2 P1 N1
F2 L2 X2 P1 N1
L2 W2 V2
Y2 P1
Y2 F1 I2 V2
V2 L2
L1 L2 F2 P1
V1 L2 F2 P1
I1 W2 V2
I2 L2
F2 L2 I2 P1 F3
"""

def decode(line):
    res = []
    for letter in line.split():
        l,n = letter[0:2]
        n = int(n)
        v = key[l]
        #print letter,l,n,list(v),n-1,list(v)[n-1]
        res.append(list(v)[n-1])
    return "".join(res)

def decode_letter(l):
    res = []
    for word in l.splitlines():
        res.append(decode(word))
    return " ".join(res)

from sets import Set
plets = key.keys()
plets = Set(v.lower() for v in plets)

def is_pentomino(word):
    for l in word:
        l = l.lower()
        if l not in plets:
            return False
    return True

print decode_letter(letter4)

#from Utils import get_wordgen
#for word in get_wordgen():
#    if is_pentomino(word): print word


