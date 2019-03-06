# Embedded file name: encrypt.py
from random import randint
from math import floor, sqrt
_ = ''
__ = "_"
____ = [ ord(___) for ___ in __ ]
_____ = randint(65, max(____)) * 255
for ___ in range(len(__)):
    _ += str(int(floor(float(_____ + ____[___]) / 2 + sqrt(_____ * ____[___])) % 255)) + ' '

print (_)