import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("dict_compressed.lz", "rb")
m = ifile.read()
ifile.close()

alphabet_size = 256
N = 5

C = ""
i = 0

enc = ""

precision = 32

full_range = 1 << precision
half_range = full_range >> 1
quarter_range = half_range >> 1
state_mask = full_range - 1

low = 0
high = (1 << precision) - 1
underflow_cntr = 0

def arithmetic_encoder(low_cum_freq, high_cum_freq, total):
	global low, high, underflow_cntr
	ret = ""
	r = high - low + 1
	newlow = low + low_cum_freq * r // total
	newhigh = low + high_cum_freq * r // total - 1
	low = newlow; high = newhigh
	while ((low ^ high) & half_range) == 0:
		bit = low >> (precision - 1)
		ret += str(bit)
		for _ in range(underflow_cntr):
			ret += str(bit ^ 1)
		underflow_cntr = 0
		low = ((low << 1) & state_mask)
		high = ((high << 1) & state_mask) | 1
	while (low & ~high & quarter_range) != 0:
		underflow_cntr += 1
		low = (low << 1) ^ half_range
		high = ((high ^ half_range) << 1) | half_range | 1
	return ret

def end_float():
	global low, enc, underflow_cntr
	lo_bin = np.binary_repr(low).zfill(precision)
	enc += lo_bin[0]
	while underflow_cntr > 0:
		enc += str(1 - int(lo_bin[0]))
		underflow_cntr -= 1
	enc += lo_bin[1:]

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
			freqs = [1 for i in range(alphabet_size + 1) if i not in excluded]
			low = 0
			for c in range(alphabet_size + 1):
				if c not in excluded:
					if c == m[i]:
						break
					low += 1
			enc += arithmetic_encoder(low, low + 1, sum(freqs))
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
				enc += arithmetic_encoder(low, low + c.frequency, s)
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
			enc += arithmetic_encoder(s - len(self.children), s, s)
			for c in self.children:
				excluded[c.character] = True
		root.get_code(c_length - 1, c_length - 1)

root = Trie(None)

m = list(m)
m.append(alphabet_size)

start = time.time()
while i < len(m):
	C = [i for i in m[max(0, i - N) : i]]
	excluded = {}
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1

end_float()

print("took", time.time() - start, "seconds")

ofile = open('ppmc_compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()