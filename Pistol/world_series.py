#!/usr/bin/env python
"""\
 Predict world series outcomes using Monte Carlo
"""

from random import random
home_winning_percentage = 0.52

def main(nsamples=100000):
    home_games,away_games = 0,0

    for i in range(nsamples):
        h,a = world_series()
        home_games += h
        away_games += a
        ftot = float(i+1)
        if i%100 == 0:
            print "%6.4f %6.4f %6.4f" % (
                home_games/ftot,away_games/ftot,(home_games+away_games)/ftot)
    return

def world_series():
    home_games,away_games = 0,0
    for i in range(7):
        if random() < home_winning_percentage: home_games += 1
        else: away_games += 1
        if home_games == 4 or away_games == 4: break
    return home_games,away_games

if __name__ == '__main__': main()
