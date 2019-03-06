#=======================================================================#
#Import Modules .
#=======================================================================#
import base64
from base64 import *
import codecs
from codecs import *
import binascii
import os
import sys
from bubblepy import BubbleBabble
import threading
#=======================================================================#
#Log Module .
#=======================================================================#
a85_info = ""
b16_info = ""
b32_info = ""
b64_info = ""
b85_info = ""
hex_str_info = ""
standard_b64_info = ""
url_b64_info = ""
Decimal_info = ""
Reverse_info = ""
os.system("echo [+] Cipher_Fuzzer Log_File > Cipher_Fuzzer.log")
os.system("echo [+] Cipher_Patch Log_File > Cipher_Patch.log")
#=======================================================================#
#Cipher Text .
#=======================================================================#
#Bacon
A = "aaaaa"
B = "aaaab"
C = "aaaba"
D = "aaabb"
E = "aabaa"
F = "aabab"
G = "aabba"
H = "aabbb"
I = "abaaa"
J = "abaab"
K = "ababa"
L = "ababb"
M = "abbaa"
N = "abbab"
O = "abbba"
P = "abbbb"
Q = "baaaa"
R = "baaab"
S = "baaba"
T = "baabb"
U = "babaa"
V = "babab"
W = "babba"
X = "babbb"
Y = "bbaaa"
Z = "bbaab"


#=======================================================================#
#DeCrypto Func .
#=======================================================================#

def a85():
    try:
        a85 = str(base64.a85decode(src))
        a85 = a85[2:-1]
        print (" [+] A85 To str :          ==  " + a85)
    except:
        a85_info = "error"
        print (" [-] Not A85 . ")
    show_info()
    
def b16():
    try:
        b16 = str(base64.b16decode(src))
        b16 = b16[2:-1]
        print (" [+] B16 To str :          ==  " + b16)
    except:
        b16_info = "error"
        print (" [-] Not B16 . ")
    show_info()

def b32():
    try:
        b32 = str(base64.b32decode(src))
        b32 = b32[2:-1]
        print (" [+] B32 To str :          ==  " + b32)
    except:
        b32_info = "error"
        print (" [-] Not B32 . ")
    show_info()

def b64():
    try:
        b64 = str(base64.b64decode(src))
        b64 = b64[2:-1]
        print (" [+] B64 To str :          ==  " + b64)
    except:
        b64_info = "error"
        print (" [-] Not B64 . ")
    show_info()

def b85():
    try:
        b85 = str(base64.b85decode(src))
        b85 = b85[2:-1]
        print (" [+] B85 To str :          ==  " + b85)
    except:
        b85_info = "error"
        print (" [-] Not B85 . ")
    show_info()

def standard_b64():
    try:
        standard_b64 = str(base64.standard_b64decode(src))
        standard_b64 = standard_b64[2:-1]
        print (" [+] Standard_B64 To str : ==  " + standard_b64)
    except:
        standard_b64_info = "error"
        print (" [-] Not Standard_B64 . ")
    show_info()

def url_b64():
    try:
        url_b64 = str(base64.urlsafe_b64decode(src))
        url_b64 = url_b64[2:-1]
        print (" [+] Url_B64 To str :      ==  " + url_b64)
    except:
        url_b64_info = "error"
        print (" [-] Not Url_B64 . ")
    show_info()

def bb():
    try:
        bb = BubbleBabble()
        bbre = bb.decode(str(src))
        print (" [+] Bubble Babble :      ==  " + str(bbre)[2:-1])
    except:
        bb_str_info = "error"
        print (" [-] Not Bubble Babble . ")
    show_info()
def hex():
    try:
        src_new = src.upper()
        hex_str = str(base64.b16decode(src_new))
        hex_str = hex_str[2:-1]
        print (" [+] hex To str :          ==  " + hex_str)
    except:
        hex_str_info = "error"
        print (" [-] Not Hex . ")
    show_info()

