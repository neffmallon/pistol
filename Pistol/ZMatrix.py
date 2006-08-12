#!/usr/bin/env python

def z2c(zatoms):
    atoms = []
    for i in range(len(zatoms)):
        zatom = zatoms[i]
        if i == 1:
            atno = zatom[0]
            atoms.append((atno,(0,0,0)))
        elif i == 2:
            atno = zatom[0]
            dref = zatom[1]
            dist = zatom[2]
            atoms.append((atno,(dist,0,0)))
        elif i == 3:
            atno = zatom[0]
            dref = zatom[1]
            dist = zatom[2]
            aref = zatom[3]
            angl = zatom[4]
            # need to finish

            
