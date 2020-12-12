import numpy as np
import math
import sys
from bitstring import *

# Read input file
ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

# Set parameters and initial variable values
max_dict_count = 2**16 - 1
dict_count = 0

character_bits = 7
index_bits = math.ceil(math.log(max_dict_count + 1, 2))

class Trie:
	"""A recursive Trie data type for storing and searching the dictionary efficiently"""
	def __init__(self, character):
		global dict_count
		self.character = character
		self.children = []
		self.position = dict_count
		dict_count += 1
	def add_child(self, child_character):
		self.children.append(Trie(child_character))
	def find_match(self, i):
		"""Finds the length of the longest match starting from character i (and returns a pointer to that entry in the dictionary)"""
		best_l = 0
		best_node = self
		if i < len(m):
			for child in self.children:
				if child.character == m[i]:
					l, n = child.find_match(i + 1)
					if l > best_l:
						best_l = l
						best_node = n
		return (best_l + 1, best_node)

enc = ""
dictionary = Trie('')

i = 0
while i < len(m):
	# For each symbol find the length l of the longest match in the dictionary (i.e. m[i..i + l])
	l, node = dictionary.find_match(i)
	p = np.binary_repr(node.position).zfill(index_bits)
	if i + l >= len(m):
		child_chr = m[-1]  # figure out exactly what causes this (this solution causes issues)
	else:
		child_chr = m[i + l - 1]
	if child_chr > 127:
		print("oh no!")
		input()
	c = np.binary_repr(child_chr).zfill(character_bits)
	# Add a new child in the trie
	node.add_child(child_chr)
	if dict_count == max_dict_count:  # If the dictionary exceeds 2**index_bits - 1 then it can no longer be pointed to so it's reset and a new dictionary is used
		dict_count = 0
		dictionary = Trie('')
	# Add the token (p, c) to the output (where p is position in the dictionary of the longest match and c is the character immediately following this matched)
	enc += p + c
	i += l  # Continue encoding from the next unmatched character

print(enc)

# Write to output file
ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)  # enc is a binary string so should be written as such
ofile.close()