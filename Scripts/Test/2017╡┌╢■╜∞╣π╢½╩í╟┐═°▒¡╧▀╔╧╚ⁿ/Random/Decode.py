from random import randint

from math import floor, sqrt

 

ANSInum = [i for i in range(33,127)]

flagEnc=[208,140,149,236,189,77,193,104,202,184,97,236,148,202,244,199,77,122,113]

for k in range(65*255,127*255,255)

    tmpDict={}

    for i in range(len(ANSInum)):

        tmpInt = int(floor(float(k + ANSInum[i])  /2 + sqrt(k * ANSInum[i])) % 255)

        tmpDict[tmpInt] = chr(ANSInum[i])

    try

        flag=''.join([tmpDict[i] for i in flagEnc])

        print 'flag{' + flag + '}'

    except

        pass