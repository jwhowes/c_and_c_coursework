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

neg_one_freqs = np.ones((alphabet_size + 1), dtype=int)

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

def huffman_encoder(character, frequencies):
	global A, heap_length
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
	return codewords[character]

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
		pos = -1
		if c_length == -1:
			# Encode character with context -1z
			enc += huffman_encoder(m[i], neg_one_freqs.copy())
			#enc += arithmetic_coder(m[i]/(alphabet_size + 1), (m[i] + 1) / (alphabet_size + 1))
			return
		if c_pos == 0:
			for c in range(len(self.children)):
				if self.children[c].character == m[i]:
					pos = c
					break
			if pos != -1:
				freqs = [c.frequency for c in self.children]
				freqs.append(len(self.children))
				# Encode character
				enc += huffman_encoder(pos, freqs)
				#enc += arithmetic_coder(low / denominator, (low + node.frequency) / denominator)
				return
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					c.get_code(c_length, c_pos - 1)
					return
		# Encode escape character
		# if there are no children (context has never been seen before), we print nothing
		if len(self.children) != 0:
			freqs = [c.frequency for c in self.children]
			freqs.append(len(self.children))
			enc += huffman_encoder(len(self.children), freqs)
			#enc += arithmetic_coder((denominator - len(self.children)) / denominator, 1)
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

print(len(enc)/8, len(m))
print("took", time.time() - start, "seconds")

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()