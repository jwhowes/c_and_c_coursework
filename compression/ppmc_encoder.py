import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

alphabet_size = 256
N = 2

C = ""
i = 0

enc = ""

precision = 32

low = 0
high = (2**precision) - 1
underflow_cntr = 0

def arithmetic_encoder(low_prob, high_prob):
	global low, high, underflow_cntr
	ret = ""
	r = high - low + 1
	newlow = low + math.floor(low_prob * r)
	newhigh = low + math.floor(high_prob * r) - 1
	lo_bin = np.binary_repr(newlow).zfill(precision)
	hi_bin = np.binary_repr(newhigh).zfill(precision)
	while lo_bin[0] == hi_bin[0]:
		bit = lo_bin[0]
		ret += bit
		lo_bin = lo_bin[1:] + "0"
		hi_bin = hi_bin[1:] + "1"
		if underflow_cntr > 0:
			for i in range(underflow_cntr):
				ret += str(1 - int(bit))
			underflow_cntr = 0
	while lo_bin[0] == "0" and lo_bin[1] == "1" and hi_bin[0] == "1" and hi_bin[1] == "0":
		underflow_cntr += 1
		lo_bin = lo_bin[0] + lo_bin[2:] + "0"
		hi_bin = hi_bin[0] + hi_bin[2:] + "1"
	low = int(lo_bin, 2)
	high = int(hi_bin, 2)
	return ret

excluded = {}

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self):
		for i in range(len(C) + 1):
			self.add_child(i, 0)
	def add_child(self, con_length, depth):
		if depth == con_length:
			found = False
			for c in self.children:
				if c.character == m[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(m[i]))
		else:
			for c in self.children:
				if C[depth - con_length] == c.character:
					c.add_child(con_length, depth + 1)
					break
	def get_code(self, c_length, c_pos):
		global enc, excluded
		found = False
		if c_length == -1:
			# Encode character with context -1
			freqs = [1 for i in range(alphabet_size) if i not in excluded]
			low = 0
			for c in range(alphabet_size):
				if c not in excluded:
					if c == m[i]:
						break
					low += 1
			print("order -1", chr(m[i]), low, low + 1, len(freqs))
			enc += arithmetic_encoder(low/len(freqs), (low + 1)/len(freqs))
			return
		if c_pos == 0:
			low = 0
			for c in self.children:
				if c.character not in excluded:
					if c.character == m[i]:
						found = True
						break
					low += c.frequency
			if found:
				freqs = [c.frequency for c in self.children if c.character not in excluded]
				freqs.append(len(self.children))
				s = sum(freqs)
				print(chr(c.character), low, low + c.frequency, s)
				enc += arithmetic_encoder(low/s, (low + c.frequency)/s)
				return
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					c.get_code(c_length, c_pos - 1)
					return
		# Encode escape character
		# if there are no children (context has never been seen before), we print nothing
		if len(self.children) != 0:
			freqs = [c.frequency for c in self.children if c.character not in excluded]
			if len(freqs) == 0:
				root.get_code(c_length - 1, c_length - 1)
				return
			freqs.append(len(self.children))
			s = sum(freqs)
			print("escape", s - len(self.children), s, s)
			enc += arithmetic_encoder((s - len(self.children))/s, 1)
			for c in self.children:
				excluded[c.character] = True
		root.get_code(c_length - 1, c_length - 1)

root = Trie(None)

start = time.time()
while i < len(m):
	C = [i for i in m[max(0, i - N) : i]]
	excluded = {}
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1
# End message by escaping N + 1 times (escapes out of order -1) TODO

#enc += np.binary_repr(low).zfill(precision) not sure if we need this

print("took", time.time() - start, "seconds")

print(enc)

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()