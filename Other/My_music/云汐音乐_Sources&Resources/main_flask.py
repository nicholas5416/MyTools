import flask
from flask import *
from api import *
#============================================#
cloud_page_head = """
<!DOCTYPE html>
<html xmlns="/www.w3.org/1999/xhtml">
<head id="Head1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>云汐---云上的日子</title>
<meta name="Keywords" content="云汐--想念云上的日子" />
<link href="Images/web.css?v20150217" rel="stylesheet" />
<link rel="stylesheet" href="css/stylesheets/style.css">
<script src="js/jquery-1.7.2.min.js"></script>
<script type="text/javascript">
function hehe(){
	var aa="<div style=' position:relative; top:-120px; width:500px; height:200px; margin-left:32%;border-radius:15px; overflow:hidden;  border: 1px solid #CECFD4;-webkit-box-shadow:#666 0px 0px 10px;'><iframe name='iframe_canvas' src='http:\\\\douban.fm/partner/baidu/doubanradio' scrolling='no' frameborder='0' width='500' height='200'  ></iframe></div>";
	document.getElementById("douban").re
	document.getElementById("douban").innerHTML=aa;
	}
</script>
</head>

<body>
<form method="post" action="" id="form1">
  <div class="aspNetHidden">
    <input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPDwUKLTc1NTI0MDUxNmRkhXbaTpIxMPDoysndg51aitx85REO2oAB9WjTm+jKHs4=" />
  </div>
  <div class="aspNetHidden">
    <input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="CA0B0334" />
  </div>
  <div id="body" >
    <div id="jp_container" role="application" aria-label="media player">
      <div class="jp-type-playlist">
        <div id="jplayer" class="jp-jplayer"></div>
        <div class="jp-time"> <span class="jp-current-time" role="timer" aria-label="time"></span><span class="jp-duration" role="timer" aria-label="duration"></span> </div>
      </div>
    </div>
  </div>
  <div id="douban" style="margin:auto">
    <div class="grid-music-container f-usn">
      <div class="m-music-play-wrap">
        <div class="u-cover"></div>
        <div class="m-now-info">
          <h1 class="u-music-title"><strong>标题</strong><small>歌手</small></h1>
          <div class="m-now-controls">
            <div class="u-control u-process"> <span class="buffer-process"></span> <span class="current-process"></span> </div>
            <div class="u-control u-time">00:00/00:00</div>
            <div class="u-control u-volume">
              <div class="volume-process" data-volume="0.50"> <span class="volume-current"></span> <span class="volume-bar"></span> <span class="volume-event"></span> </div>
              <a class="volume-control"></a> </div>
          </div>
          <div class="m-play-controls"> <a class="u-play-btn prev" title="上一曲"></a> <a class="u-play-btn ctrl-play play" title="暂停"></a> <a class="u-play-btn next" title="下一曲"></a> <a class="u-play-btn mode mode-list current" title="列表循环"></a> <a class="u-play-btn mode mode-random" title="随机播放"></a> <a class="u-play-btn mode mode-single" title="单曲循环"></a> </div>
        </div>
      </div>
      <div class="f-cb">&nbsp;</div>
      <div class="m-music-list-wrap"></div>
    </div>
    <script src="src/js/smusic.min.js"></script> 
    <script>
var musicList = [
"""
cloud_page_foo = """
	
];

new SMusic({

	musicList:musicList

});
</script>
    <link rel="stylesheet" href="src/css/smusic.css"/>
  </div>
  <div style="color:gray; font-family:微软雅黑; font-size:14px; position:relative; top:130px" > QQ：1838115594 邮箱：1838115594@qq.com <a style="color:gray; font-family:微软雅黑; font-size:14px;a:hover:black" target="_blank" href="http://1838115594.qzone.qq.com/" title="留言给我">给我留言</a> &nbsp;&nbsp;&nbsp;<a style="color:gray; font-family:微软雅黑; font-size:14px;a:hover:black" target="_blank"</a>
  </div>
</form>
</body>
</html>
<script type="text/javascript" src="Images/jquery.js"></script>
<script type="text/javascript" src="Images/ThreeWebGL.js"></script>
<script type="text/javascript" src="Images/ThreeExtras.js"></script>
<script type="text/javascript" src="Images/Detector.js"></script>
<script type="text/javascript" src="Images/RequestAnimationFrame.js"></script>
<script id="vs" type="x-shader/x-vertex">
			varying vec2 vUv;
			void main() {
				vUv = uv;
				gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			}
    </script>
<script id="fs" type="x-shader/x-fragment">
			uniform sampler2D map;
			uniform vec3 fogColor;
			uniform float fogNear;
			uniform float fogFar;
			varying vec2 vUv;
			void main() {
				float depth = gl_FragCoord.z / gl_FragCoord.w;
				float fogFactor = smoothstep( fogNear, fogFar, depth );
				gl_FragColor = texture2D( map, vUv );
				gl_FragColor.w *= pow( gl_FragCoord.z, 20.0 );
				gl_FragColor = mix( gl_FragColor, vec4( fogColor, gl_FragColor.w ), fogFactor );
			}
    </script>
<script type="text/javascript" src="Images/cloud.js"></script>
"""
Mv_Page_Head = """
<!DOCTYPE html>
<!-- saved from url=(0024)http://127.0.0.1:57638/# -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project</title>
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <link rel="stylesheet" href="./css/font-awesome.min.css">
    <link rel="stylesheet" href="./css/Features-Boxed.css">
    <link rel="stylesheet" href="./css/styles.css">
</head>

<body>
    <div class="features-boxed">
        <div class="container">
            <div class="intro">
                <h2 class="text-center">List:</h2>
            </div>
            <div class="row justify-content-center features">
"""
Mv_Page_Foo = """       
            </div>
        </div>
    </div>
    <script src="./js/jquery-3.2.1.min.js"></script>
    <script src="./js/bootstrap.min.js"></script>
    <script id="bs-live-reload" data-sseport="57639" data-lastchange="1550649605522" src="./js/livereload.js"></script>
</body></html>
"""
try:
    Mv_Names, Mv_Singers, Mv_Pic, Mv_Srcs = QQ_Get_MV_List()
    List_Mv_Names, List_Mv_Singers, List_Mv_Pic, List_Mv_Srcs = Netease_Get_MV_List()
    All_Mv_List_Names, All_Mv_List_Singers, All_Mv_List_Pics, All_Mv_List_Srcs = List_Mv_Names + Mv_Names, List_Mv_Singers + Mv_Singers, List_Mv_Pic + Mv_Pic, List_Mv_Srcs + Mv_Srcs
