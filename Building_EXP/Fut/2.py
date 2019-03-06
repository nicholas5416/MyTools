# -*- coding=utf-8 -*-
# Author: LSHV
# Date: 2019 / 2 / 5
baidu_app_id = "11661012"
baidu_api_key = "DsTWniZ4oaVcsTL2AMwulevZ"
baidu_secret_key = "4M4eNyy1DncWrN7XrEAhfpyLFFnD6PjG"
baidu_access_token = ""
baidu_expires_in = ""
Turing_User_ID = "306894"
Turing_API_key = "d48c5b2b4a854d9dbc8db4cd675f1c26" 
Turing_API_address = "http://www.tuling123.com/openapi/api"
from pathlib import Path
import wave,time, sys, os, requests, argparse, io, threading, pycurl, uuid, base64, json, pyaudio, _thread, datetime
from urllib import request
from aip import AipSpeech
from playsound import playsound

def audio_record(out_file, rec_time):
    CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, # 音频流wav
                    channels=1, # 声道
                    rate=16000, # 采样率
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
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
    baidu_access_token = json_data['access_token']
    return baidu_access_token
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
        print (wav_ret_text)
        return wav_ret_text
    except:
        null = " "

audio_record("./src.wav",5)
wav_to_text()