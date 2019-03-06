import os
Win_list = ['formatstring','rsa','pydub','pathlib','wave','datetime','pyaudio','argparse','uuid','json','pycurl','pyinstaller','bubblepy','numpy','opencv_python']
Lin_list = ['pwntools','rsa','formatstring',"pypinyin","pydub","pathlib","wave","datetime","pyaudio","argparse","uuid","json","pycurl","one_gadget",'opencv_python']

if os.name == "nt":
    for DPK in Win_list:
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple " + str(DPK))
        except:
            null = ""
else:
    for DPK in Lin_list:
        try:
            os.system("pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple " + str(DPK))
        except:
            null = ""