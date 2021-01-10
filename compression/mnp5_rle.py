import numpy as np

ifile = open("bwt_encoded.lz", "rb")
m = ifile.read()
ifile.close()

min_count = 3

enc = bytearray()

curr_byte = None
count = 0
for byte in m:
	if curr_byte is None:
		curr_byte = byte
		count = 1
	elif byte != curr_byte:
		if count < min_count:
			for _ in range(count):
				enc.append(curr_byte)
		else:
			for _ in range(min_count):
				enc.append(curr_byte)
			enc.append(count - min_count)
		curr_byte = byte
		count = 1
	elif count == 255 + min_count:
		for _ in range(min_count):
			enc.append(curr_byte)
		enc.append(count - min_count)
		curr_byte = None
		count = 0
	else:
		count += 1

if count < min_count:
	for _ in range(count):
		enc.append(curr_byte)
else:
	for _ in range(min_count):
		enc.append(curr_byte)

ofile = open("rle_compressed.lz", "wb")
ofile.write(enc)
ofile.close()