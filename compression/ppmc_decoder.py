import numpy as np
import math
import sys
import time
import pickle
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

alphabet_size = 256

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = bytearray()

N = 4

C = ""
i = 0

precision = 32

low = 0
high = (1 << precision) - 1
offset = 0

def arithmetic_decoder(freqs):
	global low, high, offset, enc
	s = sum(freqs)
	freqs = [0] + freqs
	for i in range(1, len(freqs)):
		freqs[i] += freqs[i - 1]
	buffer = enc[offset : offset + precision]
	b_int = int(buffer, 2)
	value = math.floor((((b_int - low + 1) * s) - 1) / (high - low + 1))
	symbol = 0
	while freqs[symbol] <= value:
		symbol += 1
	symbol -= 1
	newlow = math.floor(low + ((high - low + 1) * freqs[symbol]) / s)
	newhigh = math.floor(low + (((high - low + 1) * freqs[symbol + 1]) / s) - 1)
	lo_bin = np.binary_repr(newlow).zfill(precision)
	hi_bin = np.binary_repr(newhigh).zfill(precision)
	while lo_bin[0] == hi_bin[0]:
		lo_bin = lo_bin[1:] + "0"
		hi_bin = hi_bin[1:] + "1"
		offset += 1
	while lo_bin[1] == "1" and hi_bin[1] == "0":
		lo_bin = lo_bin[0] + lo_bin[2:] + "0"
		hi_bin = hi_bin[0] + hi_bin[2:] + "1"
		# I feel like this next line could be made way more efficient (but need to figure out exactly what it does)
		enc = enc[:offset] + str(1 - int(enc[offset + 1])) + enc[offset + 2:]
	low = int(lo_bin, 2)
	high = int(hi_bin, 2)
	return symbol

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
				if c.character == dec[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(dec[i]))
		else:
			for c in self.children:
				if C[depth - con_length] == c.character:
					c.add_child(con_length, depth + 1)
					break
	def get_character(self, c_length, c_pos):
		global dec, excluded
		if c_length == -1:
			freqs = [1 for i in range(alphabet_size + 1) if i not in excluded]
			x = arithmetic_decoder(freqs)
			pos = 0
			for c in range(alphabet_size + 1):
				if c not in excluded:
					if pos == x:
						x = c
						break
					pos += 1
			if x == alphabet_size:
				return False
			dec.append(x)
			return True
		if c_pos == 0:
			if len(self.children) == 0:
				return root.get_character(c_length - 1, c_length - 1)
			freqs = [c.frequency for c in self.children if c.character not in excluded]
			if len(freqs) == 0:
				return root.get_character(c_length - 1, c_length - 1)
			freqs.append(len(self.children))
			p = arithmetic_decoder(freqs)
			if p is None:
				return False
			if p == len(freqs) - 1:
				for c in self.children:
					excluded[c.character] = True
				return root.get_character(c_length - 1, c_length - 1)
			pos = 0
			for c in range(len(self.children)):
				if self.children[c].character not in excluded:
					if pos == p:
						p = c
						break
					pos += 1
			dec.append(self.children[p].character)
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					return c.get_character(c_length, c_pos - 1)
		return True

#root = Trie(None)

objfile = open("ppmc_dict.pickle", "rb")
root = pickle.load(objfile)
objfile.close()

print("read root")

start = time.time()
while True:
	C = [i for i in dec[max(0, i - N) : i]]
	excluded = {}
	if not root.get_character(len(C), len(C)):
		break
	root.add_character()
	i += 1

print("took", time.time() - start, "seconds")

ofile = open("ppmc_out.lz", "wb")
ofile.write(dec)
ofile.close()