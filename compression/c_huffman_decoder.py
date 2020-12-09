import numpy as np
import math
import sys
import json
from bitstring import *

character_bits = 8

num_characters = 2**character_bits

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(character_bits)

dec = bytearray()

length_bits = int(enc[:8], 2)

lengths = np.zeros((num_characters), dtype=int)
for i in range(8, 8 + length_bits * num_characters, length_bits):
	lengths[(i - 8)//length_bits] = int(enc[i : i + length_bits], 2)

max_length = lengths.max()
numl = np.zeros((max_length + 1), dtype=int)
for i in lengths:
	numl[i] += 1

first = np.zeros((max_length + 1), dtype=int)
first[max_length] = 0
for i in range(max_length - 1, 0, -1):
	first[i] = math.ceil((first[i + 1] + numl[i + 1])/2)

codewords = {k: "" for k in sorted(list(range(num_characters)), key=lambda x: lengths[x])}

l = -1
for i in codewords:
	if lengths[i] != l:
		l = lengths[i]
		num = first[l]
	codewords[i] = np.binary_repr(num).zfill(lengths[i])
	num += 1

i = 8 + length_bits * num_characters
codewords = dict([(v, k) for k, v in codewords.items()])
v = ""
while i < len(enc):
	if v in codewords:
		dec.append(codewords[v])
		v = ""
	else:
		v += enc[i]
		i += 1

#while i < len(enc):
#	v = ""
#	l = 1
#	while v == "" or (int(v, 2) < first[l] and i < len(enc)):
#		v += enc[i]
#		l += 1
#		i += 1
#	v = int(v, 2)

ofile = open("huffman_out.lz", "wb")
ofile.write(dec)
ofile.close()