import numpy as np
import math
import sys
import json
from bitstring import *

ifile = open("in.tex", "r")
m = ifile.read()
ifile.close()

N = 2

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self, C, S, depth=0, con_string=""):
		if con_string + self.character == C[len(C) - depth:]:
			found = False
			for c in self.children:
				if c.character == S:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(S))
			for c in self.children:
				c.add_character(C, S, depth + 1, con_string + self.character)
		elif depth < len(C):
			for c in self.children:
				if C[depth] == c.character:
					c.add_character(C, S, depth + 1, con_string + self.character)
# IT WORKS!!!!!
root = Trie("")

for i in range(len(m)):
	C = m[max(0, i - N) : i]
	root.add_character(C, m[i])

for c in n.children:
	print(c.character, c.frequency)