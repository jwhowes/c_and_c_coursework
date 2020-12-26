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
			p = 0
			for c in range(alphabet_size):
				if c not in excluded:
					if c == m[i]:
						break
					p += 1
			enc += huffman_encoder(p, freqs)
			return
		if c_pos == 0:
			p = 0
			for c in self.children:
				if c.character not in excluded:
					if c.character == m[i]:
						found = True
						break
					p += 1
			if found:
				freqs = [c.frequency for c in self.children if c.character not in excluded]
				freqs.append(len(self.children))
				# Encode character
				enc += huffman_encoder(p, freqs)
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
			enc += huffman_encoder(len(freqs) - 1, freqs)
			for c in self.children:
				excluded[c.character] = True
		root.get_code(c_length - 1, c_length - 1)
	def end_message(self, c_length, c_pos):
		global enc, excluded
		if c_length == -1:
			freqs = [1 for i in range(alphabet_size) if i not in excluded]
			enc += huffman_encoder(len(freqs) - 1, freqs)
			return
		if len(self.children) != 0:
			freqs = [c.frequency for c in self.children if c.character not in excluded]
			if len(freqs) == 0:
				root.end_message(c_length - 1, c_length - 1)
				return
			freqs.append(len(self.children))
			enc += huffman_encoder(len(freqs) - 1, freqs)
			for c in self.children:
				excluded[c.character] = True
		root.end_message(c_length - 1, c_length - 1)



root = Trie(None)

start = time.time()
while i < len(m):
	C = [i for i in m[max(0, i - N) : i]]
	excluded = {}
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1

# End message by escaping N + 1 times (escapes out of order -1)
C = [i for i in m[max(0, i - N) : i]]
excluded = {}
root.end_message(len(C), len(C))

print("took", time.time() - start, "seconds")

ofile = open('compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()