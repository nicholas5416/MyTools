# -*- coding:utf-8 -*-
import base64
import binascii
f=open("known.txt",'r')
c="CzVrT1wCdFoUBARGMgYgN3McVkFDQzIINxUjPD8qIi0=".decode("base64")
str=f.readline()
strset=str.split(":")
i=0
plain=""
cipher=""
while True:
    str=f.readline()
    if str=="":
        break    
    strs=str.split(":")
    plain+=strs[0]
    cipher+=base64.b64decode(strs[1])
f.close()
plain_list=list(plain)
cipher_list=list(cipher)

for i in range(0, len(str(plain):
        print (ord(plain_list[i])^ord(cipher_list[i]))
xor=[74, 70, 75, 54, 51, 119, 84, 49, 122, 107, 115, 102, 70, 110, 65, 67, 83, 100, 57, 51, 99, 53, 87, 122,78, 53, 80, 85, 82, 90, 78, 72]
print '*********************************************32位的循环的数组是********************************'
print (xor)
print '***************************************明文是*********************************'
for k in range(0,len(c)):
    c_list = list(c)
    print (chr(ord(c_list[k])^xor[k]))
