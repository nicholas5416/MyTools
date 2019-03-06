import itchat
from itchat import *
from itchat.content import *
import time
import os
import sys
itchat.auto_login(enableCmdQR=True)
"""
user = itchat.search_friends("NiceName")
username = user[0]['UserName']
print(username)
"""
#itchat.send('Test To Send Text !', toUserName=username)
try:
	@itchat.msg_register(itchat.content.TEXT)
	def main(msg):
		print (msg['Text'])
		inside = msg['Text']
		defs = inside[0:4]
		if  defs == "Exec":
			commands = inside[5::]
			recv = os.popen(str(commands)).readlines()
			itchat.send(str(recv), toUserName="filehelper")
		else:
			itchat.send('Session Exec : ' + inside, toUserName="filehelper")
		if defs == "Quit":
			exit()

	itchat.run()
except:
	itchat.send('Error !', toUserName="filehelper")
itchat.logout()