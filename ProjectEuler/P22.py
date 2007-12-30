"""
Using names.txt (right click and 'Save Link/Target As...'), a 46K text
file containing over five-thousand first names, begin by sorting it
into alphabetical order. Then working out the alphabetical value for
each name, multiply this value by its alphabetical position in the
list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN,
which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the
list. So, COLIN would obtain a score of 938 53 = 49714.

What is the total of all the name scores in the file?
"""

from string import uppercase

def get_let_value(name):
    s = 0
    for l in name:
        s += uppercase.index(l)+1
    return s

names = open('names.txt').read().split(",")

for i in range(len(names)):
    names[i] = names[i].replace("\"","")


names.sort()

print get_let_value("COLIN") * (names.index("COLIN") + 1)

s = 0
for name in names:
    v = get_let_value(name) * (names.index(name) + 1)
    s += v
print s



