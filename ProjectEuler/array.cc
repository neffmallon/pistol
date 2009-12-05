#include "array.h"

array::array(int nrows, int ncols){
  nr = nrows;
  nc = ncols; 
  vector<dtype> data(nr*nc);    
}
array::zero(){
  for (vector<dtype>::iterator i=data.begin(); i < data.end(); i++)
    *i = 0.0;
}
dtype array::get(int i, int j){
  return data[i*nr+j];
}
array::set(int i, int j, dtype value){
  data[i*nr+j] = value;
}
