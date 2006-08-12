#!/usr/bin/env python
"Playing with factorials"

from math import sqrt,pi,e

# Often we need to take the factorials of small numbers over and over;
#  the cached values make this much faster.
fact_cache = [1,1,2,6,24,120,720,5040]

def fact(n):
    if n < len(fact_cache): return fact_cache[n]
    return n*fact(n-1)

def stirling(n): return sqrt(2*pi*n)*pow(n/e,n)

def plot_fact(n=6):
    from Gnuplot import Gnuplot,Data
    f = []
    s = []
    for i in range(n):
        f.append(fact(i))
        s.append(stirling(i))
    steps = range(len(s))
    d1 = Data(steps,f,title='Factorial',with='lines')
    d2 = Data(steps,s,title='Stirling',with='lines')
    g = Gnuplot()
    g.plot(d1,d2)
    raw_input('Press any key...')
    return
    

if __name__ == '__main__':
    plot_fact()

