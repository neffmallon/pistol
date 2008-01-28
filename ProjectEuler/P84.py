#!/usr/bin/env python

import random

names = ["GO","A1","CC1","A2","T1",   "R1","B1","CH1","B2","B3",
         "JAIL","C1","U1","C2","C3",  "R2","D1","CC2","D2","D3",
         "FP","E1","CH2","E2","E3",   "R3","F1","F2","U2","F3",
         "G2J","G1","G2","CC3","G3",  "R4","CH3","H1","T2","H2"]

# 40 = next RR
# 41 = next U
# 42 = go back 3

cc_cards = [0,10,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1]

ch_cards = [0,10,11,24, 39,5,40,40, 41,42,-1,-1, -1,-1,-1,-1]

next_rr = [5,5,5,5,5,      5,15,15,15,15,
           15,15,15,15,15, 15,25,25,25,25,
           25,25,25,25,25, 25,35,35,35,35,
           35,35,35,35,35, 35,5,5,5,5]

next_u = [12,12,12,12,12, 12,12,12,12,12,
          12,12,12,38,38, 38,38,38,38,38,
          38,38,38,38,38, 38,38,38,38,12,
          12,12,12,12,12, 12,12,12,12,12]


def cc(i):
    j = random.choice(cc_cards) 
    if j == -1: return i
    return j

def ch(i):
    j = random.choice(ch_cards)
    if j == -1: return i
    if j == 40: return next_rr[i]
    if j == 41: return next_u[i]
    if j == 42: return i-3
    return j

def is_ch(i): return i in [7,22,36]
def is_cc(i): return i in [2,17,33]
def is_g2j(i): return i == 30

def dice_roll(nsides):
    i = random.randrange(1,nsides+1)
    j = random.randrange(1,nsides+1)
    return i+j,i==j

def monopoly(nsteps=100,nsides=6,VERBOSE=False):
    probs = [0]*40
    square = 0
    rprobs = [0]*13
    double_count = 0
    for step in range(nsteps):
        if VERBOSE: print "============="
        if VERBOSE: print "On square ",names[square]
        roll,is_double = dice_roll(nsides)
        if VERBOSE: print "Rolled %d" % roll,
        if is_double:
            double_count += 1
            if VERBOSE: print " -- a double "
        else:
            double_count = 0
            if VERBOSE: print ""
        rprobs[roll] += 1
        square = (square + roll) % 40
        if VERBOSE: print "Landed on ",names[square]
        if double_count == 3 or is_g2j(square):
            square = 10
            double_count = 0
            if VERBOSE: print "Go to jail!"
        elif is_ch(square):
            square = ch(square)
            if VERBOSE: print "Chance! Now on ",names[square]
        elif is_cc(square):
            square = cc(square)
            if VERBOSE: print "Community Chest! Now on ",names[square]
        probs[square] += 1
    return probs

def highest_probs(probs):
    results = [(hits,step) for step,hits in enumerate(probs)]
    results.sort()
    return results

def main():
    probs = monopoly(1000000,4)
    results = highest_probs(probs)
    print results[-1:-4:-1]
    return

if __name__ == '__main__': main()

    



















