# -*- coding: utf-8 -*-
from flask import *
import requests, urllib, json, os, sys, threading, time
app = Flask(__name__)
#========================================================#
mv_lists_page = """
<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>Musics</title> 
<style type="text/css">
body {
    background-image: url();
    margin-left: 0px;
    margin-top: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    background-repeat: repeat;
}
body,td,th {
    color: #000000;
}
</style>
</head>
<body leftmargin="0" topmargin="0" marginwidth="1920" marginheight="1080">
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <th height="47" colspan="2" align="center" valign="middle" scope="col"><p><strong><em><a href="/">
        <p1>主页</p1>
      </a></em></strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="/re/">刷新</a></p></th>
    </tr>
    <tr>
      <td width="50%" height="25" align="left" valign="middle"><strong><em>SongName :</em></strong></td>
      <td width="50%" align="left" valign="middle"><strong><em>Singer:</em></strong></td>
"""
music_lists_page = """
<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>Musics</title> 
<style type="text/css">
body {
    background-image: url();
    margin-left: 0px;
    margin-top: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    background-repeat: repeat;
}
body,td,th {
    color: #000000;
}
</style>
</head>
<body leftmargin="0" topmargin="0" marginwidth="1920" marginheight="1080">
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <th height="47" colspan="2" align="center" valign="middle" scope="col"><p><strong><em><a href="/">
        <p1>主页</p1>
      </a></em></strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="/re/">刷新</a></p></th>
    </tr>
    <tr>
      <td height="25" align="left" valign="middle"><strong><em>SongName :</em></strong></td>
      <td align="left" valign="middle"><strong><em>Singer:</em></strong></td>
    </tr>
"""
music_player = """
<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>Musics</title> 
<style type="text/css">
body {
    background-image: url();
    margin-left: 0px;
    margin-top: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    background-repeat: no-repeat;
}
body,td,th {
    color: #000000;
}
</style>
</head>
<body leftmargin="0" topmargin="0" marginwidth="1920" marginheight="1080">
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <th height="47" colspan="3" align="center" valign="middle" scope="col"><a href="/">
        <p1><strong><em>主页</em></strong></p1>
      </a></th>
    </tr>
    <tr>
      <td width="42%" height="25" align="center" valign="middle"><strong><em>SongName :</em></strong></td>
      <td width="24%" align="center" valign="middle"><strong><em>Singer :</em></strong></td>
      <td width="34%" align="center" valign="middle"><strong><em>Media:</em></strong></td>
    </tr>
"""
mv_player = """
<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>Mvs</title> 
<style type="text/css">
body {
    background-image: url();
    margin-left: 0px;
    margin-top: 0px;
    margin-right: 0px;
    margin-bottom: 0px;
    background-repeat: no-repeat;
}
body,td,th {
    color: #0F0E0E;
    font-size: medium;
}
</style>
</head>
<body leftmargin="0" topmargin="0" marginwidth="1920" marginheight="1080">
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <th height="47" colspan="4" align="center" valign="middle" scope="col"><a href="/">
        <p1><strong><em>主页</em></strong></p1>
      </a></th>
    </tr>
"""









#========================================================#
def Netease_Search_API(Keywords):
    global songnames, singers, srcs, photo
    word = Keywords
    Resources = []
    singers = []
    songnames = []
    srcs = []
    photo = []
    try:
        res1 = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&type=song&limit=100&offset=0')
        jm1 = json.loads(res1.text.strip('callback()[]'))
        jm1 = jm1['data']
        for all_list in jm1:
            Resources.append(all_list)
        for in_list in Resources:
            singers.append(in_list['singer'])
            songnames.append(in_list['name'])
            srcs.append(in_list['url'])
            photo.append(in_list['pic'])
    except:
        print (" [-] Null!")

def QQ_Search_API(Keywords):
    global songnames, singers, srcs, photo
    word = Keywords
    Resources = []
    singers = []
    songnames = []
    srcs = []
    photo = []
    try:
        res1 = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s='+ word + '&limit=100&offset=0&type=song')
        jm1 = json.loads(res1.text.strip('callback()[]'))
        jm1 = jm1['data']
        for all_list in jm1:
            Resources.append(all_list)
        for in_list in Resources:
            songnames.append(in_list['name'])
            singers.append(in_list['singer'])
            srcs.append(in_list['url'])
            photo.append(in_list['pic'])
    except:
        print (" [-] Null!")

