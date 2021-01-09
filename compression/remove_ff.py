import numpy as np
from bitstring import *

ifile = open("compressed.lz", "rb")
m = ifile.read()
ifile.close()

enc = bytearray()

for byte in m:
	if byte == 255:
		enc.append(254)
	elif byte == 254:
		enc.append(253)
		enc.append(254)
	elif byte == 253:
		enc.append(253)
		enc.append(253)
	else:
		enc.append(byte)
	

ofile = open('ff_removed.lz', 'wb')
ofile.write(enc)
ofile.close()