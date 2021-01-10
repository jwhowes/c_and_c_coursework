ifile = open("rle_compressed.lz", "rb")
enc = ifile.read()
ifile.close()

dec = bytearray()

i = 0
count = 0
last = None

for i in range(len(enc)):
	if count == 3:
		for _ in range(enc[i]):
			dec.append(last)
		count = 0
		last = None
	else:
		dec.append(enc[i])
		if last is None:
			last = enc[i]
			count = 1
		elif enc[i] == last:
			count += 1
		else:
			last = enc[i]
			count = 1

ofile = open("rle_out.lz", "wb")
ofile.write(dec)
ofile.close()