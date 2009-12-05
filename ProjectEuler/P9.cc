#include <iostream>
#include <cmath>
using namespace std;

main(){
  int n = 1000,a,b,b2,a2,c,c2;
  double xc;
  for (b=1; b<n/2; b++){
    b2 = b*b;
    for (a=1; a<b; a++){
      a2 = a*a;
      c2 = a2+b2;
      c = sqrt(c2);
      if ( (c*c == c2) && (a+b+c==n) )
	cout << a <<" "<< b <<" "<< c <<" "<< a*b*c << endl;
    }
  }
}
