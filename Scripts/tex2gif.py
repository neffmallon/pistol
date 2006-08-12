#!/usr/bin/env python
"""\
 tex2gif.py  Lightweight wrapper around Tex2Img libraries

 Much credit is due to Nikos Drakos' pstogif.pl
  and John Walker's textogif PERL programs.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""
from Pistol.Tex2Img import tk_converter

if __name__ == '__main__': tk_converter()
