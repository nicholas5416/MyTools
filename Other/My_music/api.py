import requests, urllib, json, os, sys, threading, time
#=======================================#
# Def!
type='song'   # Search Song.        # 1
type='mv'     # Search Mv.          # 2
type='album'  # Search album.       # 3
type='list'   # Search Song Lists.  # 4
#=======================================#
def Netease_Get_MV_List():
    global List_Mv_Names, List_Mv_Singers, List_Mv_Pic, List_Mv_Srcs
    List_Mv_Names = []
    List_Mv_Singers = []
    List_Mv_Pic = []
    List_Mv_Srcs = []
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/netease/topMvList?key=579621905&limit=1000&offset=0')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        List_Mv_Names.append(in_list['name'])
        List_Mv_Singers.append(in_list['singer'])
        List_Mv_Pic.append(in_list['pic'])
        List_Mv_Srcs.append(in_list['url'])
    return List_Mv_Names, List_Mv_Singers, List_Mv_Pic, List_Mv_Srcs

def Netease_Search_MV_API(Keywords):
    global Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    word = Keywords
    Resources = []
    Mv_Authors = []
    Mv_Names = []
    Mv_Srcs = []
    Mv_Pic = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&type=video&limit=100&offset=0')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']['videos']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            if len(str(in_list['vid'])) > 10:
                pass
            else:
                Mv_Authors.append(in_list['creator'][0]['userName'])
                Mv_Names.append(in_list['title'])
                Mv_Srcs.append('https://api.bzqll.com/music/netease/mvUrl?key=579621905&id=' + in_list['vid'] + '&r=1080')
                Mv_Pic.append(in_list['coverUrl'])
        return Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    except:
        print (" [-] Null!")
    
def Netease_Search_Music_Album_API(Keywords):
    global Album_Names, Album_Authors, Album_Pic, Album_Ids
    word = Keywords
    Resources = []
    Album_Authors = []
    Album_Names = []
    Album_Pic = []
    Album_Ids = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&type=album&limit=100&offset=0')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']['albums']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Album_Names.append(in_list['name'])
            Album_Authors.append(in_list['company'])
            Album_Pic.append(in_list['pic'])
            Album_Ids.append(in_list['id'])
        return Album_Names, Album_Authors, Album_Pic, Album_Ids
    except:
        print (" [-] Null!")

def Netease_Search_Music_List_API(Keywords):
    global List_Names, List_Authors, List_Pic, List_Ids
    word = Keywords
    Resources = []
    List_Authors = []
    List_Names = []
    List_Pic = []
    List_Ids = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&limit=100&offset=0&type=list')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']['playlists']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            List_Names.append(in_list['name'])
            List_Authors.append(in_list['creator']['nickname'])
            List_Pic.append(in_list['coverImgUrl'])
            List_Ids.append(in_list['id'])
    except:
        print (" [-] Null!")
    return List_Names, List_Authors, List_Pic, List_Ids

def Netease_Get_Music_List():
    global Music_List_Names, Music_List_Authors, Music_List_Photo, Music_List_Ids
    Music_List_Names = []
    Music_List_Authors = []
    Music_List_Photo = []
    Music_List_Ids = []
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/netease/hotSongList?key=579621905&cat=%E5%85%A8%E9%83%A8&limit=1000&offset=0')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List_Names.append(in_list['title'])
        Music_List_Authors.append(in_list['creator'])
        Music_List_Photo.append(in_list['coverImgUrl'])
        Music_List_Ids.append(in_list['id'])
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/netease/highQualitySongList?key=579621905&cat=%E5%85%A8%E9%83%A8&limit=1000')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']['playlists']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List_Names.append(in_list['title'])
        Music_List_Authors.append(in_list['creator'])
        Music_List_Photo.append(in_list['coverImgUrl'])
        Music_List_Ids.append(in_list['id'])
    Resources = []
    return Music_List_Names, Music_List_Authors, Music_List_Photo, Music_List_Ids


