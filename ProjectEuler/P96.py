#!/usr/bin/env python
"""\
"""

from sudoku import Sudoku

puzzle1 = """\
003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300"""

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
    for i in range(len(puzzles)):
        puz = Sudoku(puzzles[i])
        print puz
        puz.solve()
        key =  100*puz.cell(1,1)+10*puz.cell(1,2)+puz.cell(1,3)
        print i,key
        sumkey += key
    print sumkey

if __name__ == '__main__': main()
