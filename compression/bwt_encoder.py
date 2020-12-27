import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("dict_compressed.lz", "rb")
m = ifile.read()
ifile.close()

end_symbol = 0

enc = bytearray(m)
for i in range(len(enc)):
	enc[i] += 1

enc.append(end_symbol)

start = time.time()

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

print("took", time.time() - start, "seconds")

ofile = open("bwt_encoded.lz", "wb")
ofile.write(enc)
ofile.close()