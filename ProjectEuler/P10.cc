#include <cmath>
#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

typedef unsigned long long inttype;

vector<inttype> primes(inttype nmax){
  // Construct a vector of primes using a sieve of Eratosthenes
  int i=0,j=0;
  //vector<bool> isprime;
  bool isprime[nmax];
  vector<inttype> ps;
  int m, mroot;
  for (i=0; i<=nmax; i++) 
    isprime[i] = true;
    //  isprime.push_back(true);
  isprime[0] = false;
  isprime[1] = false;
  for (i=2; i*i <= nmax; i++){
    if (isprime[i]){
      for (j=2; i*j <= nmax; j++)
	isprime[i*j] = false;
    }
  }
  for (i=1; i<nmax; i++){
    if (isprime[i]) {
      ps.push_back(i);
    }
  }
  return ps;
}

main(){
  int n = 1000000;
  vector<inttype> ps = primes(n);
  // accumulate doesn't work here?!
  //inttype psum = accumulate(ps.begin(), ps.end(), 0);
  //cout << psum << endl;
  psum = 0;
  for (vector<inttype>::iterator i=ps.begin(); i<ps.end(); i++)
    psum += *i;
  cout << psum << endl;
}
