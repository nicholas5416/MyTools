from base64 import *
import base64
code = input()
for i in range(10):
    try:
        code = base64.b16decode(code)
    except:
        try:
            code = base64.b32decode(code)
        except:
            code = base64.b64decode(code)
print ("\n\n\n")
print (code)
input()