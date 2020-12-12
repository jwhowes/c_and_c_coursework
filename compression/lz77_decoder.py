import numpy as np
import math
import sys
from bitstring import *

W = 2**8 - 1
L = 2**8 - 1
W_bits = math.ceil(math.log(W + 1, 2))
L_bits = math.ceil(math.log(L + 1, 2))
character_bits = 8

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(character_bits)

def lz77_decode(enc):
	m = bytearray()
	for j in range(0, len(enc), W_bits + L_bits + character_bits):
		if enc[j + W_bits + L_bits : j + W_bits + L_bits + character_bits] != "":
			i = len(m)
			d = int(enc[j : j + W_bits], 2)
			l = int(enc[j + W_bits : j + W_bits + L_bits], 2)
			c = int(enc[j + W_bits + L_bits : j + W_bits + L_bits + character_bits], 2)
			m += m[i - d : i - d + l]
			m.append(c)
	return m

dec = lz77_decode(enc)
ofile = open("out.tex", "w", newline='\n')
ofile.write(str(dec, encoding="utf-8"))
ofile.close()