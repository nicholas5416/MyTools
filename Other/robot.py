# -*- coding=utf-8 -*-
# Author: Zero
# Date: 2018 / 9 / 1
#---------------------------------------------------------------------------#
#Import Modules .
#---------------------------------------------------------------------------#
from pathlib import Path
import wave,time, sys, os, requests, argparse, io, threading, pycurl, uuid, base64, json, pyaudio, _thread, datetime
from urllib import request
import aip
from aip import AipSpeech
import playsound
from playsound import playsound
#=======================================================================#
#Global Options .
#=======================================================================#
baidu_app_id = "11661012"
baidu_api_key = "DsTWniZ4oaVcsTL2AMwulevZ"
baidu_secret_key = "4M4eNyy1DncWrN7XrEAhfpyLFFnD6PjG"
baidu_access_token = ""
baidu_expires_in = ""
dump = ""
Turing_User_ID = "306894"
Turing_API_key = "d48c5b2b4a854d9dbc8db4cd675f1c26" 
Turing_API_address = "http://www.tuling123.com/openapi/api"

CHUNK = 1024 
FORMAT = pyaudio.paInt16 
RATE = 8000  
CHANNELS = 1 
RECORD_SECONDS = 5 
global wav_path
wav_path = "src.wav"
wav_ret_text = " "

#=======================================================================#
#Listen Info To Wav File .
#=======================================================================#
def record_wave():
    pa = pyaudio.PyAudio()
    stream = pa.open(format = FORMAT,
                     channels = CHANNELS,
                     rate = RATE,
                     input = True,
                     frames_per_buffer = CHUNK)
    print(" [+] Listening .")
    save_buffer = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        audio_data = stream.read(CHUNK)
        save_buffer.append(audio_data)
    print(" [+] Sending .")
    stream.stop_stream()
    stream.close()
    pa.terminate()
    # wav path
    wf = wave.open(wav_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    # 注意join 前的类型，如果是str类型会出错
    wf.writeframes(b''.join(save_buffer))
    wf.close()

#=======================================================================#
#Wav Info To Text .
#=======================================================================#

def get_mac_address():
    return uuid.UUID(int=uuid.getnode()).hex[-12:]
    # 获取百度token
def get_access_token():
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=ZrjLfF5Rh7pOL66gaOmDGnXn&client_secret=16bac9645093ca2632ebb81015ff7544"
    req = request.Request(url, method="POST")
    resp = request.urlopen(req)
    data = resp.read().decode('utf-8')
    json_data = json.loads(data)
    global bda_access_token
    bda_access_token = json_data['access_token']
    return bda_access_token
# 读取wav文件内容
CHUNK = 1024
def get_wav_data(wav_path):
    if wav_path is None or len(wav_path) == 0:
        return None
    # 使用"rb"(二进制模式)打开文件
    wav_file = wave.open(wav_path, 'rb')
    nframes = wav_file.getnframes()
    audio_data = wav_file.readframes(nframes)
    wav_file.close()
    return audio_data, nframes
# 解析返回值
def dump_res(buf):
    resp_json = json.loads(buf.decode('utf-8'))
    global wav_ret_text
    try:
        ret = resp_json['result']
        wav_ret_text = ret[0]
    except:
        wav_ret_text = " "
    #print(buf)
def wav_to_text():
    try:
        wav_path = "src.wav"
        if wav_path is None or len(wav_path) == 0:
            return None
        if len(baidu_access_token) == 0:
            get_access_token()
            if len(baidu_access_token) == 0:
                return None
        data, f_len = get_wav_data(wav_path)
        url = 'http://vop.baidu.com/server_api?cuid=' + get_mac_address() + '&token=' + baidu_access_token
        # 必须是list，不能是dict
        http_header = [
            'Content-Type: audio/pcm; rate=8000',
            'Content-Length: %d' % f_len
        ]
        c = pycurl.Curl()
        # url
        c.setopt(pycurl.URL, str(url)) 
        # header
        c.setopt(c.HTTPHEADER, http_header) 
        # Method
        c.setopt(c.POST, 1) 
        # 连接超时时间
        c.setopt(c.CONNECTTIMEOUT, 30) 
        # 请求超时时间
        c.setopt(c.TIMEOUT, 30)
        # 返回信息回调
        c.setopt(c.WRITEFUNCTION, dump_res)
        # post 的信息
        c.setopt(c.POSTFIELDS, data)
        # post的信息长度
        c.setopt(c.POSTFIELDSIZE, f_len)
        c.perform() 
        return wav_ret_text
    except:
        null = " "

#---------------------------------------------------------------------------#
#Text To Music .
#---------------------------------------------------------------------------#
client = AipSpeech(baidu_app_id, baidu_api_key, baidu_secret_key)
def text_to_music(response):
    try:
        os.mkdir("lib")
    except:
        null = " "
    result  = client.synthesis(response, 'zh', 1, {
        'vol': 5,
    })

    if not isinstance(result, dict):
        mp =  open("lib/" + value + ".mp3", 'wb')
        mp.write(result)
        mp.close()
    playsound("lib/" + value + ".mp3")

#---------------------------------------------------------------------------#
#Import tuling API , TEXT Ret TEXT && Main Func .
#---------------------------------------------------------------------------#
while 1:
    value = str(time.time())
    print (time.clock)
    t0 = threading.Thread(target=record_wave)
    t0.start()
    print (time.clock)
    t1 = threading.Thread(target=wav_to_text)
    t1.start()
    print (wav_ret_text)
    r = requests.post(
        Turing_API_address, 
        json = {
        "key": Turing_API_key,
        "info": wav_ret_text, 
        "loc": "吴忠市", 
        "userid":User_ID
        })
    response = r.json()["text"]
    print (response)
    text_to_music(response)
    os.remove("lib/" + value + ".mp3")





            