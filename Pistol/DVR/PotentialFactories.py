def CoulombFactory(Z=1.0,L=0.0):
    def V(r):
        return -Z/r + 0.5*L*(L+1.0)/(r*r)
    return V

def HarmonicOscillatorFactory(k=1.0):
    def V(x):
        return 0.5*k*x*x
    return V

def SquareWellFactory(Depth=10.,L=5.0):
    def V(x):
        if abs(x)<L: return 0
        return Depth
    return V

