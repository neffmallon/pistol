"""
"""

from Utils import primes, xcombos

def ssub(s,pos):
    l = list(s)
    patmatch = True
    for i in pos:
        if l[i] != l[pos[0]]: patmatch = False
    if not patmatch: return ""
    for i in pos:
        l[i] = "*"
    return "".join(l)

ndigits = 6
ps = [p for p in primes(int(10**ndigits)) if p > int(10**(ndigits-1))-1]
nmatch = 3

patterns = xcombos(range(ndigits),nmatch)

# First find all of the ps
results = {}
for pt in patterns:
    for p in ps:
        starred = ssub(str(p),pt)
        if not starred: continue
        if starred in results:
            results[starred].append(p)
        else:
            results[starred] = [p]

for key in results:
    if len(results[key]) > 6:
        print key,results[key]

            

