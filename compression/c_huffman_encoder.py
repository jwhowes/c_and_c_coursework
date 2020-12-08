import numpy as np
import math
import sys
import json
from bitstring import *

ifile = open("huffman_in.lz", "rb")
m = ifile.read()
ifile.close()

character_bits = 8

A = np.zeros((2**(character_bits + 1)), dtype=int)
max_heap_length = 2**character_bits

for i in m:
	A[i + 256] += 1

heap_length = 0
def heapify():
	global heap_length
	A[0] = A[heap_length - 1]
	v = 1
	heap_length -= 1
	smallest = -1
	while smallest != v:
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

def add_to_heap(value):
	global heap_length
	A[heap_length] = value
	v = heap_length
	while v > 0:
		if v % 2 == 0:
			parent = v // 2
		else:
			parent = (v - 1) // 2
		if A[A[v]] < A[A[parent]]:
			temp = A[parent]
			A[parent] = A[v]
			A[v] = temp
			v = parent
		else:
			break
	heap_length += 1

for i in range(256):
	add_to_heap(i + 256)

lengths = np.zeros((2**character_bits), dtype=int)

while heap_length > 1:
	a = A[0]
	heapify()
	b = A[0]
	heapify()
	# we're combining a and b
	A[heap_length + 2] = A[a] + A[b]
	A[a] = heap_length + 2
	A[b] = heap_length + 2
	add_to_heap(heap_length)