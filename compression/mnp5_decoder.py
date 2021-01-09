ifile = open("rle_compressed.lz", "rb")
enc = ifile.read()
ifile.close()

dec = bytearray()