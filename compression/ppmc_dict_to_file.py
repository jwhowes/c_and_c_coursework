import pickle
import time

ifile = open("dict_compressed.lz", "rb")
m = ifile.read()
ifile.close()

N = 4

class Trie:
	def __init__(self, character):
		self.character = character
		self.frequency = 1
		self.children = []
	def add_character(self):
		for i in range(len(C) + 1):
			self.add_child(i, 0)
	def add_child(self, con_length, depth):
		if depth == con_length:
			found = False
			for c in self.children:
				if c.character == m[i]:
					c.frequency += 1
					found = True
					break
			if not found:
				self.children.append(Trie(m[i]))
		else:
			for c in self.children:
				if C[depth - con_length] == c.character:
					c.add_child(con_length, depth + 1)
					break

start = time.time()

#root = Trie(None)

objfile = open("ppmc_dict.pickle", "rb")
root = pickle.load(objfile)
objfile.close()

i = 0
while i < len(m):
	C = [i for i in m[max(0, i - N) : i]]
	root.add_character()
	i += 1

#objfile = open("ppmc_dict.pickle", "wb")
#pickle.dump(root, objfile)
#objfile.close()

print("took", time.time() - start, "seconds")