from Utils import cf_to_rf,num_to_digits

l = [2]
for i in range(1,40):
    l.extend([1,2*i,1])

for i in range(10):
    r = cf_to_rf(l[:(i+1)])
    print r, sum(num_to_digits(r.N))
    
r = cf_to_rf(l[:100])
print sum(num_to_digits(r.N))



