import numpy as np
import math
import sys
import ctypes
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

N = 2

C = ""
i = 0

enc = ""

precision = 32
a = 0
b = 2**precision - 1

def arithmetic_coder(low_cum_freq, high_cum_freq):
	global a, b
	old_a = a
	ret = ""
	w = b - a + 1
	a = a + math.floor(w * low_cum_freq)
	b = old_a + math.floor(w * high_cum_freq) - 1
	a_bin = np.binary_repr(a).zfill(precision)
	b_bin = np.binary_repr(b).zfill(precision)
	while a_bin[0] == b_bin[0]:
		ret += a_bin[0]
		a_bin = a_bin[1:] + "0"
		b_bin = b_bin[1:] + "1"
	a = int(a_bin, 2)
	b = int(b_bin, 2)
	return ret
	# Need to add rescaling

decode_a = 0
decode_b = 2**precision - 1
decode_pos = 0
def arithmetic_decoder(enc, frequencies):
	global decode_a, decode_b, decode_pos
	w = decode_b - decode_a + 1
	old_a = decode_a
	frequencies = [0] + frequencies
	for i in range(1, len(frequencies)):
		frequencies[i] += frequencies[i - 1]
	index = math.floor(((int(enc[decode_pos : decode_pos + precision], 2) - decode_a + 1) * frequencies[-1] - 1) / (decode_b - decode_a + 1))
	char = 0
	for i in range(len(frequencies)):
		if frequencies[i] > index:
			char = i - 1
			break
	decode_a = old_a + math.floor(w*frequencies[char]/frequencies[-1])
	decode_b = old_a + math.floor(w*frequencies[char + 1]/frequencies[-1])
	a_bin = np.binary_repr(decode_a).zfill(precision)
	b_bin = np.binary_repr(decode_b).zfill(precision)
	while a_bin[0] == b_bin[0]:
		a_bin = a_bin[1:] + "0"
		b_bin = b_bin[1:] + "1"
		decode_pos += 1
	decode_a = int(a_bin, 2)
	decode_b = int(b_bin, 2)
	return char

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self, depth=0, con_string=b""):
		if self.character is None or con_string + chr(self.character).encode() == C[len(C) - depth:]:
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
					c.add_character(depth + 1, con_string + chr(self.character).encode())
		elif depth < len(C):
			for c in self.children:
				if C[depth] == c.character:
					if self.character is None:
						c.add_character(depth + 1, con_string)
					else:
						c.add_character(depth + 1, con_string + chr(self.character).encode())
	def get_code(self, c_length, c_pos):
		global enc
		denominator = 0
		node = None
		low = 0
		if c_length == -1:
			# Encode character with context -1
			enc += arithmetic_coder(m[i]/128, (m[i] + 1) / 128)
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

while i < len(m):
	C = m[max(0, i - N) : i]
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1
enc += np.binary_repr(b)

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()