def QQ_MV_API(Keywords):
    global songnames, singers, srcs, photo
    word = Keywords
    Resources = []
    singers = []
    songnames = []
    srcs = []
    photo = []
    try:
        res1 = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s=' + word + '&limit=100&offset=0&type=mv')
        jm1 = json.loads(res1.text.strip('callback()[]'))
        jm1 = jm1['data']
        for all_list in jm1:
            Resources.append(all_list)
        for in_list in Resources:
            songnames.append(in_list['mv_name'])
            singers.append(in_list['singer_name'])
            srcs.append("https://api.bzqll.com/music/tencent/mvUrl?key=579621905&id=" + in_list['v_id'] + '&r=4')
            photo.append(in_list['mv_pic_url'])
    except:
        print (" [-] Null!")
    
def Netease_MV_API(Keywords):
    global songnames, singers, srcs, photo
    word = Keywords
    Resources = []
    singers = []
    songnames = []
    srcs = []
    photo = []
    try:
        res1 = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&type=video&limit=100&offset=0')
        jm1 = json.loads(res1.text.strip('callback()[]'))
        jm1 = jm1['data']['videos']
        for all_list in jm1:
            Resources.append(all_list)
        for in_list in Resources:
            if len(str(in_list['vid'])) > 10:
                pass
            else:
                singers.append(in_list['creator'][0]['userName'])
                songnames.append(in_list['title'])
                srcs.append('https://api.bzqll.com/music/netease/mvUrl?key=579621905&id=' + in_list['vid'] + '&r=1080')
                photo.append(in_list['coverUrl'])
    except:
        print (" [-] Null!")

def Get_Music_List():
    global Music_List, Author_list
    Music_List = []
    Author_list = []
    Resources = []
    res1 = requests.get('https://api.bzqll.com/music/netease/hotSongList?key=579621905&cat=%E5%85%A8%E9%83%A8&limit=100&offset=0')
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']
    for all_list in jm1:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List.append(in_list['title'])
        Author_list.append(in_list['creator'])
        
    Resources = []
    res1 = requests.get('https://api.bzqll.com/music/netease/highQualitySongList?key=579621905&cat=%E5%85%A8%E9%83%A8&limit=100')
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']['playlists']
    for all_list in jm1:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List.append(in_list['title'])
        Author_list.append(in_list['creator'])
    Resources = []

    res1 = requests.get('https://api.bzqll.com/music/tencent/hotSongList?key=579621905&categoryId=10000000&sortId=3&limit=100')
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']
    for all_list in jm1:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List.append(in_list['name'])
        Author_list.append(in_list['creator'])

def Get_MV_List():
    global MVname, MVSingers
    MVname = []
    MVSingers = []
    Resources = []
    res1 = requests.get('https://api.bzqll.com/music/netease/topMvList?key=579621905&limit=10&offset=0')
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']
    for all_list in jm1:
        Resources.append(all_list)
    for in_list in Resources:
        MVname.append(in_list['name'])
        MVSingers.append(in_list['singer'])

    Resources = []
    res1 = requests.get('https://api.bzqll.com/music/tencent/hotMvList?key=579621905&year=0&tag=0&area=0&limit=100&offset=0')
    jm1 = json.loads(res1.text.strip('callback()[]'))
    jm1 = jm1['data']
    for all_list in jm1:
        Resources.append(all_list)
    for in_list in Resources:
        MVSingers.append(in_list['singer'])
        MVname.append(in_list['name'])
    

Get_MV_List()
Get_Music_List()
@app.route('/',methods=['GET','POST'])
def Main():
    Main_Html = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Music Web Site</title>
<style type="text/css">
body {
    background-image: url(https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1550440374221&di=ff0bd6f426fa2cd4df2297e972459a35&imgtype=0&src=http%3A%2F%2Fuploads.5068.com%2Fallimg%2F161205%2F68-1612051H454.jpg);
}
body,td,th {
    color: #FFFDFD;
}
</style>
</head>

<body>
<table width="100%" border="0" align="center" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td width="39%" height="56" align="right"><a href="/Music/">Music</a></td>
      <td width="22%" align="right"><a href="/Mv/">Mv</a></td>
      <td width="39%">&nbsp;</td>
    </tr>
    <tr>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
      <td>&nbsp;</td>
    </tr>
  </tbody>
