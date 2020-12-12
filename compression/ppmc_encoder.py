import numpy as np
import math
import sys
import json
from bitstring import *

ifile = open("in.tex", "rb")
m = ifile.read()
ifile.close()

N = 2

C = ""
i = 0

enc = ""

def arithmetic_coder(low_cum_freq, high_cum_freq):
	return 0

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self, depth=0, con_string=b""):
		if self.character is None or con_string + chr(self.character).encode() == C[len(C) - depth:]:
			found = False
			for c in self.children:
				if c.character == m[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(m[i]))
			for c in self.children:
				if self.character is None:
					c.add_character(depth + 1, con_string)
				else:
					c.add_character(depth + 1, con_string + chr(self.character).encode())
		elif depth < len(C):
			for c in self.children:
				if C[depth] == c.character:
					if self.character is None:
						c.add_character(depth + 1, con_string)
					else:
						c.add_character(depth + 1, con_string + chr(self.character).encode())
	def get_code(self, c_length, c_pos):
		global enc
		denominator = 0
		node = None
		low = 0
		if c_length == -1:
			# Encode character with context -1
			enc += str(arithmetic_coder((m[i]) / 128, ((m[i]) + 1) / 128))
			return
		if c_pos == 0:
			for c in self.children:
				if c.character == m[i]:
					node = c
				if node is None:
					low += c.frequency
				denominator += c.frequency
			denominator += len(self.children)
			if node is not None:
				# Encode character
				enc += str(arithmetic_coder(low / denominator, (low + node.frequency) / denominator))
				return
		else:
			for c in self.children:
				if c.character == C[-c_pos]:
					c.get_code(c_length, c_pos - 1)
					return
				denominator += c.frequency
			denominator += len(self.children)
		# Encode escape character
		if denominator == 0:
			enc += str(arithmetic_coder(0, 1))
		else:
			enc += str(arithmetic_coder((denominator - len(self.children)) / denominator, 1))
		root.get_code(c_length - 1, c_length - 1)
# Currently it just prints what's encoded and with what probability but it is correct
root = Trie(None)

while i < len(m):
	C = m[max(0, i - N) : i]
	root.get_code(len(C), len(C))
	root.add_character()
	i += 1