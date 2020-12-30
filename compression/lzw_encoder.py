import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()


eof_byte = 255

character_bits = 8
reference_bits = 16

m += eof_byte.to_bytes(1, 'little')

max_dict_entries = 2**reference_bits

num_entries = -1
class Trie:
	def __init__(self, character):
		global num_entries
		self.character = character
		self.index = num_entries
		num_entries += 1
		self.children = []
	def read_string(self):
		global i, I, enc, num_entries
		if i == len(m):
			enc += np.binary_repr(self.index).zfill(reference_bits)
			return 0
		for c in self.children:
			if c.character == m[i]:
				i += 1
				I.append(c.character)
				return c.read_string()
		enc += np.binary_repr(self.index).zfill(reference_bits)
		self.children.append(Trie(m[i]))
		return m[i]

# Initialise root
root = Trie(None)
for i in range(256):
	root.children.append(Trie(i))

start = time.time()

enc = ""
i = 0
while m[i] != eof_byte:
	I = bytearray()
	root.read_string()
	if num_entries == max_dict_entries:
		num_entries = -1
		root = Trie(None)
		for j in range(256):
			root.children.append(Trie(j))

enc += np.binary_repr(eof_byte).zfill(reference_bits)

print("took", time.time() - start, "seconds")

ofile = open("lzw_compressed.lz", "wb")
BitArray(bin=enc).tofile(ofile)
ofile.close()