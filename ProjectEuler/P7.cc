
#include <cmath>
#include <iostream>
#include <vector>
using namespace std;

vector<int> primes(int nmax){
  // Construct a vector of primes using a sieve of Eratosthenes
  int i=0,j=0;
  vector<bool> isprime;
  vector<int> ps;
  int m, mroot;
  for (i=0; i<=nmax; i++) 
    isprime.push_back(true);
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
  vector<int> ps = primes(1000000);
  cout << ps[10000] << endl;
}
