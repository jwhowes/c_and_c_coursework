import numpy as np
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

m = ""
for i in b:
	m += np.binary_repr(i).zfill(8)

enc = ""

count = 0
for bit in m:
	if bit == "1":
		count += 1
		if count == 7:
			for _ in range(count):
				enc += "1"
			enc += "0"
			count = 0
	else:
		for _ in range(count):
			enc += "1"
		enc += "0"
		count = 0

ofile = open("bit_stuffed.lz", "wb")
BitArray(bin=enc).tofile(ofile)
ofile.close()