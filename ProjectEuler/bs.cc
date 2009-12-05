#include <iostream>
#include <gmpxx.h>
using namespace std;

int
main (void)
{
  mpz_class a, b, c;

  a = 1234;
  b = "-5678";
  c = a+b;

  return 0;
}
