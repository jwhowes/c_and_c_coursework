import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("lzw_compressed.lz", "rb")
b = ifile.read()
ifile.close()

eof_byte = 255

character_bits = 8
reference_bits = 8

max_dict_entries = 2**reference_bits

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dict_count = 0
dictionary = []
for i in range(256):
	dictionary.append(bytearray((i).to_bytes(1, 'little')))
	dict_count += 1

i = 0
J = bytearray()
I = bytearray()

dec = bytearray()

start = time.time()

index = int(enc[i : i + reference_bits], 2)
while index != eof_byte:
	if dict_count == max_dict_entries:
		dict_count = 0
		dictionary = []
		for j in range(256):
			dictionary.append(bytearray((j).to_bytes(1, 'little')))
			dict_count += 1
	if index == dict_count:
		J = I + I[0].to_bytes(1, 'little')
	else:
		J = dictionary[index]
	dec += J
	if I + (J[0]).to_bytes(1, 'little') not in dictionary and len(I) > 0:
		dictionary.append(I + (J[0]).to_bytes(1, 'little'))
		dict_count += 1
	I = J.copy()
	i += reference_bits
	index = int(enc[i : i + reference_bits], 2)

dec.append(J[-1])
dec = dec[:-1]

print("took", time.time() - start, "seconds")

ofile = open("lzw_out.lz", "wb")
ofile.write(dec)
ofile.close()