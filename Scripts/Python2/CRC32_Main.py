from crc32_5byte import 

l = [0x20AE9F17,
     0xD2D0067E,
     0x6C53518D,
     0x80DF4DC3,
     0x3F637A50,
     0xBCD9703B]

for k in l
    crc32_reverse(k, 5)

"""
这么多重合的crc32，巨坑，手动一个一个试，最后得到

password:f~Z-;lapEwF\<0ZkhyAo5

解压rar得到flag

XUSTCTF{6ebd0342caa3cf39981b98ee24a1f0ac}"""
