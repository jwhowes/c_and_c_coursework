import numpy as np
import random
import time
from des import *
import multiprocessing
import subprocess, sys, os

# The first eight of bytes of the ciphertext: b'\x904\x08\xecM\x95\x1a\xcf'

'''def check_encrypt(plain):
	if DesKey(b"12345678").encrypt(plain[:8]) == b'\x904\x08\xecM\x95\x1a\xcf':
		return plain
	return b""'''

def check_encrypt(plain):
	p = subprocess.Popen("encrypt.exe " + plain[:8].hex(), stdout=subprocess.PIPE)
	o = p.stdout.read()[:-2]
	if o == b"903408ec4d951acf":
		ofile = open("first_block_out.txt", "w")
		ofile.write(plain)
		ofile.close()
		print("found in function")
		exit()
		return plain
	return b""
	'''if subprocess.run(["encrypt.exe", plain[:8].hex()], stdout=subprocess.PIPE).stdout[:-2] == b"a80f2c74f235484e":
		return plain
	return b""'''

if __name__ == '__main__':
	start = time.time()
	with multiprocessing.Pool(processes=16) as pool:

		ifile = open("words.txt", "r")
		m = ifile.readlines()
		ifile.close()

		count = 0
		plaintexts = []
		#plaintexts = np.array([b"" for i in range(len(m) * len(m))], dtype=bytearray)

		pos = 0
		for i in range(len(m)):
			for j in range(len(m)):
				if len(m[i]) + len(m[j]) <= 11:
					plaintexts.append((m[i][:-1] + "." + m[j][:-1]).encode())
		plaintexts = np.array(plaintexts[::-1], dtype=bytearray)

		print("got plaintexts")  # I got this far without crashing (i.e. doesn't use too much memory. Let's hope the rest won't either)
		shorter_plaintexts = pool.map(check_encrypt, plaintexts)
	ofile = open("pairs.txt", "wb")
	for i in plaintexts:
		if i != b"":
			ofile.write(i + b"\n")
	ofile.close()
	print("took", time.time() - start, "seconds")