import numpy as np
from bitstring import *

ifile = open("bit_stuffed.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = bytearray()

byte = ""
count = 0
i = 0
while i < len(enc):
	byte += enc[i]
	if len(byte) == 8:
		dec.append(int(byte, 2))
		byte = ""
	if enc[i] == "1":
		count += 1
		if count == 7:
			i += 1
			count = 0
	else:
		count = 0
	i += 1

ofile = open("bit_stuffed_out.lz", "wb")
ofile.write(dec)
ofile.close()