from Crypto.Cipher import AES
key = 'PHRACK-BROKENPIC'
aes = AES.new(key)

with open('brokenpic.bmp', 'r') as f:
    data = f.read()
    pic = aes.decrypt(data)

with open('2.bmp', 'w') as f:
    f.write(pic)
