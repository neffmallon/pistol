#!/usr/bin/python

# Author: Remy Oukaour (Rangi42): remy dot oukaour at gmail dot com
# Date: 2007-10-08

# See techniques at http://www.sadmansoftware.com/sudoku/techniques.htm
# See the 17-hint ones at http://people.csse.uwa.edu.au/gordon/sudokumin.php

def test17():
	from urllib import urlopen
	boards = urlopen("http://people.csse.uwa.edu.au/gordon/sudoku17")
	board = boards.readline().strip()
	while board:
		S = Sudoku(board)
		try:
			S.solve()
			print "Sudoku('" + "".join(map(str, Sudoku.flatten(S.cells))) + "')"
		except:
			print "       " + repr(board)
		board = boards.readline().strip()

class Sudoku:
	
	@staticmethod
	def flatten(L):
		return sum(L, [])
	
	def __init__(self, *cells):
		# Accepts 81 ints, 9 sequences of 9 ints, 1 sequence of 81 ints,
		# or 1 sequence of 9 sequences of 9 ints. Sequences can be strs,
		# lists, or tuples; ints must be between 0 and 9.
		if len(cells) == 1:
			cells = list(cells[0])
		if len(cells) == 9:
			cells = Sudoku.flatten(map(list, cells))
		if len(cells) != 81:
			raise ValueError, "Invalid Sudoku board"
		cells, self.cells = list(cells), []
		while cells:
			self.cells += [map(int, cells[:9])]
			cells = cells[9:]
		if not self.check():
			raise ValueError, "Invalid Sudoku board"
	
	def __str__(self):
		s = "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "------+-------+------\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "------+-------+------\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s\n" + \
		    "%s %s %s | %s %s %s | %s %s %s"
		return s % tuple([str(n or " ")
			for n in Sudoku.flatten(self.cells)])
	
	def __repr__(self):
		return "Sudoku(" + str(Sudoku.flatten(self.cells)) + ")"
	
	def copy(self):
		return Sudoku(self.cells)
	
	def set_cell(self, x, y, value):
		if value not in range(10):
			raise ValueError, "Invalid Sudoku cell"
		self.cells[x-1][y-1] = value
	
	def row(self, n):
		return self.cells[n-1]
	
	def col(self, n):
		return [x[n-1] for x in self.cells]
	
	def block(self, x, y):
		segments = [self.cells[3*x-n][3*y-3:3*y] for n in range(3, 0, -1)]
		return Sudoku.flatten(segments)
	
	def cell_block(self, x, y):
		return self.block((x-1)/3+1, (y-1)/3+1)
	
	def cell(self, x, y):
		return self.cells[x-1][y-1]
	
	def check_cell(self, x, y):
		row = filter(None, self.row(x))
		col = filter(None, self.col(y))
		block = filter(None, self.cell_block(x, y))
		cell = self.cell(x, y)
		row_good = map(row.count, row) == [1] * len(row)
		col_good = map(col.count, col) == [1] * len(col)
		block_good = map(block.count, block) == [1] * len(block)
		cell_good = cell in range(10)
		return row_good and col_good and block_good and cell_good
	
	def check(self):
		for x in range(1, 10):
			for y in range(1, 10):
				if not self.check_cell(x, y):
					return False
		return True
	
	def candidates(self, x, y):
		if self.cell(x, y):
			return set([self.cell(x, y)])
		all = set(range(10))
		row = set(self.row(x))
		col = set(self.col(y))
		block = set(self.cell_block(x, y))
		return all - (row | col | block)
	
	def solved(self):
		return 0 not in Sudoku.flatten(self.cells)
	
	def solve_neg(self, x, y):
		if not self.cell(x, y):
			candidates = self.candidates(x, y)
			if len(candidates) == 1:
				value = list(candidates)[0]
				self.set_cell(x, y, value)
				return value
		return self.cell(x, y)
	
	def solve_pos(self, x, y):
		if not self.cell(x, y):
			row_candidates = set()
			for yp in range(1, 10):
				if yp != y and not self.cell(x, yp):
					row_candidates |= self.candidates(x, yp)
			col_candidates = set()
			for xp in range(1, 10):
				if xp != x and not self.cell(xp, y):
					col_candidates |= self.candidates(xp, y)
			block_candidates = set()
			for xp in range(x-(x-1)%3, x-(x-1)%3+3):
				for yp in range(y-(y-1)%3, y-(y-1)%3+3):
					if (xp != x or yp != y) and not self.cell(xp, yp):
						block_candidates |= self.candidates(xp, yp)
			for value in self.candidates(x, y):
				if value not in row_candidates or \
				   value not in col_candidates or \
				   value not in block_candidates:
					self.set_cell(x, y, value)
					return value
		return self.cell(x, y)
	
	def solve(self):
		while not self.solved():
			previous = self.copy()
			for x in range(1, 10):
				for y in range(1, 10):
					if not self.solve_neg(x, y):
						self.solve_pos(x, y)
			if self.cells == previous.cells:
				raise RuntimeError, "Unsolvable Sudoku board"

def neat_solve(S):
	T = S.copy()
	T.solve()
	ST = ""
	for sr, tr in zip(str(S).split("\n"), str(T).split("\n")):
		ST += sr + "     " + tr + "\n"
	print ST[:-1]

def main():
	neat_solve(Sudoku(
		0,8,0,0,0,0,2,0,5,
		7,0,1,4,0,0,0,8,9,
		9,0,0,3,5,0,0,1,0,
		0,0,9,0,0,7,6,3,0,
		0,0,2,0,0,9,7,0,0,
		0,7,8,5,0,0,0,0,0,
		0,6,0,0,4,5,0,0,3,
		2,9,0,0,0,6,5,0,1,
		4,0,5,0,0,0,8,7,0))
	print
	neat_solve(Sudoku([
		[5,3,0,0,7,0,0,0,0],
		[6,0,0,1,9,5,0,0,0],
		[0,9,8,0,0,0,0,6,0],
		[8,0,0,0,6,0,0,0,3],
		[4,0,0,8,0,3,0,0,1],
		[7,0,0,0,2,0,0,0,6],
		[0,6,0,0,0,0,2,8,0],
		[0,0,0,4,1,9,0,0,5],
		[0,0,0,0,8,0,0,7,9]]))
	print
	neat_solve(Sudoku(
		"000235000",
		"009000701",
		"004000206",
		"010800040",
		"750106093",
		"060002070",
		"301000500",
		"807000900",
		"000471000"))
	print
	neat_solve(Sudoku(
		"010607004042000000870300600080070020000893000030060010008006045000000170400908060"))

if __name__ == '__main__': main()
