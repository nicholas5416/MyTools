import hashlib
#IceCTF{Can_You_Know_MD5}
#3d6574e29ba99dffc7930c3ddbef2f30


def getmd5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()
#Match Str List .
char = [' ', '!', '"', '#', '$', '%', '&amp;', '\'', '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '&lt;', '=', '&gt;', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
#For Match Str , Calc Text To MD5 . Get FLAG !
str_1 = 'IceCTF'
str_2 = 'Can'
str_3 = 'You'
str_4 = 'Know_MD5}'
try:
    for i in char:
        for j in char:
            for k in char:
                text = str_1 + i  + str_2 + j + str_3 + k + str_4
                md5value = getmd5(text)
                #print (md5value)
                #MD5 start To End.
                if md5value.startswith('3d6574e29ba') and md5value.endswith('f2f30'):
                    result = text
                    print (" ")
                    print(' [+] Find MD5 Key : ' + md5value)
                    print (" [+] Find MD5 Str : " + result)
                    print (" ")
except:
    print (" [-] Over Time ! ")