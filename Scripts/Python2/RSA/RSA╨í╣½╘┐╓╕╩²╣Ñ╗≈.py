# coding=utf-8
import gmpy2
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes

with open('extremelyhardRSA/pubkey.pem', 'r') as f:
    key = RSA.importKey(f)
    N = key.n
    e = key.e
with open('extremelyhardRSA/flag.enc', 'r') as f:
    cipher = f.read().encode('hex')
    cipher = int(cipher, 16)

# 爆破出来值为118719488
for i in range(118000000, 120000000):
    if gmpy2.iroot(cipher + i * N, 3)[1]:
        print long_to_bytes(gmpy2.iroot(cipher + i * N, 3)[0])
# Didn't you know RSA padding is really important? Now you see a non-padding message is so dangerous. And you should notice this in future.Fl4g: PCTF{Sm4ll_3xpon3nt_i5_W3ak}
