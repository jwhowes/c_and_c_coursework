import numpy as np
import time
import heapq

ifile = open("test_bwt.lz", "rb")
enc = ifile.read()
ifile.close()

block_size = 2000
end_symbol = 0
eof_byte = end_symbol.to_bytes(1, 'little')

dec = bytearray()

start = time.time()

pos = 0
while pos < len(enc):
	block = bytearray(enc[pos : pos + block_size + 1])
	n = len(block)
	p = 0
	while block[p] != end_symbol:
		p += 1
	p += 1

	ret = bytearray()

	block_pos = 0
	while n - block_pos > 2:
		c = heapq.nsmallest(p, block[block_pos:])[-1]
		count = 0
		for i in range(n - block_pos):
			if block[i + block_pos] < c:
				count += 1
		f = p - count
		q = -1
		while f > 0:
			q += 1
			if block[q + block_pos] == c:
				f -= 1
		block[q + block_pos] = end_symbol
		for i in range(p-1, 0, -1):
			block[i + block_pos] = block[i + block_pos - 1]
		block[block_pos] = c
		block_pos += 1
		if p - 1 >= q:
			p = q + 1
		else:
			p = q
	block = block[:-1]
	for i in range(len(block)):
		block[i] -= 1
	dec += block
	pos += block_size + 1

print("took", time.time() - start, "seconds")

ofile = open("bwt_out.lz", "wb")
ofile.write(dec)
ofile.close()