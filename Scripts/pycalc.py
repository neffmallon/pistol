#!/usr/bin/env python

from operator import add,sub,mul,truediv,floordiv,pow,abs
from math import sin,cos,tan,exp,sqrt

def spop(stack,default=0):
    "Safe pop: returns a default value when popping from an empty list"
    try:
        a = stack.pop()
        return a
    except:
        pass
    return default
        
def main():
    stack = []
    binary_commands = {'+':add,
                       "-":sub,
                       "*":mul,
                       "/":truediv,
                       "^":pow}
    unary_commands = {"abs":abs,
                      "sin":sin,
                      "cos":cos,
                      "tan":tan,
                      "exp":exp,
                      "sqrt":sqrt}
    while 1:
        for i in stack: print i
        inp = raw_input("\ ").strip()
        if inp.lower().startswith('q'):
            break
        elif inp in unary_commands:
            a = spop(stack)
            stack.append(unary_commands[inp](a))
        elif inp in binary_commands:
            b = spop(stack)
            a = spop(stack)
            stack.append(binary_commands[inp](a,b))
        else:
            try:
                stack.append(float(inp))
            except:
                pass
    return

if __name__ == '__main__': main()

        
        
