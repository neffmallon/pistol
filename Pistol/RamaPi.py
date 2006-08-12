#!/usr/bin/env python
"""\
From the Javascript web app by John Bohr (jnbohr@netscape.net):
                       n=infinity 
                     _____________ 
                     \ 
    1       sqrt(8)   \    (4n)! [ 1103 + 26390 n ] 
   ----  =  ------     \  -------------------------- 
    Pi       9801      /          4    4n 
                      /       (n!)  396 
                     /____________ 
                        n=0 
There are three main calculations in this Javascript program:
 - Taylor series for the square root of 8,
 - Ramanujan's series for 1/Pi,
 - Newton-Raphson method for the reciprocal.

"""

fact_cache = [1,1,2,6,24,120,720,5040]

def fact(n):
    if n < len(fact_cache): return fact_cache[n]
    return n*fact(n-1)

def rama(nsteps,prec=10):
    from gmpy import mpf
    pre = mpf('8',prec).sqrt()/mpf('9801',prec)
    sum = mpf('0',prec)
    for i in range(nsteps):
        num = fact(4*i)*(1103+26390*i)
        den = pow(fact(i),4)*pow(396,4*i)
        sum += mpf(num,prec)/mpf(den,prec)
    print mpf(1,prec)/(pre*sum)

if __name__ == '__main__':
    from gmpy import pi
    print pi(1000)
    rama(100,1000)

