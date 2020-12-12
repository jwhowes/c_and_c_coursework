import numpy as np
import math
import sys
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

dict_count = 1
max_dict_count = 2**16 - 1

character_bits = 7
index_bits = math.ceil(math.log(max_dict_count + 1, 2))

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dictionary = [(0, 0)]

dec = bytearray()

def string_from_dict(pos):
	ret = bytearray()
	while pos != 0 and pos < len(dictionary):
		p, c = dictionary[pos]
		ret.append(c)
		pos = p
	ret.reverse()
	return ret

for i in range(0, len(enc), index_bits + character_bits):
	if enc[i + index_bits : i + index_bits + character_bits] != "":
		pos = int(enc[i : i + index_bits], 2)
		c = int(enc[i + index_bits : i + index_bits + character_bits], 2)
		dec += string_from_dict(pos)
		dec.append(c)
		dict_count += 1
		if dict_count == max_dict_count:
			dict_count = 1
			dictionary = [(0, 0)]
		else:
			dictionary.append((pos, c))

ofile = open("out.tex", "w", newline='\n')
ofile.write(str(dec, encoding="utf-8"))
ofile.close()