import base64
#Source Text & Encode Info .
#Full Encode = 5806915943097005397
#Full Flag = PCTF{C4n_YOu_KnOw_Bas3X?}
#global encrypt
encrypt = hash("PCTF{C4n_YOu_KnOw_Bas3X?}".encode())
print (encrypt)
Get_len = len(str(encrypt)) /2
Get_len = int(Get_len)
dec = int(round(Get_len))
encrypt = str(encrypt)
print (dec)
c1_len = dec - 2
c2_len = dec + 2
c1 = encrypt[0:7]
print (c1)
c2 = encrypt[9::]
print (c2)
m1 = "PCTF{C4n_YOu_"
m2 = "_Bas3X?}"

char = [' ', '!', '"', '#', '$', '%', '&amp;', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '&lt;', '=', '&gt;', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
for i in char:
    for j in char:
        for k in char:
            for l in char:
                text = m1 + i + j + k + l + m2
                result = hash(text.encode())
                result = str(result)
                if result.startswith(str(c1)) and result.endswith(str(c2)):
                    print ("\n\n")
                    print(' [+] Find  Key : ' + result)
                    print (" [+] Find Str : " + text)
input()