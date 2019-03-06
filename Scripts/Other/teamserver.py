import os
import sys
osverinfo = os.uname()
print osverinfo
ifconfig = raw_input("Local IP :")
rpc = str("/usr/share/metasploit-framework/msfrpc -U msf -P password -S -a " + ifconfig + " 55553")
angel = str("/usr/bin/teamserver " + ifconfig + " password")
os.system("msfdb start")
os.system(rpc)
os.system(angel)
