# A simple Huffman encoder (not using canonical mode)
import numpy as np
import math
import sys
import json
from bitstring import *

ifile = open("huffman_in.lz", "rb")
m = ifile.read()
ifile.close()

character_bits = 8
num_characters = 2**character_bits

codewords = {}

class HuffmanTree:
	def __init__(self, frequency=0, character=None):
		self.left_child = -1
		self.right_child = -1
		self.frequency = frequency
		self.character = character
	def get_codewords(self, codeword=""):
		global codewords
		if self.character is not None:
			codewords[self.character] = codeword
		else:
			nodes[self.left_child].get_codewords(codeword + "0")
			nodes[self.right_child].get_codewords(codeword + "1")

nodes = np.array([HuffmanTree(character=i) for i in range(num_characters)])
tree = np.array([i for i in range(num_characters)])

for i in m:
	nodes[i].frequency += 1

while len(tree) > 1:
	min_pos = np.array([nodes[t].frequency for t in tree]).argmin()
	a = tree[min_pos]
	tree = np.delete(tree, min_pos)
	min_pos = np.array([nodes[t].frequency for t in tree]).argmin()
	b = tree[min_pos]
	tree = np.delete(tree, min_pos)
	parent = HuffmanTree(frequency=nodes[a].frequency + nodes[b].frequency)
	parent.left_child = a
	parent.right_child = b
	nodes = np.append(nodes, [parent])
	tree = np.append(tree, [len(nodes) - 1])
nodes[tree[0]].get_codewords()