import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

start = time.time()

m = bytearray(m)

literal_bits = 8
max_literal_length = 16
literal_length_bits = literal_bits - int(math.log(max_literal_length, 2))
copy_bits = 16

search_buffer_size = int(2**(copy_bits - math.log(max_literal_length, 2)))

copy_depth_bits = int(copy_bits - math.log(max_literal_length, 2))
copy_length_bits = copy_bits - copy_depth_bits

character_bits = 8

end_symbol = 0
bwt_chunk_size = 2*search_buffer_size

bwt = bytearray()

for k in range(0, len(m), bwt_chunk_size):
	chunk = m[k : k + bwt_chunk_size]
	chunk.append(end_symbol)
	n = len(chunk)
	for s in range(n - 3, -1, -1):
		c = chunk[s]
		r = s
		i = s + 1
		while chunk[i] != end_symbol:
			if chunk[i] <= c:
				r += 1
			i += 1
		p = i
		while i < n:
			if chunk[i] < c:
				r += 1
			i += 1
		chunk[p] = c
		i = s
		while i < r:
			chunk[i] = chunk[i + 1]
			i += 1
		chunk[r] = end_symbol
	bwt += chunk

m = bwt

print("took", time.time() - start, "seconds to compute bwt")

literal_string = ""

enc = ""

i = 0
while i < len(m):
	best_d = 0
	best_l = 1
	d = 1
	while d < min(search_buffer_size, i+1):
		l = 1
		while l <= max_literal_length and l < d and i + l <= len(m) and m[i + l - 1] == m[i - d + l - 1]:
			l += 1
		if l - 1 > best_l:
			best_l = l - 1
			best_d = d
		d += l
	if (best_l >= 2 or len(literal_string) == max_literal_length) and len(literal_string) > 0:
		literal_token = "0000"
		literal_token += np.binary_repr(len(literal_string) - 1).zfill(literal_length_bits)
		enc += literal_token
		for j in literal_string:
			enc += np.binary_repr(ord(j)).zfill(character_bits)
		literal_string = ""
	if best_l >= 2:
		length = np.binary_repr(best_l - 1).zfill(copy_length_bits)
		d = np.binary_repr(best_d).zfill(copy_depth_bits)
		enc += length + d
	else:
		literal_string += chr(m[i])
	i += best_l

if len(literal_string) > 0:
	literal_token = "0000"
	literal_token += np.binary_repr(len(literal_string) - 1).zfill(literal_length_bits)
	enc += literal_token
	for j in literal_string:
		enc += np.binary_repr(ord(j)).zfill(character_bits)

print("took", time.time() - start, "seconds")

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()