
ifile = open("all_symbols.txt", "r", encoding='utf-8')
m = ifile.read()
ifile.close()

dict_file = open("latex_dict.txt", "r")
latex_commands = dict_file.readlines()
dict_file.close()

for i in range(len(latex_commands)):
	latex_commands[i] = latex_commands[i].replace("\n", "")
	latex_commands[i] = latex_commands[i].replace("\r", "")

allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

to_add = []

v = ""
for i in range(len(m)):
	if m[i] == "\\":
		if len(v) > 2 and v not in latex_commands:
			to_add.append(v)
		v = m[i]
	elif len(v) > 0 and m[i] in allowed:
		v += m[i]
	elif len(v) > 0 and v not in latex_commands:
		if len(v) > 2:
			to_add.append(v)
		v = ""

print(len(to_add))

ofile = open("latex_dict.txt", "a+")
for i in to_add:
	ofile.write(i + "\n")
ofile.close()