def Decimal():
    try:
        Decimal = chr(int(src))
        Decimal = str(Decimal)
        print (" [+] Decimal To str :      ==  " + Decimal)
    except:
        Decimal_info = "error"
        print (" [-] Not Decimal . ")
    show_info()

def Reverse():
    try:
        Reverse = src[::-1]
        print (" [+] Reverse To str :      ==  " + Reverse)
    except:
        Reverse_info = "error"
        print (" [-] Not Reverse . ")
    show_info()

def Bacon():
    try:
        loop = 4
        Bacon = ""
        gen_src =  src.lower()
        while (loop > 0):
            five = gen_src[0:5]
            if five == A:
                Bacon += "A" 
                gen_src = gen_src[5::]
            elif five == B:
                Bacon += "B"
                gen_src = gen_src[5::]
            elif five == B:
                Bacon += "B"
                gen_src = gen_src[5::]
            elif five == C:
                Bacon += "C"
                gen_src = gen_src[5::]
            elif five == D:
                Bacon += "D"
                gen_src = gen_src[5::]
            elif five == E:
                Bacon += "E"
                gen_src = gen_src[5::]
            elif five == F:
                Bacon += "F"
                gen_src = gen_src[5::]
            elif five == G:
                Bacon += "G"
                gen_src = gen_src[5::]
            elif five == H:
                Bacon += "H"
                gen_src = gen_src[5::]
            elif five == I:
                Bacon += "I"
                gen_src = gen_src[5::]
            elif five == J:
                Bacon += "J"
                gen_src = gen_src[5::]
            elif five == K:
                Bacon += "K"
                gen_src = gen_src[5::]
            elif five == L:
                Bacon += "L"
                gen_src = gen_src[5::]
            elif five == M:
                Bacon += "M"
                gen_src = gen_src[5::]
            elif five == N:
                Bacon += "N"
                gen_src = gen_src[5::]
            elif five == O:
                Bacon += "O"
                gen_src = gen_src[5::]
            elif five == P:
                Bacon += "P"
                gen_src = gen_src[5::]
            elif five == Q:
                Bacon += "Q"
                gen_src = gen_src[5::]
            elif five == R:
                Bacon += "R"
                gen_src = gen_src[5::]
            elif five == T:
                Bacon += "T"
                gen_src = gen_src[5::]
            elif five == U:
                Bacon += "U"
                gen_src = gen_src[5::]
            elif five == V:
                Bacon += "V"
                gen_src = gen_src[5::]
            elif five == W:
                Bacon += "W"
                gen_src = gen_src[5::]
            elif five == X:
                Bacon += "X"
                gen_src = gen_src[5::]
            elif five == Y:
                Bacon += "Y"
                gen_src = gen_src[5::]
            elif five == Z:
                Bacon += "Z"
                gen_src = gen_src[5::]
            else:
                last = "last"
            loop = loop -1
        print (" [+] Bacon   To str :      ==  " + Bacon)
    except:
        print (" [-] Not Bacon .")
        Bacon_str_info = "error"
    show_info()

def Rot13():
    try:
        Rot13 = codecs.decode(src,'rot13')
        print (" [+] Rot13   To str :      ==  " + Rot13)
    except:
        print (" [-] Not Rot13 . ")
        rot13_str_info = "error"
    show_info()

def Bin():
    bin_cont = len(src) /8
    bin_src = src
    dec_str = ""

    try:
        while (bin_cont > 0):
            bin_src = bin_src
            bin_head = bin_src[0:8]
            #print (bin_head)
            #8位
            Bin_output = str(int(bin_head, base=2))
            #print (Bin_output)
            #73
            bin_src = bin_src[8::]
            #print (bin_src)
            #ok
            dec_str += chr(int(Bin_output))
            #print (dec_str)
            bin_cont = bin_cont -1
            #26 or 102
            #Bin To Decimal .
            #Decimal To Str .
        print (" [+] Bin     To str :      ==  " + dec_str)
    except:
        print (" [-] Not Bin . ")
        bin_str_info = "error"
    show_info()

