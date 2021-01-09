import numpy as np
from bitstring import *

ifile = open("ff_removed.lz", "rb")
enc = ifile.read()
ifile.close()

dec = bytearray()

i = 0
while i < len(enc):
	if enc[i] == 253:
		dec.append(enc[i + 1])
		i += 1
	elif enc[i] == 254:
		dec.append(255)
	else:
		dec.append(enc[i])
	i += 1

ofile = open("ff_added.lz", "wb")
ofile.write(dec)
ofile.close()