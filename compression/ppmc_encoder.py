import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

alphabet_size = 128

N = 2

C = ""
i = 0

enc = ""

precision = 32
a = 0
b = 2**precision - 1
cntr = 0

def arithmetic_coder(low_cum_freq, high_cum_freq):
	global a, b, cntr
	old_a = a
	ret = ""
	w = b - a + 1
	a = a + math.floor(w * low_cum_freq)
	b = old_a + math.floor(w * high_cum_freq) - 1
	a_bin = np.binary_repr(a).zfill(precision)
	b_bin = np.binary_repr(b).zfill(precision)
	if a_bin[0] == b_bin[0]:
		ret += a_bin[0]
		if cntr > 0:
			if a_bin[0] == "0":
				ret += '1' * cntr
			else:
				ret += '0' * cntr
			cntr = 0
		a_bin = a_bin[1:] + "0"
		b_bin = b_bin[1:] + "1"
	while a_bin[0] == b_bin[0]:
		ret += a_bin[0]
		a_bin = a_bin[1:] + "0"
		b_bin = b_bin[1:] + "1"
	while a_bin[0] == "0" and a_bin[1] == "1" and b_bin[0] == "1" and b_bin[1] == "0":
		a_bin = a_bin[0] + a_bin[2:] + "0"
		b_bin = b_bin[0] + b_bin[2:] + "1"
		cntr += 1
	a = int(a_bin, 2)
	b = int(b_bin, 2)
	return ret

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self, depth=0, con_string=[]):
		if self.character is None or con_string + [self.character] == C[len(C) - depth:]:
			found = False
			for c in self.children:
				if c.character == m[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(m[i]))
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
	def get_code(self, c_length, c_pos):
		global enc
		denominator = 0
		node = None
		low = 0
		if c_length == -1:
			# Encode character with context -1z
			enc += arithmetic_coder(m[i]/(alphabet_size + 1), (m[i] + 1) / (alphabet_size + 1))
			return
		if c_pos == 0:
			for c in self.children:
				if c.character == m[i]:
					node = c
				if node is None:
					low += c.frequency
				denominator += c.frequency
			denominator += len(self.children)
			if node is not None:
				# Encode character
				enc += arithmetic_coder(low / denominator, (low + node.frequency) / denominator)
				return
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					c.get_code(c_length, c_pos - 1)
					return
				denominator += c.frequency
			denominator += len(self.children)
		# Encode escape character
		# if there are no children (context has never been seen before), we print nothing
		if denominator != 0:
			enc += arithmetic_coder((denominator - len(self.children)) / denominator, 1)
		root.get_code(c_length - 1, c_length - 1)
# Currently it just prints what's encoded and with what probability but it is correct
root = Trie(None)

m += (alphabet_size).to_bytes(1, 'little')

start = time.time()
while i < len(m):
	C = [i for i in m[max(0, i - N) : i]]
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1
enc += np.binary_repr(b)

print("took", time.time() - start, "seconds")

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()