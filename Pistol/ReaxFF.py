#!/usr/bin/env python
"""\
 Wrapper to simplify running ReaxFF

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,os,glob,shutil

reax = '/home/rmuller/Programs/ReaxFF/src/reac'

reax_control_keys = [ # defines the order the keys are in the control file
    'itrans', 'imetho', 'igeofo', 'axis1', 'axis2', 'axis3', 'cutof2',
    'cutof3', 'icharg', 'ichaen', 'iappen',  'isurpr',
    'irecon', 'icheck', 'idebug', 'ixmolo', 'volcha',
    'iconne', 'imolde', 'imdmet', 'tstep', 'mdtemp', 'mdtem2',
    'tincr', 'itdmet', 'tdamp1', 'tdamp2', 'ntdamp',  'mdpres', 
    'pdamp1', 'inpt', 'nmdit',  'nmdeqi',  'ichupd',  'iout1',  'iout2', 
    'ivels',  'itrafr',  'iout3',  'iravel',  'endmd',  'iout6',  'irten', 
    'npreit',  'range',  'endmm',  'imaxmo',  'imaxit',  'iout4',  'iout5', 
    'celopt',  'icelo2',  'parsca',  'parext', 'icelop',  'igeopt',
    'iincop',  'accerr',
    'nmoset', 'ideve1',  'ideve2',  'nreac',  'ibiola',  'tdhoov',  'achoov', 
    'itfix' ]

reax_control_defaults = {
    # General flags
    'itrans' : 2,     # New flag, I don't know what it is
    'imetho' : 0 ,    # 0: MD 1: Mminimization 2:MD minimization
    # Changed the default to use xyz formatted files
    'igeofo' : 2,     # 0:xyz-input, 1: Biograf input 2: xmol-input geometry
    'axis1' : 200.0 , # a (for non-periodical systems)
    'axis2' : 200.0 , # b (for non-periodical systems)
    'axis3' : 200.0 , # c (for non-periodical systems)
    'cutof2' : 0.001, # BO-cutoff for valency angles and torsion angles
    'cutof3' : 0.300, # BO-cutoff for bond order for graphs
    'icharg' :3,      # Charges. 1:EEM 2:- 3: Shielded EEM 4: Full system EEM
                      # 5: Fixed (unit 26) 6: Fragment EEM
    'ichaen' : 1,     # 1:include charge energy 0: Do not include charge energy
    'iappen' : 0,     # 1: Append fort.7 and fort.8
    'isurpr' : 0,     # 1: Surpress lots of output
                      # 2: Read in all geometries at the same time
    'irecon' : 25,    # Frequency of reading control-file
    'icheck' : 0,     # 0: Normal run 1:Check first derivatives;2: Single run
    'idebug' : 0,     # 0: normal run 1: debug run
    'ixmolo' : 0,     # 0: only x,y,z-coordinates in xmolout
                      # 1: x,y,z + velocities + molnr. in xmolout
    # MD parameters
    'volcha' : 10.00, # volume change (%) with 'S' and 'B' labels
    'iconne' : 0,     # 0: normal, 1: Fixed connection table,
                      #  2: input from cnt.in
    'imolde' : 0,     # 0: normal, 2: fixed molecule def (moldef.in)
    'imdmet' : 3,     # MD-method. 1:VVerlet+Berendsen 2:Hoover-Nose;3:NVE 4: NPT
    'tstep' : 0.5,    # MD-time step (fs)
    'mdtemp' : 298.0, # MD-temperature
    'mdtem2' :  5.0,  # Second MD temperature
    'tincr' : 0.0,    # Increase/decrease temperature
    'itdmet' :  2,    # 0: T-damp atoms 1: Energy cons 2:System 3: Mols
                      # 4: Anderson 5: Mols+2 types of damping
    'tdamp1' : 2.5 ,  # 1st Berendsen/Anderson temperature damping constant (fs)
    'tdamp2' : 2.5 ,  # 2nd Berendsen/Anderson temperature damping constant (fs)
    'ntdamp' : 192,   # Number of atoms with 1st Berendsen damping constant 
    'mdpres' : 0.0 ,  # MD-pressure (MPa)
    'pdamp1' : 500.0, # Berendsen pressure damping constant (fs)
    'inpt' : 0,       # 0: Change all cell parameters in NPT-run
                      # 1: fixed x 2: fixed y 3: fixed z
    'nmdit' : 1000,   # Number of MD-iterations
    'nmdeqi' : 0 ,    # Number of MD-equilibrium iterations
    'ichupd' : 1,     # Charge update frequency
    'iout1' : 5,      # Output to unit 71 and unit 73
    'iout2' : 50,     # Save coordinates
    'ivels' : 0,      # 1:Set vels and accels from moldyn.vel to zero
    'itrafr' : 25,    # Frequency of trarot-calls
    'iout3' : 1,      # 0: create moldyn.xxxx-files
                      # 1: do not create moldyn.xxxx-files
    'iravel' :  0,    # 1: Random initial velocities
    'endmd' : 1.0 ,   # End point criterium for MD energy minimisation
    'iout6' : 1000,   # Save velocity file
    'irten' : 25,     # Frequency of removal of rot. and trans. energy
    'npreit' : 0 ,    # Nr. of iterations in previous runs
    'range' : 2.5,    # Range for back-translation of atoms

    # MM parameters
    'endmm' : 1.0,    # End point criterium for MM energy minimisation
    'imaxmo' : 50,    # Maximum movement (1/1D6 A) during minimisation
    'imaxit' : 50,    #  Maximum number of iterations
    'iout4' : 50,     #  Frequency of structure output during minimisation
    'iout5' : 0,      # 1:Remove fort.57 and fort.58 files
    'celopt' : 1.0005,# Cell parameter change
    'icelo2' : 0,     # Change all cell parameters (0) or only x/y/z axis (1/2/3)

    # FF optimization parameters
    'parsca' : 1.00,  # Parameter optimization: parameter step scaling
    'parext' : 0.001, # Parameter optimization: extrapolation
    'icelop' : 0,     # 0: No cell optimisation 1:Cell optimisation
    'igeopt' : 0,     # 0: Always use same start geometries 1:Overwrite old files
    'iincop' : 0,     # heat increment optimisation 1: yes 0: no
    'accerr' : 2.50,  # Accepted increase in error force field
    'nmoset' : 5,     # Nr. of molecules in training set

    # Outdated parameters
    'ideve1' : 0,     # 0: Normal run 1:Check for radical/double bond distances
    'ideve2' : 20000, # Frequency of radical/double bond check
    'nreac' : 0,      # 0: reactive; 1: non-reactive; 2: Place default atoms
    'ibiola' : 0,     # 0: Use old Biograf-labels 1: Assign Biograf-labels
    'tdhoov' : 100.0, # Hoover-Noose temperature damping constant (fs)
    'achoov'  : 1.0 , # 100*Accuracy Hoover-Noose
    'itfix' : 0       # 1:Keep temperature fixed at exactly tset
    }

def parse_control(filename):
    "Parse a ReaxFF control file to extract the keywords. Not used"
    vals = {}
    for line in open(filename):
        if line[0] == '#': continue
        # Here's the python way...
        #words = line.split()
        #val = eval(words[0])
        #key = words[1]
        # Do this the same way Adri's fortran does it:
        val = eval(line[:8])
        key = line[8:14].strip()
        vals[key] = val
    return vals

def write_flag(flag,value):
    "Format a key,value pair properly for a reaxff control file"
    if type(value) == type(1):
        return '%7d %-6s\n' % (value,flag)
    elif type(value) == type(1.0):
        if abs(value) > 1:
            return '%7.2f %-6s\n' % (value,flag)
        else:
            return '%7.5f %-6s\n' % (value,flag)
            
    raise "Invalid value"

def write_control(filename, **properties):
    "Write a ReaxFF Control File"
    out = []
    for key in reax_control_keys:
        if properties.has_key(key):
            out.append(write_flag(key,properties[key]))
        elif reax_control_defaults.has_key(key):
            out.append(write_flag(key,reax_control_defaults[key]))
        else:
            raise "Flag %s has an unknown value" % key
    open(filename,'w').writelines(out)
    return

def run(geoname, **properties):
    for unit in [83,4,41,91,59,58,57,71,72,73,74,76,13,99,79,7,8,81,87]:
        if os.path.exists('fort.%d' % unit):
            os.rename('fort.%d' % unit, 'save.%d' % unit)
        for file in ['xmolout','moldyn.vel', 'end.geo'] \
            + glob.glob('fort.*') + glob.glob('moldyn.0*') \
            + glob.glob('molsav.0*'):
            if os.path.exists(file): os.unlink(file)
        
        write_control('control',**properties)
        shutil.copyfile(geoname,'geo')
        shutil.copyfile('geo','fort.3')
        if os.path.exists('ffield'):
            shutil.copyfile('ffield','fort.4')
        else:
            raise "Missing ffield"

        if os.path.exists('ranfile'):
            shutil.copyfile('ranfile','fort.35')
        else:
            print "Created ranfile in unit 35"
            open('fort.35','w').write('234535.1\n')

        if os.path.exists('iopt'):
            shutil.copyfile('iopt','fort.20')
        else:
            print "Created iopt in unit 20: assume normal run"
            open('fort.20','w').write('  0   0: Normal run   '
                                      '1: Force field optimization')

        if os.path.exists('outres'):
            shutil.copyfile('outres','fort.9')
        else:
            print "Touched unit 9 (outres)"
            open('fort.9','w').write('\n')

        if os.path.exists('inilp'): shutil.copyfile('inilp', 'fort.2')
        if os.path.exists('params'): shutil.copyfile('params', 'fort.21')
        if os.path.exists('koppel'): shutil.copyfile('koppel', 'fort.22')
        if os.path.exists('koppel2'): shutil.copyfile('koppel2', 'fort.23')
        if os.path.exists('tregime'): shutil.copyfile('tregime', 'fort.19')
        if os.path.exists('restraint'): shutil.copyfile('restraint', 'fort.18')
        if os.path.exists('restraintt'): shutil.copyfile('restraintt', 'fort.28')
        if os.path.exists('restraintv'): shutil.copyfile('restraintv', 'fort.38')
        if os.path.exists('vels'): shutil.copyfile('vels', 'moldyn.vel')

        os.system('%s > run.log' % reax)
        return


