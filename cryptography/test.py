import time

ifile = open("words.txt", "r")
m = ifile.readlines()
ifile.close()

for i in range(len(m)):
	m[i] = m[i][:-1]

ofile = open("word_combinations.txt", "w")

start = time.time()
for i in range(len(m)):
	if i > 0:
		print(time.time() - start)
		exit()
	for j in range(len(m)):
		for k in range(len(m)):
			combination = m[i] + "." + m[j] + "." + m[k]
			if len(combination) <= 16:
				ofile.write(combination + "\n")