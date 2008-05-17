def gcd(int a, int b):
    while b:
        a, b = b, a%b
    return a
