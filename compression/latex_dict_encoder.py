import numpy as np
import math
import sys
import csv

dict_file = open("latex_dict.txt", "r")
latex_commands = dict_file.readlines()
dict_file.close()

for i in range(len(latex_commands)):
	latex_commands[i] = latex_commands[i].replace("\n", "")
	latex_commands[i] = latex_commands[i].replace("\r", "")
	latex_commands[i] = latex_commands[i].encode()

latex_dict = {}

for i in range(len(latex_commands)):
	latex_dict[latex_commands[i]] = (i + 33024).to_bytes(2, 'big')

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

enc = bytearray()

i = 0
while i < len(m):
	if m[i] == 92:
		longest_match = None
		for k in latex_dict:
			if i + len(k) <= len(m) and m[i : i + len(k)] == k and (longest_match is None or len(k) > len(longest_match)):
				longest_match = k
		if longest_match is None:
			enc.append(m[i])
			i += 1
		else:
			enc += latex_dict[longest_match]
			i += len(longest_match)
	else:
		enc.append(m[i])
		i += 1

print(len(m), len(enc))
print(m, enc)

ofile = open("dict_encoder_out.lz", "wb")
ofile.write(enc)
ofile.close()