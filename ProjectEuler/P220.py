"""
Let D_(0) be the two-letter string 'Fa'. For n>=1, derive D_(n) from
D_(n-1) by the string-rewriting rules:

'a' -> 'aRbFR'
'b' -> 'LFaLb'

Thus, D_(0) = 'Fa', D_(1) = 'FaRbFR', D_(2) = 'FaRbFRRLFaLbFR', and so
on.

These strings can be interpreted as instructions to a computer
graphics program, with 'F' meaning 'draw forward one unit', 'L'
meaning 'turn left 90 degrees', 'R' meaning 'turn right 90 degrees',
and 'a' and 'b' being ignored. The initial position of the computer
cursor is (0,0), pointing up towards (0,1).

Then D_(n) is an exotic drawing known as the Heighway Dragon of order
n. For example, D_(10) is shown below; counting each 'F' as one step,
the highlighted spot at (18,16) is the position reached after 500
steps.
"""

def update_string(s):
    """
    Use the Heigway Dragon rules to update a string
    >>> update_string('Fa')
    'FaRbFR'
    >>> update_string('FaRbFR')
    'FaRbFRRLFaLbFR'
    """
    news = []
    for c in s:
        if c == 'a':
            news.append('aRbFR')
        elif c == 'b':
            news.append('LFaLb')
        else:
            news.append(c)
    return ''.join(news)

def count_occurrences(c,s):
    """
    Return the number of occurrances of character c in string s
    >>> count_occurrences('R','Rick')
    1
    """
    return sum(1 for d in s if d == c)

def walk(s,n):
    """
    Walk n steps along string.
    """
    R = {(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1)}
    L = {(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0),(1,0):(0,1)}
    x,y = 0,0
    dx,dy = 0,1
    istep = 0
    for c in s:
        if c == 'F':
            x,y = x+dx,y+dy
            istep += 1
        elif c == 'R':
            dx,dy = R[dx,dy]
        elif c == 'L':
            dx,dy = L[dx,dy]
        if istep == n:
            break
    return x,y

def main():
    import doctest; doctest.testmod()
    D = 'Fa'
    for i in range(10):
        D = update_string(D)
    print count_occurrences('F',D)
    print walk(D,500)
    # This all gives the results that the examples do. However,
    # I don't know how to generate D50, which will be 10**16 long.
    # I also don't know how to walk 10**12 steps along it.
    return

if __name__ == '__main__':
    main()
    
    
