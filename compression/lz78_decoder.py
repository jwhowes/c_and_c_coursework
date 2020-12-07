import numpy as np
import math
import sys
import json
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

dict_count = 1
max_dict_count = 2**16 - 1

character_bits = 8
index_bits = math.ceil(math.log(max_dict_count + 1, 2))

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(character_bits)

dictionary = [(0, '')]

dec = ""

def string_from_dict(pos):
	ret = ""
	while pos != 0 and pos < len(dictionary):
		p, c = dictionary[pos]
		ret = c + ret
		pos = p
	return ret

for i in range(0, len(enc), index_bits + character_bits):
	if enc[i + index_bits : i + index_bits + character_bits] != "":
		pos = int(enc[i : i + index_bits], 2)
		c = chr(int(enc[i + index_bits : i + index_bits + character_bits], 2))
		dec += string_from_dict(pos) + c
		dict_count += 1
		if dict_count == max_dict_count:
			dict_count = 1
			dictionary = [(0, '')]
		else:
			dictionary.append((pos, c))

ofile = open("out.tex", "w")
ofile.write(dec)
ofile.close()