//The prime factors of 13195 are 5, 7, 13 and 29. What is the largest
//prime factor of the number 317584931803?

#include <cmath>
#include <iostream>
#include <vector>
using namespace std;

vector<int> primes(unsigned long long nmax){
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
  unsigned long long num = 317584931803ULL;
  long imax = sqrt(num);
  vector<int> ps;
  ps = primes(imax);
  // print out the primes, if desired:
  //for (vector<int>::iterator i = ps.begin(); i < ps.end(); i++)
  //  cout << *i << " ";
  //cout << endl;
  for (vector<int>::iterator i = ps.begin(); i < ps.end(); i++){
    if (num % *i == 0) cout << *i << endl;
  }
}
