#!/usr/bin/env python
"Return a quoted list, like the perl qq function"

def qlist(**args): return args.keys()
def qlist2(*args): return args

def test():
    print qlist(a=0,b=0,c=0)

if __name__ == '__main__': test()

