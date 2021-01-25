import numpy as np
import math
import sys
import csv

ifile = open("sherlock_shorter.tex", "rb")
m = ifile.read()
ifile.close()

dict_file = open("latex_dict.txt", "r")
latex_commands = dict_file.readlines()
dict_file.close()

for i in range(len(latex_commands)):
	latex_commands[i] = latex_commands[i].replace("\n", "")
	latex_commands[i] = latex_commands[i].replace("\r", "")
	latex_commands[i] = latex_commands[i].encode()

latex_dict = {}

first_byte = 128
second_byte = 0
for i in range(len(latex_commands)):
	latex_dict[latex_commands[i]] = (first_byte * 256 + second_byte).to_bytes(2, 'big')
	second_byte += 1
	if second_byte == 256:
		second_byte = 0
		first_byte += 1

class Trie:
	def __init__(self, character):
		self.character = character
		self.children = []
	def add_string(self, string, pos=0):
		if pos >= len(string):
			return
		for child in self.children:
			if child.character == string[pos]:
				child.add_string(string, pos + 1)
				return
		self.children.append(Trie(string[pos]))
		self.children[-1].add_string(string, pos + 1)
	def find_match(self, i, string=b""):
		best_s = string
		if i < len(m):
			for child in self.children:
				if child.character == m[i]:
					s = child.find_match(i + 1, string + (child.character).to_bytes(1, 'little'))
					if len(s) > len(best_s) and s in latex_dict:
						best_s = s
		return best_s

enc = bytearray()

root = Trie(None)

for i in latex_dict:
	root.add_string(i)

i = 0
while i < len(m):
	s = root.find_match(i)
	if s == b"":
		if m[i] >= 128:
			enc.append(128)
		enc.append(m[i])
		i += 1
	else:
		enc += latex_dict[s]
		i += len(s)

ofile = open("dict_compressed.lz", "wb")
ofile.write(enc)
ofile.close()