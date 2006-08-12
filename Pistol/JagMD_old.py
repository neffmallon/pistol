#!/source/python/IRIX-5.3/bin/python
# JAGMD
# Rick Muller, 4/22/99
#
# This program will run molecular dynamics using Jaguar forces.
#
# Usage:
# python jagmd.py MOL
# where MOL is the name of the molecule to be run, from the MOL.in
# Jaguar input file.

# constants:
bohr2ang = 0.529177249  # Conversion of length from bohr to angstrom
ang2bohr = 1/bohr2ang
amu2me = 1822.882       # Conversion from mass in amu to mass in au (m_e)
me2amu = 1/amu2me       # Conversion from mass in au (m_e) to mass in amu 


class JagMD:
    def __init__(self,name):
        self.name = name
        self.atomlist = []
        self.vlist = []
        self.flist = []
        self.guesslist = []
        self.timestep = 10.0   # Corresponds to ~.25 fs
        self.nsteps = 200
        self.jaguar_input = name + '.in'
        self.jaguar_output = name + '.out'
        self.restart = name + '.01.in'
        self.monitor = name + '.md'
        self.xyz = name + '.xyz'
        self.pote = 0
        self.monfile = open(self.monitor,'w')
        self.xyzfile = open(self.xyz,'w')
        self.restartvxyz = name + '-restart.vxyz'

    def stop(self):
        self.prmon_end()
        self.monfile.close()
        self.xyzfile.close()
        self.writevxyz(self.restartvxyz)

    def readjagguess(self):
        # Read the &guess section of a jaguar restart file
        import string, Element, re

        filename = self.restart

        self.guesslist = []
        file = open(filename,'r')
        pat = re.compile('[\&\$]guess')
        pat2 = re.compile('[\&\$]')
        while(1):
            line = file.readline()
            if not line: break
            if pat.search(line): break
        self.guesslist.append(line)
        while(1):
            line = file.readline()
            if not line: break
            if pat2.search(line):
                break
            else:
                self.guesslist.append(line)
        file.close()

    def runjag(self):
        # Runs a jaguar job; returns status, if desired
        import os
        input = self.jaguar_input
        status = 0
        command = '/usr/local/bin/jaguar run -F -w ' +  input
        os.system(command)

    def nrunjag(self):
        # Just print out command that the program would run
        input = self.jaguar_input
        status = 0
        command = '/usr/local/bin/jaguar run -w ' +  input
        print command

    def update_atoms(self):
        import sys
        from Constants import *
        t = self.timestep
        for i in range(len(self.atomlist)):
            atom = self.atomlist[i]
            v = self.vlist[i]
            f = self.flist[i]
            xau = angstrom2bohr*atom.x
            yau = angstrom2bohr*atom.y
            zau = angstrom2bohr*atom.z
            mau = amu2me*atom.mass
            fx,fy,fz = f
            ax = fx/mau
            ay = fy/mau
            az = fz/mau
            vx,vy,vz = v
            vx = vx + t*ax
            vy = vy + t*ay
            vz = vz + t*az
            xau = xau + t*vx
            yau = yau + t*vy
            zau = zau + t*vz
            atom.x = xau*bohr2angstrom
            atom.y = yau*bohr2angstrom
            atom.z = zau*bohr2angstrom
            self.vlist[i] = (vx,vy,vz)


    def readvxyz(self,filename):
        import string
        from Element import *
        from Atom import *
        file = open(filename,'r')
        nat = int(string.split(file.readline())[0])
        file.readline()
        for i in range(nat):
            words = string.split(file.readline())
            sym = words[0]
            atno = sym2no[sym]
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            vx = float(words[4])
            vy = float(words[5])
            vz = float(words[6])
            atom = Atom(atno,x,y,z)
            self.atomlist.append(atom)
            self.vlist.append((vx,vy,vz))
        return

    def writevxyz(self,filename):
        import string
        from Element import *
        from Atom import *
        file = open(filename,'w')
        nat = len(self.atomlist)
        file.write('%d\nVXYZ file written by JAGMD\n' % nat)
        for i in range(nat):
            atom = self.atomlist[i]
            vel = self.vlist[i]
            x = atom.x
            y = atom.y
            z = atom.z
            sym = atom.symbol
            vx, vy, vz = vel
            file.write('%s %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f\n' % \
                       (sym,x,y,z,vx,vy,vz))
        file.close()
        return

    def readjagf(self):
        from JaguarOutput import *
        filename = self.jaguar_output
        inunit = JaguarOutput()
        inunit.rd(filename)
        self.atomlist = inunit.mol.atomlist
        self.flist = inunit.forces

    def writejagin(self):
        import Constants
        filename = self.jaguar_input
        file = open(filename,'w')
        file.write('&gen\n')
        file.write('idft=22111\n')
        file.write('igeopt=-1\n')
        file.write('isymm=0\n')
        file.write('ip11=2\n')
        file.write('maxit=148\n')
        file.write('ip192=2\n')
        file.write('&\n')
        file.write('&zmat\n')
        for atom in self.atomlist:
            atom.prxyz(file)
        file.write('&\n')
        if len(self.guesslist) > 0:
            for line in self.guesslist:
                file.write(line)
            file.write('&\n')
        file.close()

    def prmon_init(self):
        self.monfile.write('Jaguar MD Run\n')
        self.monfile.write('Molecule %s\n' % self.name)
        self.monfile.write('Input geometry\n')
        for atom in self.atomlist:
            atom.prxyz(self.monfile)
        self.monfile.write('Other run parameters:\n')
        self.monfile.write(' timestep %f \n' % self.timestep)
        self.monfile.write(' number of steps %d \n' % self.nsteps)
        self.monfile.write('\n')

    def prmon_update(self):
        #self.monfile.write('Potential energy: %f\n' % self.pote)
        #self.monfile.flush()
        return

    def prmon_end(self):
        self.monfile.write('Normal finish to MD run\n')
        self.monfile.write('Final geometry\n')
        for atom in self.atomlist:
            atom.prxyz(self.monfile)

    def prxyz(self):
        import Constants
        nat = len(self.atomlist)
        file = self.xyzfile
        file.write('%d\n' % nat)
        file.write(' XYZ file written by JAGMD\n')
        for i in range(nat):
            atom = self.atomlist[i]
            vx,vy,vz = self.vlist[i]
            file.write('%s %10.4f %10.4f %10.4f  %10.4f %10.4f %10.4f\n' %\
                       (atom.symbol, atom.x, atom.y, atom.z, vx,vy,vz))
        file.flush()

    def testv(self,teststring):
        import sys
        print 'Velocity Test ',teststring
        for i in range(len(self.atomlist)):
            atom = self.atomlist[i]
            vx,vy,vz = self.vlist[i]
            print atom.x,atom.y,atom.z,vx,vy,vz
        return


if __name__ == '__main__':
    import sys
    from Constants import *
    from XYZ import *

    name = sys.argv[1]
    
    jagmd = JagMD(name)
    
    jagmd.readvxyz(name + '.vxyz')
    
    # Write out the first Jaguar input file:
    jagmd.writejagin()
    jagmd.prmon_init()
    
    for step in range(jagmd.nsteps):
        jagmd.runjag()
        jagmd.readjagf()
        jagmd.update_atoms()
        jagmd.prxyz()
        jagmd.prmon_update()
        jagmd.readjagguess()
        jagmd.writejagin()

    jagmd.stop()
