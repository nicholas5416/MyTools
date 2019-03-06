from base64 import *
import random
result = {
    '16':lambda x:b16encode(x),
    '32':lambda x:b32encode(x),
    '64':lambda x:b64encode(x),
    }
flag = b"nctf{Can_You_Know_Base_X?}"
for i in range(10):
	a = random.choice(['16', '32' ,'64'])
	flag = result[a](flag)

with open("code.txt","wb") as f:
	f.write(flag)
input()