from gmpy import *

def pi_simple(npts=100):
    hits = mpz(0)
    for i in range(npts):
        x,y = rand('floa'),rand('floa')
        if x*x+y*y < 1: hits += 1
    return mpf(mpq(4*hits,npts))

def pi_rama(npts=100,prec=100):
    pre = mpf(8,prec).sqrt() / mpf(9801,prec)
    sum = mpq(0)
    c1103 = mpz(1103)
    c26390 = mpz(26390)
    c396 = mpz(396)
    for i in range(npts):
        num = fac(4*i)*(c1103+c26390*i)
        denom = pow(fac(i),4)*pow(c396,4*i)
        sum += mpq(num,denom)
    return mpf(mpq(mpz(1),pre*sum),prec)

def gmpy_e(npts=100, prec=1000):
    e = mpq(1)
    for i in range(1,npts): e += mpq(1,fac(i))
    return mpf(e,prec)
                 

def main():
    print pi(1000)
    print pi_simple(1000)
    print pi_rama(100,1000)
    print gmpy_e()
    return

if __name__ == '__main__': main()
