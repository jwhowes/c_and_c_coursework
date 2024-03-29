import numpy as np
import math
import sys
from bitstring import *
import io

literal_bits = 8
max_literal_length = 16
literal_length_bits = literal_bits - int(math.log(max_literal_length, 2))
copy_bits = 16

copy_depth_bits = int(copy_bits - math.log(max_literal_length, 2))
copy_length_bits = copy_bits - copy_depth_bits

character_bits = 8

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = bytearray()

i = 0
while i < len(enc):
	if enc[i : i + 4] == "0000" and enc[i + 4 : i + 4 + literal_length_bits] != "":  # Token is a literal token
		literal_string = ""
		l = int(enc[i + 4 : i + 4 + literal_length_bits], 2) + 1
		for j in range(i + literal_bits, i + literal_bits + l * character_bits, character_bits):
			literal_string += chr(int(enc[j : j + character_bits], 2))
			dec.append(int(enc[j : j + character_bits], 2))
		i += literal_bits + l * character_bits
	elif enc[i + copy_length_bits : i + copy_length_bits + copy_depth_bits] != "":  # Token is a copy token
		p = len(dec)
		l = int(enc[i : i + copy_length_bits], 2) + 1
		d = int(enc[i + copy_length_bits : i + copy_length_bits + copy_depth_bits], 2)
		dec += dec[p - d : p - d + l]
		i += copy_bits
	else:
		break

ofile = io.open("out.tex", "w", newline='\n')
ofile.write(str(dec, encoding="utf-8"))
ofile.close()