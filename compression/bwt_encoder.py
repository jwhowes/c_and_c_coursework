import numpy as np
import math
import sys
import time
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

start_symbol = b"\x80"
end_symbol = b"\x81"

m = start_symbol + m + end_symbol

def rotate(s):
	return s[-1].to_bytes(1, 'little') + s[:-1]

table = [b"" for i in range(len(m))]
table[0] = m
for i in range(1, len(m)):
	table[i] = rotate(table[i - 1])

table.sort()

enc = bytearray()
for i in table:
	enc.append(i[-1])

ofile = open("bwt.lz", "w", newline='\n')
ofile.write(str(enc, encoding="utf-8"))
ofile.close()