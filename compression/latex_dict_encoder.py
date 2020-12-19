import numpy as np
import math
import sys
import csv

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

latex_dict = {}

with open("latex_dict.csv", newline='\n') as dict_file:
	reader = csv.reader(dict_file, delimiter=',')
	for row in reader:
		if len(row[1]) > 0:
			latex_dict[row[0].encode()] = int(row[1]).to_bytes(2, 'big')

enc = bytearray()

i = 0
while i < len(m):
	if m[i] == 92:
		found = False
		for k in latex_dict:
			if i + len(k) <= len(m) and m[i : i + len(k)] == k:
				found = True
				enc += latex_dict[k]
				i += len(k)
				break
		if not found:
			enc.append(m[i])
			i += 1
	else:
		enc.append(m[i])
		i += 1

ofile = open("dict_encoder_out.lz", "wb")
ofile.write(enc)
ofile.close()