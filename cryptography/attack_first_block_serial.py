import numpy as np
import random
import time
from des import *

def check_encrypt(plain):
	if DesKey(b"12345678").encrypt(plain[:8]) == b'\x87\xe4C\xd4ah3_':
		return plain
	return b""

if __name__ == '__main__':
	start = time.time()

	ifile = open("words_even_shorter.txt", "r")
	m = ifile.readlines()
	ifile.close()

	count = 0

	plaintexts = np.array([b"" for i in range(len(m) * len(m))], dtype=bytearray)

	pos = 0
	for i in range(len(m)):
		for j in range(len(m)):
			plaintexts[pos] = (m[i][:-1] + "." + m[j][:-1]).encode()
			pos += 1

	print("got plaintexts")
	# It takes two minutes to compute an array of all possible pairs of words
	# Hopefully, I can parallelise the checking and do it in a reasonable amount of time
	# Also hopefully there aren't too many matches so the second round is quicker
	plaintexts = np.array(list(map(check_encrypt, plaintexts)))
	print("took", time.time() - start, "seconds")

	#for i in range(len(plaintexts)):
	#	if key.encrypt(plaintexts[i][:8]) == cipher_first_eight:
	#		print(plaintexts[i])'''
