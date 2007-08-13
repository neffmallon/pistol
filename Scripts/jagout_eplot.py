#!/usr/bin/env python

import sys
from pylab import plot,title,xlabel,show,ylabel

def main(fname):
    energies = []
    for line in open(fname):
        #if line.startswith(' SCFE: SC'):
        if line.startswith('etot'):
            words = line.split()
            energies.append(float(words[6]))
    plot(energies,'b-')
    title("Energies from Jaguar file %s" % fname)
    xlabel("Step")
    ylabel("Energy (h)")
    show()
    return

if __name__ == '__main__':
    for fname in sys.argv[1:]:
        main(fname)
