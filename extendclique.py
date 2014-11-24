import sys
import CliqueCritique
delta = int(sys.argv[1]) 

for line in sys.stdin:
	contents = line.split(" ")
	print contents[3]
	if str(contents[3]) is not 'None':
		if int(contents[2])<=delta and delta < int(contents[3]):
			print contents
	elif int(contents[2])<=delta:
		print contents