except:
    pass
try:
    Netease_Music_List_Names, Netease_Music_List_Authors, Netease_Music_List_Photo, Netease_Music_List_Ids = Netease_Get_Music_List()
    Netease_Music_Names, Netease_Music_Authors, Netease_Music_Pic, Netease_Music_Lrc, Netease_Music_Srcs = Netease_From_List_Get_Musics(str(Netease_Music_List_Ids[0]))
except:
      print ("Get Mv List Error!")
app = Flask(__name__,static_url_path='')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cloud")
def cloud():
  INS = 0
  cloud_list = ""
  for i in range(0,100):
      try:
          cloud_list += """
{
	title : '""" + Netease_Music_Names[INS] + """',
	singer : '""" + Netease_Music_Authors[INS] + """',
	cover  : '""" + Netease_Music_Pic[INS] + """',
	src    : '""" + str(Netease_Music_Srcs[INS]) + """'
	},
"""     
          INS += 1
      except:
          pass
  return cloud_page_head + cloud_list + cloud_page_foo


@app.route("/mv")
def mv():
  Mv_Page_List = ''
  INS = 0
  for Mv_Name in All_Mv_List_Names:
    if Mv_Name == "":
      print ("Null!")
    else:
      Mv_Page_List += '''
                  <div class="col-sm-6 col-md-5 col-lg-4 item">
                    <div class="box"><img src="''' + All_Mv_List_Pics[INS] + '''" width="200" height="200" />
                        <h3 class="name">''' + Mv_Name + '''</h3>
                        <p class="description">''' + All_Mv_List_Singers[INS] +'''</p><a href="''' + All_Mv_List_Srcs[INS] + '''" class="learn-more">Play »</a></div>
                </div>
'''
    INS += 1
  return Mv_Page_Head + Mv_Page_List + Mv_Page_Foo

@app.route("/searcher")
def Searcher():
  return render_template('searcher.html')

@app.route("/musicsearch",methods=['GET','POST'])
def musicsearch():
  cloud_list = ""
  Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc = [],[],[],[],[]
  if request.method =='POST':
    source = request.form['source']
    search_source = request.form['search_source']
    if source == "":
      return " [ Null! ] "
    if search_source == "QQ":
      Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc = QQ_Search_Music_API(source)
    if search_source == "Netease":
      Music_Names, Music_Authors, Music_Srcs, Music_Pic, Music_Lrc = Netease_Search_Music_API(source)
    if search_source == "KG":
      Music_Names, Music_Singers, Music_Srcs, Music_Pic, Music_Lrc = KG_Search_Music_API(source)
    INS = 0
    for i in range(0,100):
      try:
        cloud_list += """
{
	title : '""" + Music_Names[INS] + """',
	singer : '""" + Music_Singers[INS] + """',
	cover  : '""" + Music_Pic[INS] + """',
	src    : '""" + str(Music_Srcs[INS]) + """'
	},
"""     
        INS += 1
      except:
        pass
    return cloud_page_head + cloud_list + cloud_page_foo
  else:
    return " [ Error ! ]"

@app.route("/mvsearch",methods=['GET','POST'])
def mvsearch():
  Mv_Page_List = ''
  if request.method =='POST':
    source = request.form['source']
    search_source = request.form['search_source']
    if source == "":
      return " [ Null! ] "
    if search_source == "QQ":
      Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic = QQ_Search_MV_API(source)
    if search_source == "Netease":
      Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic = Netease_Search_MV_API(source)
    if search_source == "KG":
      Mv_Names, Mv_Authors, Mv_Srcs, Mv_Pic = KG_Search_MV_API(source)
    INS = 0
    for Mv_Name in Mv_Names:
      if Mv_Name == "":
        pass
      else:
        Mv_Page_List += '''
                  <div class="col-sm-6 col-md-5 col-lg-4 item">
                    <div class="box"><img src="''' + Mv_Pic[INS] + '''" width="200" height="200" />
                        <h3 class="name">''' + Mv_Name + '''</h3>
                        <p class="description">''' + Mv_Authors[INS] +'''</p><a href="''' + Mv_Srcs[INS] + '''" class="learn-more">Play »</a></div>
                </div>
'''
      INS += 1
    return Mv_Page_Head + Mv_Page_List + Mv_Page_Foo
  else:
    return " [ Error ! ]"

app.run(host='0.0.0.0',port=5555,debug=True)