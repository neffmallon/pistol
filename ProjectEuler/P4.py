"""
A palindromic number reads the same both ways. The largest palindrome
made from the product of two 2-digit numbers is 9009 = 91 99.

Find the largest palindrome made from the product of two 3-digit
numbers.
"""

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

def to_intlist(i):
    """
    >>> to_intlist(123)
    [1, 2, 3]
    >>> to_intlist(1234)
    [1, 2, 3, 4]
    """
    return [int(si) for si in str(i)]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    vals = []
    for i in range(700,1000):
        for j in range(i+1,1000):
            ij = i*j
            if is_palindrome_list(to_intlist(ij)):
                print i,j,ij
                vals.append(ij)
    vals.sort()
    print vals

    


