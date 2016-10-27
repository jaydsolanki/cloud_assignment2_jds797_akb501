import sys
f = open(sys.argv[1])
for i in f:
	if "\"coordinates\":[" in i:
		print (i) 
f.close()
