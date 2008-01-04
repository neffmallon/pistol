
from Utils import permute

istep = 0
for p in permute([1,2,3,4,5,6,7,8,9,10]):
    istep += 1
    p015 = p[0] + p[1] + p[5]
    if p015 == p[1] + p[2] + p[6] and \
       p015 == p[2] + p[3] + p[7] and \
       p015 == p[3] + p[4] + p[8] and \
       p015 == p[4] + p[0] + p[9]:
        print "%d,%d,%d;%d,%d,%d;%d,%d,%d;%d,%d,%d;%d,%d,%d" % \
              (p[5],p[0],p[1],p[6],p[1],p[2],p[7],p[2],p[3],
               p[8],p[3],p[4],p[9],p[4],p[0])


    
