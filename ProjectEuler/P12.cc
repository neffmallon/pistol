#include <cmath>
#include <stdio.h>

int ndivisors(int n){
  int s = 0;
  int lim = (int)sqrt(n) + 1;
  for (int i=1; i<lim; i++)
    if (n%i == 0) s += 2;
  return s;
}

main(){
  int nmax=15000;
  int nd,ndi,ndi2,t;
  for (int i=1; i<nmax; i++){
    if (i%2 == 0){
      ndi = ndivisors(i/2);
      ndi2 = ndivisors(i+1);
    } else {
      ndi = ndivisors(i);
      ndi2 = ndivisors((i+1)/2);
    }
    nd = ndi*ndi2;
    t = i*(i+1)/2;
    if (nd > 400)
      printf("%d %d %d %d\n",i,t,nd,ndivisors(t));
  }
}
