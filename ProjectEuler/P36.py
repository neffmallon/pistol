"""
The decimal number, 585 = 10010010012 (binary), is palindromic in both
bases.

Find the sum of all numbers, less than one million, which are
palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not
include leading zeros.)
"""

def Denary2Binary(n):
    '''convert denary integer n to binary string bStr'''
    bStr = ''
    if n < 0: raise ValueError, "must be a positive integer"
    if n == 0: return '0'
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    return bStr

def is_palindrome_list(l):
    """
    >>> is_palindrome_list([1,2,3,4])
    False
    >>> is_palindrome_list([1,2,3,2,1])
    True
    >>> is_palindrome_list('madam')
    True
    >>> is_palindrome_list('madame')
    False
    """
    n = len(l)
    for i in range(n/2):
        if l[i] != l[-(i+1)]:
            return False
    return True

vals = []
for i in range(1000000):
    if is_palindrome_list(str(i)):
        bstr = Denary2Binary(i)
        if is_palindrome_list(bstr):
            vals.append(i)
print vals,sum(vals)





