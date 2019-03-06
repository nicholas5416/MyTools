from base64 import b64encode, b64decode
from Cryptodome.Cipher import DES

k2 = [0x6E, 0x06, 0x15, 0x51, 0x93, 0x5B, 0x07, 0xEA]
key = bytes(k2)
x = DES.new(key, DES.MODE_ECB)
s = b"GcDk0SvnNA1tsmp5FCK1FpSDfUXZbhHBSPheZaixuMyzqyysOAPCPB/p7sMpmK1KZo+lPfhMZxw="
c = b64decode(s)# 解密
p = x.decrypt(c)# 还原奇偶字符
x = b64decode(p)
y = b64decode(p[28:-4])
for i in range(37):
    if(i%2==0):
        print(chr(x[i//2]), end='')
    else:
        print(chr(y[i//2]), end='')
