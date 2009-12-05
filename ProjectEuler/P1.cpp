// Problem 1:
// If we list all the natural numbers below 10 that are multiples of 3
// or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
// Find the sum of all the multiples of 3 or 5 below 1000.

#include <iostream>
#include <set>
#include <numeric>

using namespace std;

main(){
  int maxn=1000;
  int i=0;
  set<int> s;

  for (i=3; i<maxn; i+=3)
    s.insert(i);
  for (i=5; i<maxn; i+=5)
    s.insert(i);
  int sum = accumulate(s.begin(),s.end(),0);
  cout << "Sum of 3/5's below " << maxn << " = " << sum << endl;
}
