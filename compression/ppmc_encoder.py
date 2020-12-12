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
	def get_code(self, C, S, c_length, c_pos):
		denominator = 0
		node = None
		low = 0
		if c_length == -1:
			print(S, "order -1")
			return
		if c_pos == 0:
			for c in self.children:
				if c.character == S:
					node = c
				if node is None:
					low += c.frequency
				denominator += c.frequency
			denominator += len(self.children)
			if node is not None:
				print(node.character, "low:", str(low) + "/" + str(denominator), "high:", str(low + node.frequency) + "/" + str(denominator))
				return
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					c.get_code(C, S, c_length, c_pos - 1)
					return
				denominator += c.frequency
			denominator += len(self.children)
		print("escape", "low:", str(denominator - len(self.children)) + "/" + str(denominator), "high:", 1)
		root.get_code(C, S, c_length - 1, c_length - 1)
# Currently it just prints what's encoded and with what probability but it is correct
root = Trie("")

for i in range(len(m)):
	C = m[max(0, i - N) : i]
	root.get_code(C, m[i], len(C), len(C))
	root.add_character(C, m[i])
	print("!")