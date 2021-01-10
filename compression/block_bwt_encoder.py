import numpy as np
import time

ifile = open("bit_stuffed.lz", "rb")
m = ifile.read()
ifile.close()

m = bytearray(m)

for i in range(len(m)):
	m[i] += 1

block_size = 2048

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

print(len(block))

print("took", time.time() - start, "seconds")

ofile = open("bwt_encoded.lz", "wb")
ofile.write(enc)
ofile.close()