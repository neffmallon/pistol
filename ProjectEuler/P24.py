"""
A permutation is an ordered arrangement of objects. For example, 3124
is one possible permutation of the digits 1, 2, 3 and 4. If all of the
permutations are listed numerically or alphabetically, we call it
lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2,
3, 4, 5, 6, 7, 8 and 9?
"""

perms = []
digs = []
for i in range(10): # 0
    digs.append(i)
    for j in range(10): # 1
        if j in digs: continue
        digs.append(j)
        for k in range(10): # 2
            if k in digs: continue
            digs.append(k)
            for l in range(10): # 3
                if l in digs: continue
                digs.append(l)
                for m in range(10): # 4
                    if m in digs: continue
                    digs.append(m)
                    for n in range(10): # 5
                        if n in digs: continue
                        digs.append(n)
                        for o in range(10): # 6
                            if o in digs: continue
                            digs.append(o)
                            for p in range(10): # 7
                                if p in digs: continue
                                digs.append(p)
                                for q in range(10): # 8
                                    if q in digs: continue
                                    digs.append(q)
                                    for r in range(10): # 9
                                        if r in digs: continue
                                        perms.append((i,j,k,l,m,n,o,p,q,r))
                                    digs.pop() # q (8)
                                digs.pop() # p (7)
                            digs.pop() # o (6)
                        digs.pop() # n (5)
                    digs.pop() # m
                digs.pop() # l
            digs.pop() # k
        digs.pop()  # j
    digs.pop() # i
print perms[999999],"".join(perms[999999])


