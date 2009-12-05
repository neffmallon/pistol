#include <vector>
#include <cmath>
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

string itos(int i) {
  stringstream s;
  s << i;
  return s.str();
}

double log10(double d) {return log(d)/log(10.0);}
int ndigits(int i){return int(log10(i))+1;}

int ithdigit(int n, int i){
  int nd = ndigits(n);
  if ((i >= nd)  or (i < 0)) return -1;
  return (n % int(pow(10.0,nd-i)))/pow(10.0,nd-i-1);
}

bool ispalindromenumber(int n){
  int nd = ndigits(n);
  for (int i=0; i< nd/2; i++){
    //cout << ithdigit(n,i) << " " << ithdigit(n,nd-i-1) << endl;
    if (ithdigit(n,i) != ithdigit(n,nd-i-1))
      return false;
  }
  return true;
}

main(){
  int n = 1000;
  vector<int> results;
  for (int i=700; i<n; i++){
    for (int j=i; j<n; j++){
      if (ispalindromenumber(i*j)) results.push_back(i*j);
    }
  }
  sort(results.begin(),results.end());
  for (vector<int>::iterator i=results.begin(); i<results.end(); i++)
    cout << *i << " ";
  cout << endl;

			     
}

