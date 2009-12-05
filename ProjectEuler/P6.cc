#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

int square(int i){return i*i;}

main(){
  int nmax=100;
  vector<int> num(nmax),numsq(nmax);
  for (int i=1; i<=nmax; i++){
    num.push_back(i);
    numsq.push_back(i*i);
  }
  int sq_sum = square(accumulate(num.begin(),num.end(),0));
  int sum_sq = accumulate(numsq.begin(),numsq.end(),0);
  cout << sq_sum <<" "<< sum_sq <<" "<< sq_sum-sum_sq << endl;
}
