import numpy as np
import math
import sys
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

W = 2**8 - 1
L = 2**8 - 1
W_bits = math.ceil(math.log(W + 1, 2))
L_bits = math.ceil(math.log(L + 1, 2))
character_bits = 8

def lz77_encode(m):
	"""Returns an array of triples generated by running LZ77 on a message m"""
	i = 0
	ret = ""
	while i < len(m):
		best_d = 0
		best_l = 0
		for d in range(1, min(W, i + 1)):
			l = 1
			while l <= L and l < d and i + l < len(m) and m[i + l - 1] == m[i - d + l - 1]:
				l += 1
			if l - 1 > best_l:
				best_l = l - 1
				best_d = d
		d = np.binary_repr(best_d)
		l = np.binary_repr(best_l)
		c = np.binary_repr(m[i + best_l])
		while len(d) < W_bits:
			d = '0' + d
		while len(l) < L_bits:
			l = '0' + l
		while len(c) < character_bits:
			c = '0' + c
		ret += d + l + c
		i += best_l + 1
	return ret

enc = lz77_encode(m)
ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()