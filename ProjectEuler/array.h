#include <vector>

typedef int dtype;

class array{
public:
  array(int nrows, int ncols);
  void set(int i, int j, dtype value);
  dtype get(int i, int j);
  void zero();
private:
  int nr;
  int nc;
  vector<dtype> data;
}