</table>
</body>
</html>
'''
    return Main_Html


@app.route('/Mv/',methods=['GET','POST'])
def Mv_Main():
    Result_List = ""
    MVSingers_index = 0
    for Mv in MVname:
        Result_List += '''
    <tr>
      <td height="29" align="left" align="center" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="/MvSearcher/''' + Mv + '''">''' + Mv + '''</a></td>
      <td align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + MVSingers[MVSingers_index] + '''</td>
      <td align="left" valign="middle"></td>
    </tr>
'''
        MVSingers_index += 1
    Html_Top = '''
  </tbody>
</table>
</body>
</html>
'''
    return mv_lists_page + Result_List + Html_Top




@app.route('/Music/',methods=['GET','POST'])
def Music_Main():
    Result_List = ""
    Author_list_index = 0
    for Musics in Music_List:
        Result_List += '''
<tr>
    <td width="50%" height="25" align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="/MusicSearcher/''' + Musics + '''">''' + Musics + '''</a></td>
    <td width="50%" align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;''' + Author_list[Author_list_index] + '''</td>
</tr>
''' 
        Author_list_index += 1
    Html_Top = '''
    </tbody>
</table>
</body>
</html>
'''

    return music_lists_page + Result_List + Html_Top

@app.route('/re/',methods=['GET','POST'])
def re():
    t0 = threading.Thread(target=Get_Music_List)
    t1 = threading.Thread(target=Get_MV_List)
    t0.start()
    t1.start()
    time.sleep(3)
    return redirect(url_for('Music_Main'))
    return " [ OK ]"

@app.route('/MusicSearcher/<Str>',methods=['GET','POST'])
def MusicSearcher(Str):
    Musics_List = ""
    try:
        Netease_Search_API(Str)
        for i in range(0,1000):
            Musics_List += '''
<tr>
    <td height="29" align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>''' + songnames[i] + '''</em></td>
    <td align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>''' + singers[i] + '''</em></td>
    <td align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em><a href="''' + srcs[i]  +'''">
        <audio src="''' + srcs[i] + '''" controls="controls"></audio>
    </a></em></td>
</tr>
'''
    except:
        pass
    try:
        QQ_Search_API(Str)
        for i in range(0,1000):
            Musics_List += '''
<tr>
    <td height="29" align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>''' + songnames[i] + '''</em></td>
    <td align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>''' + singers[i] + '''</em></td>
    <td align="left" valign="middle">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em><a href="''' + srcs[i]  +'''">
        <audio src="''' + srcs[i] + '''" controls="controls"></audio>
    </a></em></td>
</tr>
'''
    except:
        pass
    Html_Top = '''
  </tbody>
</table>
</body>
</html>
    '''
    return music_player + Musics_List + Html_Top


@app.route('/MvSearcher/<Str>',methods=['GET','POST'])
def MvSearcher(Str):
    Musics_List = ""
    try:
        Netease_MV_API(Str)
        for i in range(0,1000):
            Musics_List += '''
<tr>
    <td width="28%" height="40" align="center" valign="middle"><strong><em>SongName :</em></strong></td>
    <td width="29%" align="center" valign="middle"><em>''' + songnames[i] + '''</em></td>
    <td width="9%" align="center" valign="middle"><strong><em>Singer :</em></strong></td>
    <td width="34%" align="center" valign="middle"><em>''' + singers[i] + '''</em></td>
</tr>
<tr>
    <td height="1080" colspan="1920" align="center" valign="middle"><em><a href="''' + srcs[i] + '''">
        <video width="100%" height="100%" controls="" name="media"><source src="''' + srcs[i] + '''" type="audio/mpeg"</video>
    </a></em></td>
</tr>
'''
    except:
        pass
    try:
        QQ_MV_API(Str)
        for i in range(0,1000):
            Musics_List += '''
<tr>
    <td width="28%" height="40" align="center" valign="middle"><strong><em>SongName :</em></strong></td>
    <td width="29%" align="center" valign="middle"><em>''' + songnames[i] + '''</em></td>
    <td width="9%" align="center" valign="middle"><strong><em>Singer :</em></strong></td>
    <td width="34%" align="center" valign="middle"><em>''' + singers[i] + '''</em></td>
</tr>
<tr>
    <td height="1080" colspan="1920" align="center" valign="middle"><em><a href="''' + srcs[i] + '''">
        <video width="100%" height="100%" controls="" name="media"><source src="''' + srcs[i] + '''" type="audio/mpeg"</video>
    </a></em></td>
</tr>
'''
    except:
            pass
    Html_Top = '''
  </tbody>
</table>
</body>
</html>
'''
    return mv_player + Musics_List + Html_Top
    


app.run(host="0.0.0.0",port=5555,debug=True)

