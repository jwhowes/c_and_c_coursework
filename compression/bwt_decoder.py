import numpy as np
import math
import sys
import time
from bitstring import *

enc = b'dkadrfr eiieepklpptppopppccck   ip\x80   eeeere\x81s'

start_symbol = b"\x80"
end_symbol = b"\x81"  # It's important that end_symbol > any other

table = [[None for j in range(len(enc))] for i in range(len(enc))]

for i in range(len(enc)):
	for j in range(len(enc)):
		table[j][-(i + 1)] = enc[j]
	table.sort()

dec = []
for i in table:
	if i[-1].to_bytes(1, 'little') == end_symbol:
		dec = i

dec = bytearray(dec)
dec = dec[1:-1]
print(dec)