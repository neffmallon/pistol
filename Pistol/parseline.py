#!/usr/bin/env python

def parseline(line,format):
    """\
    Given a line (a string actually) and a short string telling
    how to format it, return a list of python objects that result:

    Basic parsing of strings:
    >>> parseline('Hello, World','ss')
    ['Hello,', 'World']

    You can use 'x' to skip a record; you also don't have to parse
    every record:
    >>> parseline('1 2 3 4','xdd')
    [2, 3]

    >>> parseline('C1   0.0  0.0 0.0','sfff')
    ['C1', 0.0, 0.0, 0.0]

    Should this return an empty list?
    >>> parseline('This line wont be parsed','xx')
    """
    xlat = {'x':None,'s':str,'f':float,'d':int,'i':int}
    result = []
    words = line.split()
    for i in range(len(format)):
        f = format[i]
        trans = xlat.get(f,None)
        if trans: result.append(trans(words[i]))
    if len(result) == 0: return None
    if len(result) == 1: return result[0]
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

