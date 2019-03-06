import os
char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for a in char:
	for b in char:
		for c in char:
			for d in char:
				for e in char:
					for f in char:
						for g in char:
							for h in char:
								os.system("echo " + a + b +c + d +e + f + g + h + " >> 8wei.txt")
print ("char Over.")
input()
#每位数字有8种可能，就是10**8
