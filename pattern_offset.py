import sys

if len(sys.argv) != 3:
	print "Usage: python pattern_offset.py [number of bytes in original patten] [string]"
	exit(0)

cap_letters 	= ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
low_letters	= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
numbers 	= ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

i = 0
count = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0

string = ""

for i in range(0, int(sys.argv[1])):
	if count == 0:
		string += cap_letters[count1]
	
	elif count == 1:
		string += low_letters[count2]
	
	elif count == 2:
		string += cap_letters[count3]
	
	elif count == 3:
		string += numbers[count4]
	
	count += 1

	if count == 4:
		count = 0

		count4 += 1

		if count4 == len(numbers):
			count3 += 1
			count4 = 0

		if count3 == len(cap_letters):
			count2 += 1
			count3 = 0

		if count2 == len(low_letters):
			count1 += 1
			count2 = 0

offset = string.find(sys.argv[2])
print "Offset is " + str(offset) + " bytes in."
