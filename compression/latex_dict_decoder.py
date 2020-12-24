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

ifile = open("ppmc_out.lz", "rb")
enc = ifile.read()
ifile.close()

dec = bytearray()

i = 0
while i < len(enc):
	if enc[i] < 128:
		dec.append(enc[i])
	else:
		index = enc[i]*256 + enc[i + 1] - 33024
		dec += latex_commands[index]
		i += 1
	i += 1

ofile = open("out.tex", "w", newline="\n")
ofile.write(str(dec, encoding='utf-8'))
ofile.close()