# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910 admin/vi/login.py
##############################################################################

import time
import re
import datetime
import random
from importlib import reload
from basic.JD_TOOL import DEBUG,user_menu,PUBLIC_KEY
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL import cBASE_TPL
from flask import make_response,redirect

class clogin(cBASE_TPL):

    def setClassName(self):
        self.dl_name = ''

    def goPartList(self):
        return self.runApp('login.html')
    
    def goPartDologin(self):
        dR={'code':'1','MSG':''}
        signature = self.dl.GP('signature', '','')
        if signature=='':
            dR['MSG'] = '用户名或密码有误'
            return self.jsons(dR)
        V = self.dl.decryption_data(signature)
        login_id = V.get('inputname','')
        password = V.get('inputPassword','')
        try:
            login_ip = self.objHandle.headers["X-Real-IP"]
        except:
            login_ip = self.objHandle.remote_addr

        if login_id =='' or password=='':
            dR['MSG']='用户名或密码有误'
            return self.jsons(dR)

        lT = self.dl.login(login_id,password)

        if lT:
            usr_id=lT[0][0]
            login_lock=lT[0][2]
            if str(login_lock) == '1':
                dR['MSG'] = '您的帐号已被锁定，请联系管理员!'
                return self.jsons(dR)

            result = self.dl.cookie.isetcookie("__session" , usr_id)
            
            self.dl.checkuser(usr_id)
            menu1,menu2,menu3 = self.dl.getSysMenu(usr_id)
            if usr_id in user_menu:
                user_menu[usr_id] = {
                    'menu1':menu1,'menu2':menu2,'menu3':menu3
                }
            else:
                user_menu.update( {usr_id:{
                    'menu1':menu1,'menu2':menu2,'menu3':menu3
                }} )

            sql="UPDATE users SET  last_login=%s,last_ip=%s WHERE usr_id=%s"
            self.dl.db.query(sql,[self.dl.getToday(7),login_ip,usr_id])
            self.dl.create_token(usr_id)
            self.login_log(login_status='成功', usr_id=usr_id, login_id=login_id, login_type='PC',login_ip=login_ip)
            dR['MSG'] = '登录成功！'
            dR['code']='0'
        else:

            self.login_log(login_status= '失败', usr_id='0', login_id=login_id, login_type='PC',login_ip=login_ip)
            dR['MSG'] = '用户名或密码错误！'
        return self.jsons(dR)


    # 登录时插入数据库表login_log的函数
    def login_log(self, login_status='', usr_id='0', login_id='', login_type='PC',login_ip=''):

        HTTP_USER_AGENT = self.objHandle.environ['HTTP_USER_AGENT']

        login_id = login_id.replace("'", "")
        if len(login_id) > 18: login_id = 'XXXXXX'
        sql = """insert into login_log(login_id,usr_id,login_ip,http_user_agent,login_type,login_status,ctime,status)
               values(%s,%s,%s,%s,%s,%s,now(),0)
            """
        self.dl.db.query(sql,[login_id, usr_id, login_ip, HTTP_USER_AGENT, login_type, login_status])
        if login_status == '失败':  # 登录失败失败超过5次，锁住账号
            sql = """select COUNT(*) from login_log 
                    where login_id=%s and status=0 
                    and to_char(ctime,'YYYY-MM-DD HH:24-MI')>to_char(now(),'YYYY-MM-DD') and login_status='失败'
            """
            lT, iN = self.dl.db.select(sql,login_id)
            if lT[0][0] >= 5:
                sql = "update users set login_lock=1,login_lock_time=now() where login_id=%s"
                self.dl.db.query(sql,login_id)
                sql2 = "update login_log set status=1 where login_id=%s"
                self.dl.db.query(sql2,login_id)

    def goPartLogout(self):
        self.dl.cookie.clearcookie('__session')
        response = make_response(redirect("admin?viewid=login"))
        self.dl.cookie.responeCookie(response)
        return response

    def goPartshowkey(self):
        dR={'code':'0','MSG':'','PUBLIC_KEY':PUBLIC_KEY}
        return self.jsons(dR)



