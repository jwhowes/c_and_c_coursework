import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

end_symbol = 0

enc = bytearray(m)
enc.append(end_symbol)

for s in range(len(enc) - 3, -1, -1):
	c = enc[s]
	r = s
	i = s + 1
	while enc[i] != end_symbol:
		if enc[i] <= c:
			r += 1
		i += 1
	p = i
	while i < len(enc):
		if enc[i] < c:
			r += 1
		i += 1
	enc[p] = c
	i = s
	while i < r:
		enc[i] = enc[i + 1]
		i += 1
	enc[r] = end_symbol

ofile = open("bwt.lz", "w", newline='\n')
ofile.write(str(enc, encoding="utf-8"))
ofile.close()