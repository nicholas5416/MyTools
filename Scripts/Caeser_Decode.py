# Caesar Cipher
import os
MAX_KEY_SIZE = 128
#mode = "e"
mode = "d"
os.system("echo [+] Cipher_Fuzzer Log_File > Cipher_Fuzzer.log")
cipher = src
key = 0
 
def getTranslatedMessage(mode, message, key):
        if mode[0] == 'd':
            key = -key
        translated = ''
 
        for symbol in message:
            if symbol.isalpha():
                num = ord(symbol)
                num += key
 
                if symbol.isupper():
                    if num > ord('Z'):
                        num -= 26
                    elif num < ord('A'):
                        num += 26
                elif symbol.islower():
                    if num > ord('z'):
                        num -= 26
                    elif num < ord('a'):
                        num += 26
                translated += chr(num)
            else:
                translated += symbol
        return translated
 
message = cipher
if mode[0] == 'e':
    print(getTranslatedMessage(mode, message, key))
else:
    for key in range(1,MAX_KEY_SIZE + 1):
        try:
            caeser_result = getTranslatedMessage('decrypt',message,key)
            #print(key,caeser_result)
            f = open("Cipher_Fuzzer.log","a")
            f.write(" [" + str(key) + "]   " + str(caeser_result) + "\n")
            f.close()
        except:
            run = " "