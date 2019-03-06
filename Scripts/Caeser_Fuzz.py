from pycipher import Caesar
for i in range(1,128):
	str_result = Caesar(key=i).decipher('gmbh{4d850d5c3c2756f67b91cbe8f046eebd}')
	print (" [" + str(i) + "] " + str_result + '\n')
input()
