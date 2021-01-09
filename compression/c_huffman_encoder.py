import numpy as np
import math
import sys
from bitstring import *

ifile = open("rle_compressed.lz", "rb")
m = ifile.read()
ifile.close()

character_bits = 8

A = np.zeros((2**(character_bits + 1)), dtype=int)
num_characters = 2**character_bits

for i in m:
	A[i + num_characters] += 1

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

for i in range(num_characters):
	add_to_heap(i + num_characters)

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

# I'm fairly certain it's working

lengths = np.ones((num_characters), dtype=int)

for i in range(num_characters):
	v = A[i + num_characters]
	while v != 1:
		lengths[i] += 1
		v = A[v]

codewords = {k: "" for k in sorted(list(range(num_characters)), key=lambda x: lengths[x])}

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

enc = ""
for i in m:
	enc += codewords[i]

length_bits = math.ceil(math.log(max_length, 2))
length_encoding = ""
for i in lengths:
	length_encoding += np.binary_repr(i).zfill(length_bits)

enc = length_encoding + enc

enc = np.binary_repr(length_bits).zfill(character_bits) + enc

ofile = open('huffman_compressed.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()