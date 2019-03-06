lstr = 'gmbh{4d850d5c3c2756f67b91cbe8f046eebd}'
str1 = ""
for p in range(127): 
	for i in lstr: 
		temp = chr((ord(i)+p)%127) 
		if 32<ord(temp)<127 : 
			str1 = str1 + temp 
			feel = 1 
		else: 
			feel = 0 
			break 
		if feel == 1: 
			print ("    ")
			print(str1) 
			print ("    ")