def Netease_From_List_Get_Musics(id):
    global Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs
    Music_Names = []
    Music_Authors = []
    Music_Pic = []
    Music_Lrc = []
    Resources = []
    Music_Srcs = []
    Recv_All = requests.get('https://api.bzqll.com/music/netease/songList?key=579621905&id=' + str(id) + '&limit=1000&offset=0')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']['songs']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_Names.append(in_list['name'])
        Music_Authors.append(in_list['singer'])
        Music_Pic.append(in_list['pic'])
        Music_Lrc.append(in_list['lrc'])
        Music_Srcs.append(in_list['url'])
    return Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs

def Netease_From_Album_Get_Musics(id):
    global Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs
    Music_Names = []
    Music_Authors = []
    Music_Pic = []
    Music_Lrc = []
    Resources = []
    Music_Srcs = []
    Recv_All = requests.get('https://api.bzqll.com/music/netease/album?key=579621905&id=' + str(id))
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_Names.append(in_list['name'])
        Music_Authors.append(in_list['singer'])
        Music_Pic.append(in_list['pic'])
        Music_Lrc.append(in_list['lrc'])
        Music_Srcs.append(in_list['url'])
    return Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs

def Netease_Search_Music_API(Keywords):
    global Music_Names, Music_Authors, Music_Srcs, Music_Pic, Music_Lrc
    word = Keywords
    Resources = []
    Music_Authors = []
    Music_Names = []
    Music_Srcs = []
    Music_Pic = []
    Music_Lrc = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/netease/search?key=579621905&s=' + word + '&type=song&limit=100&offset=0')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Music_Authors.append(in_list['singer'])
            Music_Names.append(in_list['name'])
            Music_Srcs.append(in_list['url'])
            Music_Pic.append(in_list['pic'])
            Music_Lrc.append(in_list['lrc'])
        return Music_Names, Music_Authors, Music_Srcs, Music_Pic, Music_Lrc
    except:
        print (" [-] Null!")

#======================================================#

def QQ_Get_MV_List():
    global Mv_Names, Mv_Singers, Mv_Pic, Mv_Srcs
    Mv_Names = []
    Mv_Singers = []
    Mv_Pic = []
    Mv_Srcs = []
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/tencent/hotMvList?key=579621905&year=0&tag=0&area=0&limit=100&offset=0')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Mv_Singers.append(in_list['singer'])
        Mv_Names.append(in_list['name'])
        Mv_Pic.append(in_list['pic'])
        Mv_Srcs.append(in_list['url'])
    return Mv_Names, Mv_Singers, Mv_Pic, Mv_Srcs

def QQ_Search_MV_API(Keywords):
    global Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    word = Keywords
    Resources = []
    Mv_Authors = []
    Mv_Names = []
    Mv_Srcs = []
    Mv_Pic = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s=' + word + '&limit=100&offset=0&type=mv')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Mv_Names.append(in_list['mv_name'])
            Mv_Authors.append(in_list['singer_name'])
            Mv_Srcs.append("https://api.bzqll.com/music/tencent/mvUrl?key=579621905&id=" + in_list['v_id'] + '&r=4')
            Mv_Pic.append(in_list['mv_pic_url'])
        return Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    except:
        print (" [-] Null!")

def QQ_Search_Music_Album_API(Keywords):
    global Album_Names, Album_Authors, Album_Pic, Album_Ids
    word = Keywords
    Resources = []
    Album_Authors = []
    Album_Names = []
    Album_Pic = []
    Album_Ids = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s=' + word + '&limit=100&offset=0&type=album')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Album_Names.append(in_list['albumName'])
            Album_Authors.append(in_list['singerName_hilight'])
            Album_Pic.append(in_list['albumPic'])
            Album_Ids.append(in_list['albumMID'])
        return Album_Names, Album_Authors, Album_Pic, Album_Ids
    except:
        print (" [-] Null!")

def QQ_Search_Music_List_API(Keywords):
    global List_Names, List_Authors, List_Pic, List_Ids
    word = Keywords
    Resources = []
    List_Authors = []
    List_Names = []
    List_Pic = []
    List_Ids = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s=' + word + '&limit=50&offset=0&type=list')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            List_Names.append(in_list['dissname'])
            List_Authors.append(in_list['creator']['name'])
            List_Pic.append(in_list['imgurl'])
            List_Ids.append(in_list['dissid'])
    except:
        print (" [-] Null!")
    return List_Names, List_Authors, List_Pic, List_Ids

