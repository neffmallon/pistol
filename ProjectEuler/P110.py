#!/usr/bin/env python

def nsols(n):
    return sum(1 for x in range(n+1, n*2+1) if ((n*x) % (x-n)==0))

def main():
    f = 2*3*5*7*11*13
    for i in xrange(f,f*100,f):
        if nsols(i)>=10000:
            print i
            break
    return

if __name__ == '__main__': main()


