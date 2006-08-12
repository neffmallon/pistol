import sys
from code import InteractiveInterpreter

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = ''.join(self.out)
        self.reset()
        return output

class Interp(InteractiveInterpreter):
    def __init__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.out_cache = FileCacher()
        self.err_cache = FileCacher()
        InteractiveInterpreter.__init__(self)
        return

    def get_output(self):
        sys.stdout = self.out_cache
        sys.stderr = self.err_cache
        return
    
    def return_output(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return

    def runsource(self,source):
        self.get_output()
        more = InteractiveInterpreter.runsource(self,source)
        self.return_output()
        output = self.out_cache.flush()
        errors = self.err_cache.flush()
        return more,errors,output

def simple_shell():
    interp = Interp()
    try:
        ps1 = sys.ps1
        ps2 = sys.ps2
    except:
        ps1 = '>>> '
        ps2 = '... '

    more = False
    while 1:
        if more:
            prompt = ps2
        else:
            prompt = ps1
        line = raw_input(prompt)
        more, output, errors = interp.runsource(line)
        if errors: print errors,
        print output,
    return

if __name__ == '__main__': simple_shell()
