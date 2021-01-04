import numpy as np
import time
from des import *
import multiprocessing
import subprocess, sys, os

def check_encrypt(plain):
	p = subprocess.Popen("encrypt.exe " + plain.hex(), stdout=subprocess.PIPE)
	o = p.stdout.read()[:-2]
	if o == b"903408ec4d951acf":
		ofile = open("first_block_out.txt", "w")
		ofile.write(plain)
		ofile.close()
		print("found in function")
		exit()
		return plain
	return b""
	'''if subprocess.run(["encrypt.exe", plain.hex()], stdout=subprocess.PIPE).stdout[:-2] == b"a80f2c74f235484e":
		return plain
	return b""'''

if __name__ == '__main__':
	start = time.time()
	words_file = open("5_letter_words.txt", "r")
	words = words_file.readlines()
	words_file.close()

	for w in range(len(words)):
		words[w] = words[w].replace("\n", "")
		words[w] = words[w].replace("\r", "")

	prefix_file = open("two_letter_prefixes.txt")
	prefixes = prefix_file.readlines()
	for p in range(len(prefixes)):
		prefixes[p] = prefixes[p].replace("\n", "")
		prefixes[p] = prefixes[p].replace("\r", "")

	plaintexts = []
	for i in range(len(words)):
		for j in range(len(prefixes)):
			plaintexts.append((words[i] + "." + prefixes[j]).encode())
	
	print("got plaintexts")
	with multiprocessing.Pool(processes=64) as pool:
		plaintexts = pool.map(check_encrypt, plaintexts)
	ofile = open("first_block.txt", "wb")
	for i in plaintexts:
		if i != b"":
			ofile.write(i + b"\n")
	ofile.close()
	print("took", time.time() - start, "seconds")