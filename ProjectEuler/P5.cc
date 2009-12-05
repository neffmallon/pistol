#include <iostream>
using namespace std;

typedef long long inttype;

inttype gcd(inttype a, inttype b){
  if (b == 0) return a;
  return gcd(b,a%b);
}

inttype lcm(inttype a, inttype b){return a*b/gcd(a,b);}

main(){
  inttype sm = 1;
  for (int i=2; i<21; i++){
    sm = lcm(i,sm);
    cout << i << " " << sm << endl;
  }
  cout << "Final results = " << sm << endl;
}

