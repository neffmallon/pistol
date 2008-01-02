"""
In the card game poker, a hand consists of five cards and are ranked,
from lowest to highest, in the following way:

    * High Card: Highest value card.
    * One Pair: Two cards of the same value.
    * Two Pairs: Two different pairs.
    * Three of a Kind: Three cards of the same value.
    * Straight: All cards are consecutive values.
    * Flush: All cards of the same suit.
    * Full House: Three of a kind and a pair.
    * Four of a Kind: Four cards of the same value.
    * Straight Flush: All cards are consecutive values of same suit.
    * Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the
highest value wins; for example, a pair of eights beats a pair of
fives (see example 1 below). But if two ranks tie, for example, both
players have a pair of queens, then highest cards in each hand are
compared (see example 4 below); if the highest cards tie then the next
highest cards are compared, and so on.

Consider the following four hands dealt to two players:
Hand	 	Player 1	 	Player 2	      Winner
1	 	5H 5C 6S 7S KD          2C 3S 8S 8D TD        Player 2
                Pair of Fives           Pair of Eights

2	 	5D 8C 9S JS AC          2C 5C 7D 8S QH        Player 1
                Highest card Ace        Highest card Queen
	 	
3	 	2D 9C AS AH AC          3D 6D 7D TD QD        Player 2
                Three Aces              Flush with Diamonds

4	 	4D 6S 9H QH QC          3D 6D 7H QD QS        Player 1
                Pair of Queens          Pair of Queens    
                Highest card Nine       Highest card Seven
	 	
5	 	2H 2D 4C 4D 4S          3C 3D 3S 9S 9D        Player 1
                Full House              Full House       
                With Three Fours        With Three Threes

The file, poker.txt, contains one-thousand random hands dealt to two
players. Each line of the file contains ten cards (separated by a
single space): the first five are player one's cards and the last five
are player two's cards. You can assume that all hands are valid (no
invalid characters or repeated cards), each player's hand is in no
specific order, and in each hand there is a clear winner.

How many hands does player one win?
"""

from sets import Set

data = """\
5H 5C 6S 7S KD          2C 3S 8S 8D TD 
5D 8C 9S JS AC          2C 5C 7D 8S QH 
2D 9C AS AH AC          3D 6D 7D TD QD 
4D 6S 9H QH QC          3D 6D 7H QD QS 
2H 2D 4C 4D 4S          3C 3D 3S 9S 9D \
"""

trans = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
         'T':10,'J':11,'Q':12,'K':13,'A':14}
rtrans = [None,None,'2','3','4','5','6','7','8','9',
          'T','J','Q','K','A']

class Hand:
    def __init__(self,string):
        self.string = string
        self.tuples = [parsecard(word) for word in self.string.split()]
        self.dict = todict(self.tuples)
        self.score = [0,0,0]
        self.pair_analysis = pair_analysis(self.dict)
        self.suits = suits(self.tuples)
        self.nums = nums(self.tuples)
        self.nums.sort()
        self.set_score()

    def set_score(self):
        if len(Set(self.nums)) == 5 and self.nums[-1]-self.nums[0] == 4:
            # straight
            if len(self.suits) == 1: 
                if self.nums[0] == 10: # royal flush
                    self.score = [9,0,0]
                else: # straight flush
                    self.score[0] = 8
                    self.score[1] = self.nums[-1]
            else: # plain straight
                self.score[0] = 4
                self.score[1] = self.nums[-1]
        elif len(self.suits) == 1: # flush
            self.score[0] = 5
            self.score[1] = self.nums[-1]
        # Otherwise, have to do pair analysis
        elif isfour(self.tuples):
            self.score[0] = 7
            self.score[1] = self.dict[4]
        elif istrio(self.tuples):
            if ispair(self.tuples): # Full house
                self.score[0] = 6
                self.score[1] = self.pair_analysis[0][1]
                self.score[2] = self.pair_analysis[1][1]
            else: # three of a kind
                self.score[0] = 3
                self.score[1] = self.pair_analysis[0][1]
        elif is2pair(self.tuples):
            self.score[0] = 2
            m1,n1 = self.pair_analysis[0]
            m2,n2 = self.pair_analysis[1]
            self.score[1] = max(n1,n2)
            self.score[2] = min(n1,n2)
        elif ispair(self.tuples):
            self.score[0] = 1
            self.score[1] = self.pair_analysis[0][1]
            self.score[2] = max(self.pair_analysis[1][1],
                                self.pair_analysis[2][1],
                                self.pair_analysis[3][1])
        else:
            self.score[0] = 0
            self.score[1] = self.nums[-1]
        return

    def __cmp__(self,other): return cmp(self.score,other.score)

def parsecard(s): return trans[s[0]],s[1]

def parseline(line):
    words = line.split()
    return " ".join(words[0:5])," ".join(words[5:10])

def todict(hand):
    d = {}
    for num,suit in hand:
        if num in d:
            d[num].append(suit)
        else:
            d[num] = [suit]
    return d

def pair_analysis(d):
    l = []
    for di in d:
        l.append( (len(d[di]),di) )
    l.sort()
    l.reverse()
    return l

def suits(h): return Set([s for n,s in h])
def nums(h): return [n for n,s in h]

def isflush(h): return len(suits(h)) == 1

def isntuple(h,target):
    for mult,num in pair_analysis(todict(h)):
        if mult == target: return True
    return False

def ispair(h): return isntuple(h,2)
def istrio(h): return isntuple(h,3)
def isfour(h): return isntuple(h,4)
def isfullhouse(h): return ispair(h) and istrio(h)

def is2pair(h):
    ps = pair_analysis(todict(h))
    m1,n1 = ps[0]
    m2,n2 = ps[1]
    return m1 == m2 == 2

def isstraight(h):
    ns = nums(h)
    return ns[-1]-ns[0] == 4

#for line in data.splitlines():
n1 = 0
for line in open("poker.txt"):
    h1,h2 = parseline(line)
    h1 = Hand(h1)
    h2 = Hand(h2)
    if cmp(h1,h2) == 1:
        n1 += 1
    elif cmp(h1,h2) == 0:
        print "??"
        print h1.string,h2.string
print n1

