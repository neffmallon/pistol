#!/usr/bin/env python
"""\
"""

def parse_test():
    data = []
    for line in puzzle1.splitlines():
        data.extend(map(int,list(line)))
    return data

def parse(fname):
    puzzles = []
    f = open(fname)
    while True:
        puzzle = []
        puzzles.append(puzzle)
        title = f.readline()
        if not title: break
        for i in range(9):
            line = f.readline()
            line = line.strip()
            puzzle.extend(map(int,list(line)))
    return puzzles

def main():
    puzzles = parse('sudoku.txt')
    sumkey = 0
    for i in range(50):
        puz = sudoku(Matrix(ZZ,9,puzzles[i]))
        key =  100*puz[0,0]+10*puz[0,1]+puz[0,2]
        sumkey += key
        print i,key,sumkey
    print sumkey

if __name__ == '__main__': main()
