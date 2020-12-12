import numpy as np
import math
import sys
from bitstring import *

character_bits = 8
num_characters = 2**character_bits

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

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

frequency = np.zeros((2**character_bits), dtype=int)
for i in m:
	frequency[i] += 1

alphabet_size = 0
for i in frequency:
	if i > 0:
		alphabet_size += 1

A = np.zeros((alphabet_size * 2), dtype=int)

c = 0
for i in range(num_characters):
	if frequency[i] > 0:
		A[c + alphabet_size] = frequency[i]
		c += 1

c = 0
for i in range(num_characters):
	if frequency[i] > 0:
		add_to_heap(c + alphabet_size)
		c += 1

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

lengths = np.ones((alphabet_size), dtype=int)

for i in range(alphabet_size):
	v = A[i + alphabet_size]
	while v != 1:
		lengths[i] += 1
		v = A[v]

max_length = lengths.max()
length_sort_key = np.zeros((num_characters), dtype=int)
c = 0
for i in range(num_characters):
	if frequency[i] > 0:
		length_sort_key[i] = lengths[c]
		c += 1
	else:
		length_sort_key[i] = max_length + 1
	
D1_codewords = {k: "" for k in sorted(list(range(num_characters)), key=lambda x: length_sort_key[x])}

numl = np.zeros((max_length + 1), dtype=int)
for i in lengths:
	numl[i] += 1

first = np.zeros((max_length + 1), dtype=int)
first[max_length] = 0
for i in range(max_length - 1, 0, -1):
	first[i] = math.ceil((first[i + 1] + numl[i + 1])/2)

l = -1
for i in D1_codewords:
	if length_sort_key[i] != max_length + 1:
		if length_sort_key[i] != l:
			l = length_sort_key[i]
			num = first[l]
		D1_codewords[i] = np.binary_repr(num).zfill(length_sort_key[i])
		num += 1

D1_length_bits = math.ceil(math.log(max_length, 2))
D1_length_encoding = ""
#length_skip_bits = 4
#max_length_skip = 2**length_skip_bits
num_skipped = 0
tot_num_skipped = 0
#for i in range(num_characters):
#	if num_skipped == max_length_skip:
#		D1_length_encoding += "1" + np.binary_repr(num_skipped - 1).zfill(length_skip_bits)
#		num_skipped = 0
#	if frequency[i] == 0:
#		tot_num_skipped += 1
#		num_skipped += 1
#	elif num_skipped > 0:
#		D1_length_encoding += "1" + np.binary_repr(num_skipped - 1).zfill(length_skip_bits)
#	if frequency[i] == 0:
#		D1_length_encoding += "0" + np.binary_repr(lengths[i]).zfill(D1_length_bits)
c = 0
for i in range(num_characters):
	if c >= alphabet_size:
		break
	if frequency[i] == 0:
		D1_length_encoding += "1"
	else:
		D1_length_encoding += "0" + np.binary_repr(lengths[c]).zfill(D1_length_bits)
		c += 1
D1_length_encoding = np.binary_repr(alphabet_size).zfill(character_bits) + np.binary_repr(D1_length_bits).zfill(character_bits) + D1_length_encoding

# D1_length_encoding now stores the string for encoding D1 (should be prepended to enc after lzfga1 is done)
# D1_codewords now stores the D1 codeword for each symbol
# Consider adding a flag to mark the end (i.e. from this point, all frequencies are 0)
	# An idea would be to put an 8-bit number saying total number of non-zero frequency bytes, then once that many are read decoder knows it's the end
# Format of D1 encoding:
	# First 8 bits is size of the alphabet
	# Next 8 bits is number of bits dedicated to encoding the length of a character's codeword
	# Next few bits is each character's encoding like so:
		# If a character's frequency is 0, it is encoded with a single 1
		# If a character's frequency is > 0, it is encoded with a 0 followed by it's length (encoded in length_bits bits)
	# Once all characters from the alphabet are encoded (which the decoder will know as it knows the alphabet length), the alphabet encoded simply stops (as all remaining characters have frequency 0)
	# From this data, the decoder should be able to retrieve all bytes that have frequency > 0 (the alphabet) and the length of the encoding of each character in the alphabet which should be enough data to compute the codewords for each character

literal_bits = 8
max_literal_length = 16
literal_length_bits = literal_bits - int(math.log(max_literal_length, 2))
copy_bits = 16

search_buffer_size = int(2**(copy_bits - math.log(max_literal_length, 2)))

copy_depth_bits = int(copy_bits - math.log(max_literal_length, 2))
copy_length_bits = copy_bits - copy_depth_bits

literal_string = ""

enc = ""

i = 0
while i < len(m):
	best_d = 0
	best_l = 1
	d = 1
	while d < min(search_buffer_size, i+1):
		l = 1
		while l <= max_literal_length and l < d and i + l <= len(m) and m[i + l - 1] == m[i - d + l - 1]:
			l += 1
		if l - 1 > best_l:
			best_l = l - 1
			best_d = d
		d += l
	if (best_l >= 2 or len(literal_string) == max_literal_length) and len(literal_string) > 0:
		literal_token = "0000"
		literal_token += np.binary_repr(len(literal_string) - 1).zfill(literal_length_bits)
		enc += literal_token
		for j in literal_string:
			enc += D1_codewords[ord(j)]
		literal_string = ""
	if best_l >= 2:
		length = np.binary_repr(best_l - 1).zfill(copy_length_bits)
		d = np.binary_repr(best_d).zfill(copy_depth_bits)
		enc += length + d
	else:
		literal_string += chr(m[i])
	i += best_l

if len(literal_string) > 0:
	literal_token = "0000"
	literal_token += np.binary_repr(len(literal_string) - 1).zfill(literal_length_bits)
	enc += literal_token
	for j in literal_string:
		enc += D1_codewords[ord(j)]

enc = D1_length_encoding + enc

ofile = open('huffman_in.lz', 'wb')
BitArray(bin=enc).tofile(ofile)
ofile.close()