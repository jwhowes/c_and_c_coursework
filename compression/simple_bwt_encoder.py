import numpy as np
import time

ifile = open("ff_removed.lz", "rb")
m = ifile.read()
ifile.close()

m = bytearray(m)

for i in range(len(m)):
	m[i] += 1

block_size = 2000

end_symbol = 0
eof_byte = end_symbol.to_bytes(1, 'little')

enc = bytearray()

start = time.time()

pos = 0
while pos < len(m):
	block = bytearray(m[pos : pos + block_size]) + eof_byte
	for s in range(len(block) - 3, -1, -1):
		c = block[s]
		r = s
		i = s + 1
		while block[i] != end_symbol:
			if block[i] <= c:
				r += 1
			i += 1
		p = i
		while i < len(block):
			if block[i] < c:
				r += 1
			i += 1
		block[p] = c
		i = s
		while i < r:
			block[i] = block[i + 1]
			i += 1
		block[r] = end_symbol
	enc += block
	pos += block_size

print("took", time.time() - start, "seconds")


'''def rotate(s):
	return s[1:] + s[0].to_bytes(1, 'little')

start = time.time()

pos = 0
while pos < len(m):
	block = m[pos : pos + block_size]
	rotations = [b"" for i in range(block_size)]
	rotations[0] = m
	for i in range(1, block_size):
		rotations[i] = rotate(rotations[i - 1])

	rotations.sort()
	for r in rotations:
		enc.append(r[-1])
	pos += block_size

print("took", time.time() - start, "seconds")'''

ofile = open("test_bwt.lz", "wb")
ofile.write(enc)
ofile.close()