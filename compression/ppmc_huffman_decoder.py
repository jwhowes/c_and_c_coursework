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

N = 5

C = ""
decode_pos = 0
i = 0

A = np.zeros(1, dtype=int)
heap_length = 0

def heapify():
	global heap_length
	v = 1
	heap_length -= 1
	smallest = -1
	while True:
		smallest = v
		if 2*v < heap_length:
			if A[A[2*v - 1]] < A[A[smallest - 1]]:
				smallest = 2*v
		if 2*v + 1 < heap_length:
			if A[A[2*v]] < A[A[smallest - 1]]:
				smallest = 2*v + 1
		if smallest != v:
			temp = A[smallest - 1]
			A[smallest - 1] = A[v - 1]
			A[v - 1] = temp
			v = smallest
		else:
			break

def add_to_heap(value):
	global heap_length
	A[heap_length] = value
	v = heap_length + 1
	parent = v // 2
	while parent >= 1 and A[A[v - 1]] < A[A[parent - 1]]:
		temp = A[parent - 1]
		A[parent - 1] = A[v - 1]
		A[v - 1] = temp
		v = parent
		parent = v // 2
	heap_length += 1

def huffman_decoder(frequencies):
	global A, heap_length, decode_pos
	A = np.zeros((2*len(frequencies)), dtype=int)
	for i in range(len(frequencies)):
		A[i + len(frequencies)] = frequencies[i]
	heap_length = 0
	for i in range(len(frequencies)):
		add_to_heap(i + len(frequencies))
	while heap_length > 1:
		a = A[0]
		A[0] = A[heap_length - 1]
		heapify()
		b = A[0]
		A[heap_length] = A[a] + A[b]
		A[a] = heap_length
		A[b] = heap_length
		A[0] = heap_length
		heap_length += 1
		heapify()
	lengths = np.ones((len(frequencies)), dtype=int)
	for i in range(len(frequencies)):
		v = A[i + len(frequencies)]
		while v != 1:
			lengths[i] += 1
			v = A[v]
	codewords = {k: "" for k in sorted(list(range(len(frequencies))), key=lambda x: lengths[x])}
	max_length = lengths.max()
	numl = np.zeros((max_length + 1), dtype=int)
	for i in lengths:
		numl[i] += 1
	first = np.zeros((max_length + 1), dtype=int)
	first[max_length] = 0
	for i in range(max_length - 1, 0, -1):
		first[i] = math.ceil((first[i + 1] + numl[i + 1])/2)
	l = -1
	for i in codewords:
		if lengths[i] != l:
			l = lengths[i]
			num = first[l]
		codewords[i] = np.binary_repr(num).zfill(lengths[i])
		num += 1
	codewords = dict([(v, k) for k, v in codewords.items()])
	v = ""
	while decode_pos < len(enc):
		if v in codewords:
			return codewords[v]
		v += enc[decode_pos]
		decode_pos += 1
	return None

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
			freqs = [1 for i in range(alphabet_size) if i not in excluded]
			x = huffman_decoder(freqs)
			if x is None or x == len(freqs) - 1:
				return False
			pos = 0
			for c in range(alphabet_size):
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
			p = huffman_decoder(freqs)
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

while decode_pos < len(enc):
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