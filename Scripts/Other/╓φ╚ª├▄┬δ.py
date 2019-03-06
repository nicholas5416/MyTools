import sys

def pigpen_chiper(letter):
    a = "abcdefghistuv"
    b = "jklmnopqrwxyz"
    if letter.isalpha():
        if letter in a:
            n = a.find(letter)
            pig = b[n]
        else:
            n = b.find(letter)
            pig = a[n]
        return pig
    else:
        return letter

def pigpen(word):
    """
     pigpen chiper
    """
    res = ''
    for letter in word:
        res += pigpen_chiper(letter)
    return res

if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print ("Pigpen_chiper decode 猪圈密码解密器v1.0 BY 0h1in9e")
        print ("Usage: "+sys.argv[0]+" 'ocjp{zkii}'")
    else:
    """
    print (pigpen("ocjp{zkirjwmo-ollj-nmlw-joxi-tmolnrnotvms}"))