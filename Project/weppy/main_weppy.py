import weppy
from weppy import *

app = App(__name__)

@app.route("/login")
def index():
    return

app.run(host='127.0.0.1',port=5555,debug=True)