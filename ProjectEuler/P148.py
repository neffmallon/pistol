from pprint import pprint
from Utils import prod
from pylab import *

# The pattern we see looks like:
"""\
                              _                              
                             _ _                             
                            _ _ _                            
                           _ _ _ _                           
                          _ _ _ _ _                          
                         _ _ _ _ _ _                         
                        _ _ _ _ _ _ _                        
                       _ * * * * * * _                       
                      _ _ * * * * * _ _                      
                     _ _ _ * * * * _ _ _                     
                    _ _ _ _ * * * _ _ _ _                    
                   _ _ _ _ _ * * _ _ _ _ _                   
                  _ _ _ _ _ _ * _ _ _ _ _ _                  
                 _ _ _ _ _ _ _ _ _ _ _ _ _ _                 
                _ * * * * * * _ * * * * * * _                
               _ _ * * * * * _ _ * * * * * _ _               
              _ _ _ * * * * _ _ _ * * * * _ _ _              
             _ _ _ _ * * * _ _ _ _ * * * _ _ _ _             
            _ _ _ _ _ * * _ _ _ _ _ * * _ _ _ _ _            
           _ _ _ _ _ _ * _ _ _ _ _ _ * _ _ _ _ _ _           
          _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _          
         _ * * * * * * _ * * * * * * _ * * * * * * _         
        _ _ * * * * * _ _ * * * * * _ _ * * * * * _ _        
       _ _ _ * * * * _ _ _ * * * * _ _ _ * * * * _ _ _       
      _ _ _ _ * * * _ _ _ _ * * * _ _ _ _ * * * _ _ _ _      
     _ _ _ _ _ * * _ _ _ _ _ * * _ _ _ _ _ * * _ _ _ _ _     
    _ _ _ _ _ _ * _ _ _ _ _ _ * _ _ _ _ _ _ * _ _ _ _ _ _    
   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _   
  _ * * * * * * _ * * * * * * _ * * * * * * _ * * * * * * _  
 _ _ * * * * * _ _ * * * * * _ _ * * * * * _ _ * * * * * _ _ 
"""
# but it's not that simple, because at 49 we start bigger triangles.

def gen_pascal():
    last = []
    while True:
        n = len(last)
        row = [1]*(n+1)
        for i in range(1,n):
            row[i] = last[i-1]+last[i]
        last = row
        yield row
    return

def fact(n):
    if n <= 0: return 1
    return prod(xrange(1,n+1))

def combos(n,m): return fact(n)/fact(n-m)/fact(m)
def combos_slower(n,m):
    if m == 0 or n == m: return 1
    return combos(n-1,m-1)+combos(n-1,m)

def gen_pascal_row(n):
    for r in range(0,n+1):
        yield combos(n,r)
    return

def gen_pascal_row_fast(n):
    el = 1
    yield el
    for m in range(1,n+1):
        el = (el*(n-m+1))/m
        yield el
    return

def brute(nmax=10):
    entries = 0
    div7 = 0
    for i in range(1,nmax+1):
        row = gen_pascal_row_fast(i)
        for el in row:
            entries += 1
            if el % 7 == 0: div7 += 1
    not7 = entries-div7
    print not7,entries
    return

def test():
    ps = gen_pascal()
    for i in range(0,1000):
        if not list(gen_pascal_row_fast(i))==list(ps.next()):
            print i
        if i % 100 == 0: print "Done with ",i

def guess(n):
    div,mod = divmod(n,7)
    #print (div,mod),
    if div == 0: return 0
    return n-(div+1)*(mod+1)+1

def gen_triangle(nrows):
    rows = []
    for i in range(nrows):
        rows.append(list(gen_pascal_row_fast(i)))
    return rows

def text_rows(rows):
    trows = []
    for row in rows:
        tmp = []
        for i in row:
            if i%7 == 0: tmp.append('*')
            else: tmp.append('_')
        trows.append(' '.join(tmp))
    return trows

def plot_rows():
    nrows = 50
    rows = gen_triangle(nrows)
    trows = text_rows(rows)
    for trow in trows:
        print trow.center(2*nrows+1)
    return

def main():
    n = 0
    div7 = 0
    data = []
    for i in range(0,20000):
        row = gen_pascal_row_fast(i)
        for el in row:
            n += 1
            if el % 7 == 0:
                div7 += 1
        data.append(div7/float(n))
    plot(data)
    show()
    return
                   
if __name__ == '__main__':
    main()
    #plot_rows()


    
