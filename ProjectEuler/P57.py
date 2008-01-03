from Utils import cf_to_rf,ndigits

nexp=1000
l = [1]
nlarger = 0
for i in range(nexp):
    l.append(2)
    r = cf_to_rf(l)
    if ndigits(r.N) > ndigits(r.D): nlarger += 1
    #print i+1,r,nlarger
print nlarger

    

