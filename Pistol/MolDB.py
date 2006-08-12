#!/usr/bin/env python
"""\
NAME
      MolDB.py - Persistant storage of molecular data

DESCRIPTION
      MolDB.py stores molecular information in python dictionaries.
      Perisistance is achieved through pickling to a file.

      Each entry is stored as a dictionary record using a molecule's
      name as the key:
      
      record = MolDB[name] 

      Each record has two required keys, 'structure' and 'energy'.

      energy = record['energy']    # Energy in arbitrary units
      atoms = record['structure']  # List of (atno,(x,y,z)) tuples

      Other records are optional, but are suggested to explain what
      is in the record:

      record['frequencies'] = [0.002, 25, 30., 35.]
      record['energy_units'] = 'Hartrees'

      The nooverwrite flag (given as an optional second argument to
      the constructor) triggers whether new records overwrite old
      ones with the same name, or whether they are given new unique names.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os.path

class MolDB:
    def __init__(self,filename='mol_db.pkl',nooverwrite=0):
        self.filename = os.path.expanduser(filename)
        self.dict = dload(self.filename)
        self.nooverwrite=nooverwrite
        return

    def __del__(self): ddump(self.filename,self.dict)
    def __getitem__(self,key): return self.dict[key]
    def keys(self): return self.dict.keys()
    def items(self): return self.dict.items()
    def delete(self,key): del self.dict[key]
    def clear(self): self.dict.clear()

    def __setitem__(self,key,value):
        if self.nooverwrite and self.dict.has_key(key):
            key = self.get_unique_key(key)
        if not value.has_key('structure') or\
           not value.has_key('energy'):
            print "Warning: records should have energies and structures"
        self.dict[key] = value
        return

    def __str__(self): return str(self.dict)

    def get_unique_key(self,key):
        for i in range(1,100):
            newkey = '%s.%02d' % (key,i)
            if not self.dict.has_key(newkey): return newkey
        raise "Can't find unique key for %s" % key

def dload(filename): 
    "Load a dictionary from a pickled file" 
    from pickle import load
    if os.path.exists(filename):
        file = open(filename,'r')
        data = load(file)
        file.close()
    else: data = {}
    return data

def ddump(filename,data):
    "Dump a dictionary to a picked file"
    from pickle import dump
    file = open(filename,'w')
    dump(data,file)
    file.close()
    return

if __name__ == '__main__':
    moldb = MolDB()
    moldb['null'] = {'sequence' : [], 'energy' : 0}
    moldb.clear()
    print moldb

