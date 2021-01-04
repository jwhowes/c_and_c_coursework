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

inv_dict = {}
first_byte = 129
second_byte = 0
for i in range(len(latex_commands)):
	inv_dict[first_byte * 256 + second_byte] = latex_commands[i]
	second_byte += 1
	if second_byte == 255:
		second_byte = 0
		first_byte += 1

i = 0
while i < len(enc):
	if enc[i] == 128:
		dec.append(enc[i + 1])
		i += 1
	elif enc[i] < 128:
		dec.append(enc[i])
	else:
		index = enc[i]*256 + enc[i + 1]
		dec += inv_dict[index]
		i += 1
	i += 1

ofile = open("out.tex", "wb")
ofile.write(dec)
ofile.close()