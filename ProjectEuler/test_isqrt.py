def isqrt(n):
    xn = 1
    xn1 = (xn + n/xn)/2
    while abs(xn1 - xn) > 1:
        xn = xn1
        xn1 = (xn + n/xn)/2
    while xn1*xn1 > n:
        xn1 -= 1
    return xn1

def is_square(n): return isqrt(n)**2 == n

for i in range(1,33):
    print i,is_square(i)
