# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  admin/dl/H001_dl.py
##############################################################################
import json
from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL import cBASE_DL

class cH001_dl(cBASE_DL):

    def init_data(self):
        self.FDT = [
            ['帐户名称', "u.usr_id", '', ''],  # 0

        ]
        self.GNL = self.parse_GNL([0])


    def getInfo(self):

        sql = """
                select bu.id,bu.title from bourse_users bu
                where coalesce(bu.del_flag,0)=0 and usr_id=%s
                """
        parm = [self.usr_id]
        L1, t = self.db.select(sql, parm)

        sql="""
        select  convert_from(decrypt(login_id::bytea, %s, 'aes'),'SQL_ASCII') as login_id,
        auth_login,auth_ps 
        from users where usr_id = %s
        """
        info  =  self.db.fetch(sql ,[self.md5code,self.usr_id])
        return L1,info

    def local_add_save(self):
        dR={'code':'0','MSG':'保存成功'}
        oldpassword = self.GP('oldpassword','')
        password = self.GP('password','')
        auth_login = self.GP('auth_login','')
        auth_ps = self.GP('auth_ps','')
        if oldpassword!='':
            sql="select usr_id from users where  passwd= crypt(%s, U.passwd)  and usr_id=%s;"
            l,t=self.db.select(sql,[oldpassword,self.usr_id])
            if t==0:
                dR['code'] = '1'
                dR['MSG'] = '原密码不正确'
                return dR

            sql = "update users set passwd=crypt(%s, gen_salt('md5')) where usr_id=%s;"
            parm = [password,self.usr_id]
            self.db.query(sql, parm)

        if auth_login!='':
            sql = "update users set auth_login=%s,auth_ps=%s  where usr_id=%s;"
            parm = [auth_login, auth_ps, self.usr_id]
            self.db.query(sql, parm)

        #self.use_log('修改个人帐号%s' % self.usr_id)
        return dR

    def upps_data(self):
        dR={'code':'0','MSG':'修改密码成功'}
        psstr=self.REQUEST.get('psstr','')
        if psstr=='':
            dR['code'] = '1'
            dR['MSG'] = '数据有误'
            return dR
        V = self.decryption_data(psstr)
        password = V.get('password', '')
        oldpassword = V.get('oldpassword', '')
        if oldpassword=='' or password=='':
            dR['code'] = '1'
            dR['MSG'] = '密码信息有误'
            return dR
        sql="select usr_id from users where  passwd= crypt(%s,passwd)  and usr_id=%s"
        l,t=self.db.select(sql,[oldpassword,self.usr_id])
        if t==0:
            dR['code'] = '1'
            dR['MSG'] = '原密码不正确'
            return dR
        sql = "update users set passwd=crypt(%s, gen_salt('md5'))  where usr_id=%s"
        parm = [password, self.usr_id]
        self.db.query(sql, parm)
        #self.use_log('修改个人帐号%s' % self.usr_id)
        return dR

    def bourse_users_data(self):
        dR = {'code': '', 'MSG': ''}
        personstr = self.REQUEST.get('personstr', '')
        if personstr == '':
            dR['code'] = '1'
            dR['MSG'] = '数据有误'
            return dR
        V = self.decryption_data(personstr)
        title = V.get('title', '')
        bourse_id = V.get('bourse_id', '')
        apikey = V.get('apikey', '')
        secretkey = V.get('secretkey', '')
        passphrase = V.get('passphrase', '')
        if title == '' or apikey == '' or secretkey=='' or passphrase=='':
            dR['code'] = '1'
            dR['MSG'] = '帐户信息有误'
            return dR

        # sql="""select id from bourse_users
        # where coalesce(del_flag,0)=0 and ((usr_id=%s and bourse_id=%s)
        # or (convert_from(decrypt(apikey::bytea, %s, 'aes'),'SQL_ASCII')=%s
        # and convert_from(decrypt(secretkey::bytea, %s, 'aes'),'SQL_ASCII')=%s
        # and convert_from(decrypt(passphrase::bytea, %s, 'aes'),'SQL_ASCII')=%s))"""
        # parm=[self.usr_id,bourse_id,self.md5code,apikey,self.md5code,secretkey,self.md5code,passphrase]
        sql = """select id from bourse_users 
               where coalesce(del_flag,0)=0 and usr_id=%s and bourse_id=%s 
               and convert_from(decrypt(apikey::bytea, %s, 'aes'),'SQL_ASCII')=%s;"""
        parm = [self.usr_id, bourse_id, self.md5code, apikey]
        l,t=self.db.select(sql,parm)
        if t>0:
            return {'MSG':'已有帐号，不允许添加','code':'1'}
        #写入前要检查api权限
        code=self.apikey_check(apikey,secretkey,passphrase)
        if code == 2:
            return {'MSG': '相关密钥没有交易权限，无法添加', 'code': '1'}
        elif code == 1:
            return {'MSG': '相关密钥校验有误，无法添加', 'code': '1'}
        elif code == 3:
            return {'MSG': '传输有误，请联系客服', 'code': '1'}
        elif code == 4:
            return {'MSG': '同一交易所帐户无法使用多个API同时交易', 'code': '1'}

        sql="""insert into bourse_users(usr_id,title,bourse_id,apikey,secretkey,passphrase,ctime)
        values(%s,%s,%s,encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),now());"""
        parm=[self.usr_id,title,bourse_id,apikey,self.md5code,secretkey,self.md5code,passphrase,self.md5code]
        self.db.query(sql,parm)
        dR = {'MSG': '添加帐户成功','code':'0'}
        return dR

    def del_r_data(self):

        id = self.GP('id')
        sql = "select id from bourse_users where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"
        l, t = self.db.select(sql, [self.usr_id,id])
        if t == 0:
            dR = {'MSG': '数据有误'}
            return dR
        #再加判断是否还在使用，如果在，那就不能删除
        sql = "select id from user_strategy where coalesce(del_flag,0)=0 and usr_id=%s and bu_id=%s"
        l, t = self.db.select(sql, [self.usr_id, id])
        if t > 0:
            dR = {'MSG': '请先删除使用交易帐户的交易对'}
            return dR

        sql = "update bourse_users set del_flag=1,del_time=now() where id=%s"
        self.db.query(sql, [id])
        dR = {'code':'0','MSG': '删除成功'}
        return dR



