#!/usr/bin/env python
"Solve the traveling salesman problem using GA and SA"

from math import sqrt,pow
from random import random,randrange,choice

class Path:
    # This use of genetic algorithms to solve the traveling salesman
    #  problem comes from A.K. Dewdney's _New Turing Omnibus_
    # ncities - The number of cities in the search
    # gene    - The encoding of the path that can be varied
    # indices - The "normal" encoding of the path 
    def __init__(self,cities,gene=None):
        self.cities = cities
        self.ncities = len(cities)
        if gene:
            self.gene = gene
            assert len(gene) == self.ncities
        else:
            self.gene = [randrange(self.ncities-i) for i in range(self.ncities)]
        self.set_indices()
        self.calc_length()
        return

    def set_indices(self):
        cities = range(self.ncities)
        self.indices = [cities.pop(i) for i in self.gene]
        return

    def calc_length(self):
        length = 0
        x0,y0 = self.cities[self.indices[0]]
        for i in range(1,self.ncities):
            x,y = self.cities[self.indices[i]]
            length += sqrt(pow(x-x0,2)+pow(y-y0,2))
            x0,y0 = x,y
        x,y = self.cities[self.indices[0]]
        length += sqrt(pow(x-x0,2)+pow(y-y0,2))
        self.length = length
        return

    def __cmp__(self,other): return cmp(self.length,other.length)

def breed_step(paths,nbreed,breed_cutoff):
    if breed_cutoff > len(paths) or breed_cutoff == 0: breed_cutoff = len(paths)
    newpaths = []
    for i in range(nbreed):
        ipath = randrange(breed_cutoff)
        jpath = randrange(breed_cutoff)
        if ipath == jpath: continue
        igene = paths[ipath].gene
        jgene = paths[jpath].gene
        cities = paths[ipath].cities
        ncities = len(cities)
        crossover = randrange(ncities)
        newgene = igene[:crossover]+jgene[crossover:]
        newpath = Path(cities,newgene)
        newpaths.append(newpath)
    return newpaths

def mutate_step(paths,nmutate,mutate_prob = 0.20):
    newpaths = []
    for i in range(nmutate):
        item = randrange(len(paths))
        gene = paths[item].gene
        cities = paths[item].cities
        ncities = len(cities)
        for i in range(len(gene)):
            if random() < mutate_prob: gene[i] = randrange(ncities-i)
        newpaths.append(Path(cities,gene))
    return newpaths

def main():
    # Parameters:
    ncities = 100
    xmax=ymax=100 # boundaries for cities
    nsamples = 100
    nsteps = 1000
    
    cities = [(xmax*random(),ymax*random()) for i in range(ncities)]
    #print cities
    paths = [Path(cities) for i in range(nsamples)]
    paths.sort()
    print "Min, max lengths = ",paths[0].length, paths[-1].length
    
    for i in range(nsteps):
        new_paths = breed_step(paths,10,0)
        paths.extend(new_paths)
        new_paths = mutate_step(paths,10)
        paths.extend(new_paths)
        paths.sort()
        paths = paths[:nsamples]
        print i,"Min, max lengths = ",paths[0].length, paths[-1].length
    return        

if __name__ == '__main__': main()


    
        