def QQ_Get_Music_List():
    global Music_List_Names, Music_List_Authors, Music_List_Pic, Music_List_Ids
    Music_List_Names = []
    Music_List_Authors = []
    Music_List_Pic = []
    Music_List_Ids = []
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/tencent/hotSongList?key=579621905&categoryId=10000000&sortId=3&limit=1000')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_List_Names.append(in_list['name'])
        Music_List_Authors.append(in_list['creator'])
        Music_List_Pic.append(in_list['pic'])
        Music_List_Pic.append(in_list['pic'])
        Music_List_Ids.append(in_list['id'])
    return Music_List_Names, Music_List_Authors, Music_List_Pic, Music_List_Ids

def QQ_From_List_Get_Musics(id):
    global Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs
    Music_Names = []
    Music_Authors = []
    Music_Pic = []
    Music_Lrc = []
    Resources = []
    Recv_All = requests.get('https://api.bzqll.com/music/tencent/songList?key=579621905&id=' + str(id) + '&limit=1000&offset=0')
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']['songs']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_Names.append(in_list['name'])
        Music_Authors.append(in_list['singer'])
        Music_Pic.append(in_list['pic'])
        Music_Lrc.append(in_list['lrc'])
        Music_Srcs.append(in_list['url'])
    return Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs

def QQ_From_Album_Get_Musics(id):
    global Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs
    Music_Names = []
    Music_Authors = []
    Music_Pic = []
    Music_Lrc = []
    Resources = []
    Music_Srcs = []
    Recv_All = requests.get('https://api.bzqll.com/music/tencent/album?key=579621905&id=' + str(id))
    Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
    Recv_Datas = Recv_Datas['data']['songs']
    for all_list in Recv_Datas:
        Resources.append(all_list)
    for in_list in Resources:
        Music_Names.append(in_list['name'])
        Music_Authors.append(in_list['singer'])
        Music_Pic.append(in_list['pic'])
        Music_Lrc.append(in_list['lrc'])
        Music_Srcs.append(in_list['url'])
    return Music_Names, Music_Authors, Music_Pic, Music_Lrc, Music_Srcs

def QQ_Search_Music_API(Keywords):
    global Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc
    word = Keywords
    Resources = []
    Music_Singers = []
    Music_Names = []
    Music_Srcs = []
    Music_Pic = []
    Music_Lrc = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/tencent/search?key=579621905&s='+ word + '&limit=100&offset=0&type=song')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Music_Names.append(in_list['name'])
            Music_Singers.append(in_list['singer'])
            Music_Srcs.append(in_list['url'])
            Music_Pic.append(in_list['pic'])
            Music_Lrc.append(in_list['lrc'])
        return Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc
    except:
        print (" [-] Null!")

#======================================================#

def KG_Search_MV_API(Keywords):
    global Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    word = Keywords
    Resources = []
    Mv_Authors = []
    Mv_Names = []
    Mv_Srcs = []
    Mv_Pic = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/kugou/search?key=579621905&s=' + word + '&limit=100&offset=0&type=mv')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Mv_Names.append(in_list['filename'])
            Mv_Authors.append(in_list['singername'])
            Mv_Srcs.append("https://api.bzqll.com/music/kugou/mvUrl?key=579621905&id=" + in_list['hash'] + '&r=sq')
            Mv_Pic.append(in_list['imgurl'])
        return Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic
    except:
        print (" [-] Null!")    

def KG_Search_Music_API(Keywords):
    global Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc
    word = Keywords
    Resources = []
    Music_Singers = []
    Music_Names = []
    Music_Srcs = []
    Music_Pic = []
    Music_Lrc = []
    try:
        Recv_All = requests.get('https://api.bzqll.com/music/kugou/search?key=579621905&s='+ word + '&limit=100&offset=0&type=song')
        Recv_Datas = json.loads(Recv_All.text.strip('callback()[]'))
        Recv_Datas = Recv_Datas['data']
        for all_list in Recv_Datas:
            Resources.append(all_list)
        for in_list in Resources:
            Music_Names.append(in_list['name'])
            Music_Singers.append(in_list['singer'])
            Music_Srcs.append(in_list['url'])
            Music_Pic.append(in_list['pic'])
            Music_Lrc.append(in_list['lrc'])
        return Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc
    except:
        print (" [-] Null!")