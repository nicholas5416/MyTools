#-*-coding=utf-8-*-
import execjs
from execjs import *
#======================================#
# Load JavaScript Modules.
with open("bilibili.js",'r', encoding='UTF-8') as f:
    Js_Exec = f.read()
bilibili = execjs.compile(str(Js_Exec))
with open("kugou.js","r") as f:
    Js_Exec = f.read()
kugou = execjs.compile(str(Js_Exec))
with open("kuwo.js","r") as f:
    Js_Exec = f.read()
kuwo = execjs.compile(str(Js_Exec))
with open("netease.js","r") as f:
    Js_Exec = f.read()
netease = execjs.compile(str(Js_Exec))
with open("qq.js","r") as f:
    Js_Exec = f.read()
qq = execjs.compile(str(Js_Exec))
with open("xiami.js","r") as f:
    Js_Exec = f.read()
xiami = execjs.compile(str(Js_Exec))
#======================================#
# 
ret = bilibili.call("bilibili")
print (ret)