def unicode():
    try:
        unicode_ =  (src.encode('utf-8').decode('unicode_escape'))
        print (" [+] Unicode To str :      ==  " + unicode_)
    except:
        print (" [-] Not Unicode . ")
        unicode_str_info = "error"
    show_info()


#=======================================================================#
#Caeser Module .
#=======================================================================#

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
 
def Caeser():
    MAX_KEY_SIZE = 130
    #mode = "e"
    mode = "d"
    key = 0
    cipher = src
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

#=======================================================================#
#Patch Module .
#=======================================================================#

def patch():
    cont = 0
    code = src
    while (cont < 20):
        try:
            code = base64.b16decode(code)
            f = open("Cipher_Patch.log","a")
            f.write(str(code) + "\n")
            f.close()
        except:
            try:
                code = base64.b32decode(code)
                f = open("Cipher_Patch.log","a")
                f.write(str(code) + "\n")
                f.close()
            except:
                not_b32 = " "
                try:
                    code = base64.b64decode(code)
                    f = open("Cipher_Patch.log","a")
                    f.write(str(code) + "\n")
                    f.close()
                except:
                    not_b64 = " "
        cont = cont + 1

#=======================================================================#
#Inside Messages .
#=======================================================================#
def show_info():
    print ("    ")

def help_info():
    print (" If Not You Want , Please Try MD5 .")
    show_info()

def banner():
    print ("    ")
    print (" Cipher Fuzzer . ")
    print ("    ")

#=======================================================================#
#Framework.
#=======================================================================#
banner()
while 1:
    src = input(" Src Cipher Text : ")
    src = str(src)
    show_info()
    t0 = threading.Thread(target=a85)
    t1 = threading.Thread(target=b16)
    t2 = threading.Thread(target=b32)
    t3 = threading.Thread(target=b64)
    t4 = threading.Thread(target=b85)
    t5 = threading.Thread(target=standard_b64)
    t6 = threading.Thread(target=url_b64)
    t7 = threading.Thread(target=bb)
    t8 = threading.Thread(target=hex)
    t9 = threading.Thread(target=Decimal)
    t10 = threading.Thread(target=Reverse)
    t11 = threading.Thread(target=Caeser)
    t12 = threading.Thread(target=Rot13)
    t13 = threading.Thread(target=Bacon)
    t14 = threading.Thread(target=Bin)
    t15 = threading.Thread(target=unicode)
    t16 = threading.Thread(target=patch)
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()

    show_info()
    print ("#=======================================================================#")
    help_info()
#=======================================================================#
#Info.
#=======================================================================#

        #Src int is hex (int) , to 10 ,chr() recovery .
        #chr() 还原
        #ord() 10进制
        #src[0] * 16 + src[1] = \x41  4 * 16 + 1
        #hex() 16进制
    
    
    """
    try:
        src = src.upper()
        hex_patch = ""
        hex_patch_des = ""
        i = 0
        while (i < 64):
            decode = src[0:2]
            print (decode) #66
            intdecode = int(decode)
            hex_patch = str(base64.b16decode(decode))
            print (hex_patch) #b'f'
            num = len(src) - 2
            print (num)
            if num != 0:
                src = src[-num:]
                print (src) #4161
                hex_patch_des += hex_patch[2:-1]
            else:
                hex_patch_des += hex_patch[2:-1]
            print (hex_patch_des)
            i = i +1
        print (" [+] Hex Patch To Str : ==  "+ hex_patch_des)
    except:
        print (" [-] Not Hex Can Not To Str . ")
    print ("    ")
    """


    """
def Caeser():
    key = 0
    mode = "decrypt"
    translated = ""
    Des = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Caeser_src = src.upper()
    for symbol in Caeser_src:
        if symbol in Des:
            num = Des.find(symbol)
            if mode == "encrypt":
                num = num + key
            elif mode == "decrypt":
                num = num - key
            if num >= len(Des):
                num = num - len(Des)
            elif num < 0:
                num = num + len(Des)
            translated = translated + symbol
    translated = translated.lower()
    print (translated)
"""
