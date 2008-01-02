"""
Consider quadratic Diophantine equations of the form:

x^2 - Dy^2 = 1

For example, when D=13, the minimal solution in x is 649^2 - 13*180^2
= 1.

It can be assumed that there are no solutions in positive integers
when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain
the following:

3^2 - 2*2^2 = 1
2^2 - 3*1^2 = 1
9^2 - 5*4^2 = 1
5^2 - 6*2^2 = 1
8^2 - 7*3^2 = 1

Hence, by considering minimal solutions in x for D<=7, the largest x
is obtained when D=5.

Find the value of D<=1000 in minimal solutions of x for which the
largest value of x is obtained.
"""

import psyco; psyco.full()

from math import sqrt

def issquare(n): return isint(sqrt(n))
def isint(n): return int(n) == n

def find_solutions(Ds,maxit):
    results = []
    unfound = []
    for D in Ds:
        if issquare(D): continue
        for x in xrange(2,maxit):
            y = sqrt((x*x-1)/float(D))
            if isint(y):
                results.append((D,x,int(y)))
                break
        else:
            unfound.append(D)
    return results,unfound

def sort_results(results):
    temp = [(x,D,y) for (D,x,y) in results]
    temp.sort()
    return [(D,x,y) for (x,D,y) in temp]

def print_results(results):
    results = sort_results(results)
    for D,x,y in results:
        print "%d^2 - %d x %d^2 = 1" % (x,D,y)
    D,x,y = results[-1]
    print "Maximum x value of %d obtained when D=%d" % (x,D)
    return

results,unfound = find_solutions(xrange(2,1001),10000)
print "Temporary results"
print_results(results)
results2,unfound2 = find_solutions(unfound,1000000)
print "Temporary results2"
print_results(results2)
print "Remaining unfound solutions: "
print unfound2
results3,unfound3 = find_solutions(unfound2,1000000000)
print "Temporary results3"
print_results(results3)
print "Remaining unfound solutions: "
print unfound3

# I think the solution is one of these values for D:

unfound2 = [61, 73, 94, 97, 106, 109, 113, 124, 127, 133, 137, 139,
            149, 151, 157, 163, 166, 172, 173, 179, 181, 191, 193,
            199, 202, 211, 214, 217, 229, 233, 239, 241, 244, 249,
            250, 251, 253, 261, 262, 265, 268, 271, 274, 277, 281,
            283, 284, 292, 293, 295, 298, 301, 302, 307, 309, 311,
            313, 317, 319, 329, 331, 334, 337, 341, 343, 349, 353,
            358, 364, 365, 367, 369, 373, 376, 379, 382, 388, 389,
            391, 393, 394, 397, 406, 409, 412, 415, 417, 419, 421,
            422, 424, 428, 429, 430, 431, 433, 436, 445, 446, 449,
            451, 452, 453, 454, 457, 460, 461, 463, 466, 467, 471,
            477, 478, 479, 481, 487, 489, 490, 491, 493, 496, 497,
            501, 502, 508, 509, 511, 513, 517, 519, 521, 523, 524,
            526, 532, 533, 534, 535, 537, 538, 541, 542, 547, 548,
            549, 550, 553, 554, 556, 559, 562, 565, 566, 569, 571,
            581, 583, 586, 587, 589, 593, 594, 596, 597, 598, 599,
            601, 604, 606, 607, 610, 613, 614, 617, 619, 622, 628,
            629, 631, 633, 634, 636, 637, 639, 640, 641, 643, 645,
            647, 649, 652, 653, 654, 655, 657, 661, 662, 664, 666,
            667, 669, 670, 673, 679, 681, 682, 683, 685, 686, 688,
            691, 692, 694, 698, 699, 700, 701, 703, 709, 713, 716,
            717, 718, 719, 721, 722, 724, 733, 734, 737, 739, 741,
            742, 745, 746, 748, 749, 750, 751, 753, 754, 757, 758,
            761, 763, 764, 766, 769, 771, 772, 773, 775, 778, 779,
            781, 787, 789, 790, 794, 796, 797, 801, 802, 805, 806,
            807, 808, 809, 811, 814, 821, 823, 826, 829, 831, 833,
            834, 835, 838, 844, 845, 846, 847, 849, 851, 853, 854,
            856, 857, 859, 861, 862, 863, 865, 868, 869, 871, 873,
            877, 878, 879, 881, 883, 886, 889, 893, 907, 911, 913,
            914, 916, 917, 918, 919, 921, 922, 925, 926, 928, 929,
            931, 932, 934, 937, 941, 946, 947, 949, 951, 953, 954,
            955, 956, 958, 964, 965, 967, 969, 970, 971, 972, 974,
            976, 977, 981, 988, 989, 991, 995, 996, 997, 998, 999,
            1000]
