import numpy as np
import math
import sys
import time
import heapq
from bitstring import *

ifile = open("bwt_encoded.lz", "rb")
enc = ifile.read()
ifile.close()

end_symbol = 0

dec = bytearray(enc)

n = len(dec)

p = 0
while dec[p] != end_symbol:
	p += 1
p += 1

ret = bytearray()

dec_pos = 0
while n - dec_pos > 2:
	c = heapq.nsmallest(p, dec[dec_pos:])[-1]
	count = 0
	for i in range(n - dec_pos):
		if dec[i + dec_pos] < c:
			count += 1
	f = p - count
	q = -1
	while f > 0:
		q += 1
		if dec[q + dec_pos] == c:
			f -= 1
	dec[q + dec_pos] = end_symbol
	for i in range(p-1, 0, -1):
		dec[i + dec_pos] = dec[i + dec_pos - 1]
	dec[dec_pos] = c
	dec_pos += 1
	if p - 1 > q:
		p = q + 1
	else:
		p = q

dec = dec[:-1]
for i in range(len(dec)):
	dec[i] -= 1

print(dec)

ofile = open("bwt_out.lz", "wb")
ofile.write(dec)
ofile.close()