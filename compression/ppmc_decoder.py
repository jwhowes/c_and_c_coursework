import numpy as np
import math
import sys
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

alphabet_size = 128

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = bytearray()

N = 2

C = ""
i = 0

precision = 32
a = 0
b = 2**precision - 1
decode_pos = 0

neg_one_freqs = [1 for _ in range(alphabet_size + 1)]

def arithmetic_decoder(frequencies):
	global a, b, decode_pos
	w = b - a + 1
	old_a = a
	frequencies = [0] + frequencies
	for i in range(1, len(frequencies)):
		frequencies[i] += frequencies[i - 1]
	index = math.floor(((int(enc[decode_pos : decode_pos + precision], 2) - a + 1) * frequencies[-1] - 1) / w)
	char = 0
	for i in range(len(frequencies)):
		if frequencies[i] > index:
			char = i - 1
			break
	a = old_a + math.floor(w*frequencies[char]/frequencies[-1])
	b = old_a + math.floor(w*frequencies[char + 1]/frequencies[-1]) - 1
	a_bin = np.binary_repr(a).zfill(precision)
	b_bin = np.binary_repr(b).zfill(precision)
	while a_bin[0] == b_bin[0]:
		a_bin = a_bin[1:] + "0"
		b_bin = b_bin[1:] + "1"
		decode_pos += 1
	a = int(a_bin, 2)
	b = int(b_bin, 2)
	return char

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self, depth=0, con_string=[]):
		if self.character is None or con_string + [self.character] == C[len(C) - depth:]:
			found = False
			for c in self.children:
				if c.character == dec[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(dec[i]))
			for c in self.children:
				if self.character is None:
					c.add_character(depth + 1, con_string)
				else:
					c.add_character(depth + 1, con_string + [self.character])
		elif depth < len(C):
			for c in self.children:
				if C[depth] == c.character:
					if self.character is None:
						c.add_character(depth + 1, con_string)
					else:
						c.add_character(depth + 1, con_string + [self.character])
	def get_character(self, c_length, c_pos):
		global dec
		denominator = 0
		node = None
		low = 0
		if c_length == -1:
			x = arithmetic_decoder(neg_one_freqs.copy())
			if x == alphabet_size:
				return False
			dec.append(x)
			return True
		if c_pos == 0:
			if len(self.children) == 0:
				return root.get_character(c_length - 1, c_length - 1)
			freqs = [c.frequency for c in self.children]
			freqs.append(len(self.children))
			p = arithmetic_decoder(freqs)
			if p == len(self.children):
				return root.get_character(c_length - 1, c_length - 1)
			dec.append(self.children[p].character)
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					return c.get_character(c_length, c_pos - 1)
		return True

root = Trie(None)

while True:
	C = [i for i in dec[max(0, i - N) : i]]
	if not root.get_character(len(C), len(C)):
		break
	root.add_character()
	i += 1

ofile = open("out.tex", "w", newline="\n")
ofile.write(str(dec, encoding='utf-8'))
ofile.close()

# It works up to a point. I think underflow is probably happening