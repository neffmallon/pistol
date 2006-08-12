#!/usr/bin/env python

import sys
from code import InteractiveConsole

class Shell(InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        InteractiveConsole.__init__(self)
        return

# I was hoping that this would allow me to capture the output before
#  it went back to the screen, but it didn't work.
#class Console(InteractiveConsole):
#    def write(self,data):
#        print "Hi Rick!",data
#        InteractiveConsole.write(self,data)
#        return

def myshell():
    shell = InteractiveConsole()
    try:
        while 1:
            line = shell.raw_input(ps1)
            while 1:
                result = shell.push(line)
                if not result: break
                line = shell.raw_input(ps2)
    except:
        pass
    return
    def get_output(self): sys.stdout = self.cache
    def return_output(self): sys.stdout = self.stdout

    def push(self,line):
        self.get_output()
        # you can filter input here by doing something like
        # line = filter(line)
        InteractiveConsole.push(self,line)
        self.return_output()
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        print output # or do something else with it
        return 

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output

if __name__ == '__main__':
    sh = myshell()
    sh.interact()

