# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  start.py
##############################################################################

import os
import sys


from importlib import reload
from flask import Flask, request


reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr

import basic.JD_TOOL
reload(basic.JD_TOOL)


from basic.JD_TOOL import ROOT,showadmin,showapi#,showupload,showwxvip


sys.path.append(ROOT)


app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'



@app.route('/', methods=['GET', 'POST'])
@app.route('/admin' , methods=['GET', 'POST'])
def admin():
    return showadmin(request)


@app.route('/api/<int:subid>', methods=['GET','POST'])
def api(subid):
    return showapi(request,subid)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)
    app.run(port=5002,debug=True)

application=app



