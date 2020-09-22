# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################
"""install.py"""


import os, sys
from importlib import reload
reload(sys)

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.stdout = sys.stderr

from flask import Flask, request,redirect,render_template
from sqlalchemy import *


app=Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTYj'

filename = "{}/dbconfig.py".format(app.root_path)
#


def create_config(username, password, host,port, dbname,md5code):
    data = render_template("config.html",username=username,password=password,host=host,port=port,dbname=dbname,md5code=md5code)
    fd = open(filename, "w")
    fd.write(data)
    fd.close()

@app.route('/install', methods=['GET', 'POST'])
def install():
    code=0
    if os.path.exists(filename):
        code=3
    return render_template('install.html',code=code)

@app.route('/setup', methods=['GET', 'POST'])
def setup():

    step = request.args.get("step", type=int)
    RES = request.values
    if step == 1:
        return render_template("setup1.html")
    elif step == 2:

        host = RES.get('host','')
        username = RES.get('username','')
        passwd = RES.get('passwd','')
        dbname = RES.get('dbname','')
        port = RES.get('port','')
        md5code = RES.get('md5code','')
        #print(host,username,passwd,dbname,port,md5code)
        url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (username, passwd, host,port,dbname)
        try:
            engine_ = create_engine(url)
            connection = engine_.connect()
        except Exception as e:
            print(e,'connection-errorXXXXXX ')
            return render_template("setup-error.html", code=3)

        create_config(username, passwd, host, port,dbname,md5code)
        if os.path.exists(filename):
            from models.model import createall
            createall(engine_)
            return render_template("setup2.html")
        return render_template("setup-error.html", code=3)


    elif step == 3:
        login_id = RES.get('login_id', '')
        passwd = RES.get('passwd', '')
        try:
            try:
                from dbconfig import scott, tiger, host, port, dbname,md5code
                from basic.DB_TOOL import DB_pg
                link = [host, port, dbname, scott, tiger]
                db = DB_pg(link)
            except Exception as ee:
                print(ee,'dbconfig is null@@@@@')
                raise NameError('db link error')

            l,t =db.select("SELECT usr_id FROM users WHERE usr_id=1;")

            try:#增加开启加解密扩展
                sql_pgcrypto="""
                    create extension pgcrypto;
                """
                db.query(sql_pgcrypto)

            except:
                pass
            try:
                sql_del="""
                    delete from menu_func;
                """
                db.query(sql_del)

            except:
                pass
            sql_menu="""
            INSERT INTO public.menu_func (menu_id,menu_name,ctype,menu,sort,parent_id,func_id,status,img) VALUES (1,'自动交易',0,1,1,null,'A001',1,'fa-circle-o');
            INSERT INTO public.menu_func (menu_id,menu_name,ctype,menu,sort,parent_id,func_id,status,img) VALUES (2,'我的帐户',0,1,2,null,'H001',1,'fa-user');
            """
            db.query(sql_menu)

            sql_mtc_t="""
                INSERT INTO public.mtc_t (id,ctype,txt1,txt2,status,del_flag,sort,cid,ctime,uid,utime) VALUES 
                (1,'YESNO','是',NULL,NULL,0,1,NULL,NULL,NULL,NULL)
                ,(0,'YESNO','否',NULL,NULL,0,2,NULL,NULL,NULL,NULL)
                ,(0,'STATUS','无状态','交易列表的当前状态',NULL,0,0,NULL,NULL,NULL,NULL)
                ,(1,'STATUS','准备运行','交易列表的当前状态',NULL,0,1,NULL,NULL,NULL,NULL)
                ,(2,'STATUS','运行中','交易列表的当前状态',NULL,0,2,NULL,NULL,NULL,NULL)
                ,(3,'STATUS','准备停止','交易列表的当前状态',NULL,0,3,NULL,NULL,NULL,NULL)
                ,(4,'STATUS','停止中','交易列表的当前状态',NULL,0,4,NULL,NULL,NULL,NULL)
                ,(5,'STATUS','已停止','交易列表的当前状态',NULL,0,5,NULL,NULL,NULL,NULL)
                ,(6,'STATUS','准备平仓','交易列表的当前状态',NULL,0,6,NULL,NULL,NULL,NULL)
                ,(7,'STATUS','平仓中','交易列表的当前状态',NULL,0,7,NULL,NULL,NULL,NULL)
                ,(8,'STATUS','已平仓','交易列表的当前状态',NULL,0,8,NULL,NULL,NULL,NULL)
                ,(9,'STATUS','准备删除','交易列表的当前状态',NULL,0,9,NULL,NULL,NULL,NULL);
            """
            db.query(sql_mtc_t)

            if t>0:
                sql="""update users set login_id=encrypt(%s,%s,'aes'),status=1,
                    passwd= crypt(%s, gen_salt('md5')) where usr_id=1;"""
                db.query(sql,[login_id,md5code,passwd])
                return render_template('setup.html',code=0)
            sql = """insert into users(usr_id,login_id,passwd,status)
                    values(1,encrypt(%s,%s,'aes'),crypt(%s, gen_salt('md5')),1);
                    """
            db.query(sql,[login_id, md5code,passwd])

            return render_template('setup.html',code=0)
        except Exception as e:
            print(e,'eeee')
            return render_template('setup.html', code=3)
    return render_template('install.html')



@app.route('/', methods=['GET', 'POST'])
def start():
    if not os.path.exists(filename):
        return redirect('/install')
    return render_template('ok.html')



if __name__ == '__main__':
    app.run(port=5001,debug=True)
    #app.run(host='0.0.0.0', port=5000,debug=True)




