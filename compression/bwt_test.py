ifile = open("bwt_test.txt", "wb")

m = bytes("\x00\xffte\x00st")

m += b"\x00"
print(m)