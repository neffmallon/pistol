
# My original version
def collapse(lst):
    """Convert a list like [1,2,3,5] to [(1,3),5], where the
    tuple indicates 1-3"""
    clst = []
    #print lst
    # first group the list into consecutive chunks
    for li in lst:
        if len(clst) == 0 or li != current[-1]+1:
            current = [li]
            clst.append(current)
        else:
            current.append(li)
    # Now collapse the chunks into tuples
    tlst = []
    for chunk in clst:
        if len(chunk) == 1: tlst.append(chunk[0])
        else: tlst.append((chunk[0],chunk[-1]))
    return tlst

#Kaer Buhez version, using generators
def collapseGen(aList):
    lastItem=openingItem=aList[0]
    for item in aList[1:]+[None]:
        if item != lastItem+1:
            if openingItem == lastItem:
                yield lastItem
            else:
                yield (openingItem, lastItem)
            openingItem=item
        lastItem=item

def test():
    a=[1,2,3,4,5,10,11,12,13,29,31, 32]
    print [item for item in collapseGen(a)]
    #print collapseGen(a)
    print collapse(a)
    return


if __name__ == '__main__': test()
