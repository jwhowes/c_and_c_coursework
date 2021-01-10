import numpy as np
from bitstring import *

ifile = open("bwt_out.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = ""

last_zero = True
count = 0
i = 0

while i < len(enc):
	if enc[i] == "1":
		if last_zero:
			for _ in range(count):
				dec += "0"
			count = 0
		dec += "1"
		count += 1
		last_zero = False
		if count == 7:
			i += 1
			count = 0
	else:
		if not last_zero:
			count = 0
		last_zero = True
		count += 1
	i += 1

dec = dec[:-1]

ofile = open("bit_stuffed_out.lz", "wb")
BitArray(bin=dec).tofile(ofile)
ofile.close()