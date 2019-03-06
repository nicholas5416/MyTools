#!/usr/bin/env python3
import cv2
import socket
skt = socket.socket()
skt.bind(('127.0.0.1', 4444))
skt.listen(5)
peer = skt.accept()
print (peer)
#cv2.namedWindow('Video')


while 1:
    try:
        buffer = skt.recv(2048)
        print (buffer)
        #if not buffer:
        #    cv2.imshow("Video", buffer)
    except:
        error = " "

#cv2.destroyWindow('Video')
video_capture.release()
input()


