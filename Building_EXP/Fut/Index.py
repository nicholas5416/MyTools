import os, sys
from PIL import ImageGrab
IMAGE = ImageGrab.grab()


while True:
    Commands = input(" >")
    if Commands == "shell":
        shell = 1
        while shell == 1:
            shell_put = input(" >")
            if shell_put == "exit":
                shell = 0
            os.system(shell_put)
    elif Commands == "desktop":
        IMAGE.save('./desktop.jpeg','jpeg')


            


