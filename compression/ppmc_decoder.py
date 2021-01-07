import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("compressed.lz", "rb")
b = ifile.read()
ifile.close()

alphabet_size = 256

enc = ""
for i in b:
	enc += np.binary_repr(i).zfill(8)

dec = bytearray()

N = 2

C = ""
i = 0

precision = 32

low = 0
high = (2**precision) - 1
buffer = int(enc[:precision], 2)
next_bit_pos = 32

cntr = 0

def arithmetic_decoder(freqs):
	global low, high, buffer, next_bit_pos, cntr
	s = sum(freqs)
	freqs = [0] + freqs
	for i in range(1, len(freqs)):
		freqs[i] += freqs[i - 1]
	r = high - low + 1
	offset = buffer - low
	value = ((offset + 1) * s - 1) // r
	symbol = 0
	for i in range(1, len(freqs)):
		if freqs[i] > value:
			break
		symbol += 1
	newlow = low + (freqs[symbol] * r) // s
	newhigh = (low + (freqs[symbol + 1] * r) // s) - 1
	lo_bin = np.binary_repr(newlow).zfill(precision)
	hi_bin = np.binary_repr(newhigh).zfill(precision)
	b_bin = np.binary_repr(buffer).zfill(precision)
	while lo_bin[0] == hi_bin[0]:
		lo_bin = lo_bin[1:] + "0"
		hi_bin = hi_bin[1:] + "1"
		if next_bit_pos < len(enc):
			b_bin = b_bin[1:] + enc[next_bit_pos]
			next_bit_pos += 1
		else:
			b_bin = b_bin[1:] + "0"
	while lo_bin[0] == "0" and lo_bin[1] == "1" and hi_bin[0] == "1" and hi_bin[1] == "0":
		cntr += 1
		lo_bin = lo_bin[0] + lo_bin[2:] + "0"
		hi_bin = hi_bin[0] + hi_bin[2:] + "1"
		if next_bit_pos < len(enc):
			b_bin = b_bin[0] + b_bin[2:] + enc[next_bit_pos]
			next_bit_pos += 1
		else:
			b_bin = b_bin[0] + b_bin[2:] + "0"
	low = int(lo_bin, 2)
	high = int(hi_bin, 2)
	buffer = int(b_bin, 2)
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
			if len(freqs) == 0:
				return False
			x = arithmetic_decoder(freqs)
			print(x)
			if x is None or x == len(freqs) - 1:
				return False
			pos = 0
			for c in range(alphabet_size + 1):
				if c not in excluded:
					if pos == x:
						x = c
						break
					pos += 1
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

root = Trie(None)

start = time.time()

while True:
	C = [i for i in dec[max(0, i - N) : i]]
	excluded = {}
	if not root.get_character(len(C), len(C)):
		break
	root.add_character()
	i += 1

print("took", time.time() - start, "seconds")

#print(dec)

ofile = open("out.lz", "wb")
ofile.write(dec)
ofile.close()