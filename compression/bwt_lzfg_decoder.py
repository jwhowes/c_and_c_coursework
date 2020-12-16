import numpy as np
import math
import sys
from bitstring import *
import io
import heapq

literal_bits = 8
max_literal_length = 16
literal_length_bits = literal_bits - int(math.log(max_literal_length, 2))
copy_bits = 16

search_buffer_size = int(2**(copy_bits - math.log(max_literal_length, 2)))

copy_depth_bits = int(copy_bits - math.log(max_literal_length, 2))
copy_length_bits = copy_bits - copy_depth_bits

character_bits = 8

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

m = bytearray()

i = 0
while i < len(enc):
	if enc[i : i + 4] == "0000" and enc[i + 4 : i + 4 + literal_length_bits] != "":  # Token is a literal token
		literal_string = ""
		l = int(enc[i + 4 : i + 4 + literal_length_bits], 2) + 1
		for j in range(i + literal_bits, i + literal_bits + l * character_bits, character_bits):
			literal_string += chr(int(enc[j : j + character_bits], 2))
			m.append(int(enc[j : j + character_bits], 2))
		i += literal_bits + l * character_bits
	elif enc[i + copy_length_bits : i + copy_length_bits + copy_depth_bits] != "":  # Token is a copy token
		p = len(m)
		l = int(enc[i : i + copy_length_bits], 2) + 1
		d = int(enc[i + copy_length_bits : i + copy_length_bits + copy_depth_bits], 2)
		m += m[p - d : p - d + l]
		i += copy_bits
	else:
		break

end_symbol = 0
bwt_chunk_size = 2*search_buffer_size

dec = bytearray()

for k in range(0, len(m), bwt_chunk_size):
	chunk = m[k : k + bwt_chunk_size]
	n = len(chunk)
	p = 0
	while chunk[p] != end_symbol:
		p += 1
	p += 1
	dec_pos = 0
	while n - dec_pos > 2:
		c = heapq.nsmallest(p, chunk[dec_pos:])[-1]
		count = 0
		for i in range(n - dec_pos):
			if chunk[i + dec_pos] < c:
				count += 1
		f = p - count
		q = -1
		while f > 0:
			q += 1
			if chunk[q + dec_pos] == c:
				f -= 1
		chunk[q + dec_pos] = end_symbol
		for i in range(p-1, -1, -1):
			chunk[i + dec_pos] = chunk[i + dec_pos - 1]
		chunk[dec_pos] = c
		dec_pos += 1
		if p - 1 > q:
			p = q + 1
		else:
			p = q
	dec += chunk[:-1]

ofile = open("out.tex", "w", newline="\n")
ofile.write(str(dec, encoding="utf-8"))
ofile.close()