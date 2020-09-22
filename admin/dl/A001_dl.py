# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  admin/dl/A001_dl.py
##############################################################################

from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL
#from run_task import run_log

class cA001_dl(cBASE_DL):

    def init_data(self):
        self.FDT = [
            ['帐户', "u.usr_id", '', ''],  # 0
            #['策略名称', "u.login_id", '', ''],  # 1
            ['交易标的', "u.usr_name", '', ''],  # 2
            ['时间周期', "u.usr_name", '', ''],  # 3
            ['交易数量/张', "u.usr_name", '', ''],  # 4
            #['交易标的', "u.usr_name", '', ''],  # 5
            ['当前状态', "u.mobile", '', ''],  # 5
            ['持仓', "u.login_lock_time", '', ''],  # 6
            ['持仓盈亏', "u.login_lock", '', ''],  # 7
        ]

        self.GNL = self.parse_GNL([0,1,2,3,4,5,6])


    def mRight(self):

        sql = """
                select us.id,us.bu_title,us.t_instrument_id,us.tp_okexs,us.deal_num,mt.txt1
                ,hold_position,profit_loss,coalesce(us.status,0) 
                from user_strategy us 
                left join mtc_t mt on mt.ctype='STATUS' and mt.id=coalesce(us.status,0) and coalesce(mt.del_flag,0)=0 
                where us.usr_id=%s and coalesce(us.del_flag,0)=0
                order by us.id desc
                """
        parm = [self.usr_id]
        
        L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo,L=parm)
        PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        return PL,L


    def save_deal_data(self):

        bu_id=self.GP('bu_id')#帐户
        tp_id = self.GP('t_id')#时间周期
        symbol = self.GP('symbol')#交易标的
        deal_num = self.GP('deal_num')#交易数量/张
        stop_pnl = self.GP('stop_pnl')  #止盈类型
        pnl_num = self.GP('pnl_num')  # 止盈量
        stop_kx = self.GP('stop_kx')  # 止损类型
        kx_num = self.GP('kx_num')  # 止损量
        pnl_tag= self.GP('pnl_tag')  # 止盈参数量

        sy1 = self.GP('sy1')  # 收益1
        ht1 = self.GP('ht1')  # 回撤1
        sy2 = self.GP('sy2')  # 收益2
        ht2 = self.GP('ht2')  # 回撤2
        sy3 = self.GP('sy3')  # 收益3
        ht3 = self.GP('ht3')  # 回撤3
        sy4 = self.GP('sy4')  # 收益4
        ht4 = self.GP('ht4')  # 回撤4
        sy5 = self.GP('sy5')  # 收益5
        ht5 = self.GP('ht5')  # 回撤5
        sy6 = self.GP('sy6')  # 收益6
        ht6 = self.GP('ht6')  # 回撤6

        if pnl_num:
            try:
                float(pnl_num)
            except:
                return {'MSG': '止盈量填写有误'}
        if kx_num:
            try:
                float(kx_num)
            except:
                return {'MSG': '止损量填写有误'}
        if pnl_tag:
            try:
                float(pnl_tag)
            except:
                return {'MSG': '参考量填写有误'}
        if sy1:
            try:
                float(sy1)
            except:
                return {'MSG': '收益1填写有误'}
        if sy2:
            try:
                float(sy2)
            except:
                return {'MSG': '收益2填写有误'}
        if sy3:
            try:
                float(sy3)
            except:
                return {'MSG': '收益3填写有误'}
        if sy4:
            try:
                float(sy4)
            except:
                return {'MSG': '收益4填写有误'}
        if sy5:
            try:
                float(sy5)
            except:
                return {'MSG': '收益5填写有误'}
        if sy6:
            try:
                float(sy6)
            except:
                return {'MSG': '收益6填写有误'}
        if ht1:
            try:
                float(ht1)
            except:
                return {'MSG': '回撤1填写有误'}
        if ht2:
            try:
                float(ht2)
            except:
                return {'MSG': '回撤2填写有误'}
        if ht3:
            try:
                float(ht3)
            except:
                return {'MSG': '回撤3填写有误'}
        if ht1:
            try:
                float(ht1)
            except:
                return {'MSG': '回撤1填写有误'}
        if ht4:
            try:
                float(ht4)
            except:
                return {'MSG': '回撤4填写有误'}
        if ht5:
            try:
                float(ht5)
            except:
                return {'MSG': '回撤5填写有误'}
        if ht6:
            try:
                float(ht6)
            except:
                return {'MSG': '回撤6填写有误'}


        sql="select id from user_strategy where bu_id=%s and t_instrument_id=%s and usr_id=%s and coalesce(del_flag,0)=0"
        l,t=self.db.select(sql,[bu_id,symbol,self.usr_id])
        if t>0:
            return {'MSG':'该交易对已存在'}
        code, L=self.get_name_data(bu_id)
        if code==1:
            return {'MSG': '添加交易对失败，请联系客服'}
        bu_title,bu_api,bu_secret,bu_passp=L

        sql="""insert into user_strategy(usr_id,bu_id,bu_title,bu_api,bu_secret,bu_passp,
        deal_num,ctime,t_instrument_id,tp_okexs,stop_pnl,pnl_num,stop_kx,kx_num,pnl_tag,
        sy1,sy2,sy3,sy4,sy5,sy6,ht1,ht2,ht3,ht4,ht5,ht6)
        values(%s,%s,%s,encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),encrypt(%s,%s,'aes'),
        %s,now(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        parm=[self.usr_id,bu_id,bu_title,bu_api,self.md5code,bu_secret,self.md5code,bu_passp,self.md5code,
              deal_num,symbol,tp_id,stop_pnl,pnl_num,stop_kx,kx_num,pnl_tag,sy1,sy2,sy3,sy4,sy5,sy6,
              ht1,ht2,ht3,ht4,ht5,ht6]
        self.db.query(sql,parm)
        dR = {'code':'0','MSG': '添加交易对成功'}
        return dR

    def updeal_data(self):

        id=self.GP('id')#
        deal_num = self.GP('deal_num')#交易数量/张
        stop_pnl = self.GP('stop_pnl')  #止盈类型
        pnl_num = self.GP('pnl_num')  # 止盈量
        stop_kx = self.GP('stop_kx')  #止损类型
        kx_num = self.GP('kx_num')  # 止损量
        pnl_tag= self.GP('pnl_tag')  # 参考量
        sy1 = self.GP('sy1')  # 收益1
        ht1 = self.GP('ht1')  # 回撤1
        sy2 = self.GP('sy2')  # 收益2
        ht2 = self.GP('ht2')  # 回撤2
        sy3 = self.GP('sy3')  # 收益3
        ht3 = self.GP('ht3')  # 回撤3
        sy4 = self.GP('sy4')  # 收益4
        ht4 = self.GP('ht4')  # 回撤4
        sy5 = self.GP('sy5')  # 收益5
        ht5 = self.GP('ht5')  # 回撤5
        sy6 = self.GP('sy6')  # 收益6
        ht6 = self.GP('ht6')  # 回撤6
        use_flag= self.GP('use_flag')  # 是否允许策略
        if pnl_num:
            try:
                float(pnl_num)
            except:
                return {'MSG': '止盈量填写有误'}
        if kx_num:
            try:
                float(kx_num)
            except:
                return {'MSG': '止损量填写有误'}
        if pnl_tag:
            try:
                float(pnl_tag)
            except:
                return {'MSG': '参考量填写有误'}
        if sy1:
            try:
                float(sy1)
            except:
                return {'MSG': '收益1填写有误'}
        if sy2:
            try:
                float(sy2)
            except:
                return {'MSG': '收益2填写有误'}
        if sy3:
            try:
                float(sy3)
            except:
                return {'MSG': '收益3填写有误'}
        if sy4:
            try:
                float(sy4)
            except:
                return {'MSG': '收益4填写有误'}
        if sy5:
            try:
                float(sy5)
            except:
                return {'MSG': '收益5填写有误'}
        if sy6:
            try:
                float(sy6)
            except:
                return {'MSG': '收益6填写有误'}
        if ht1:
            try:
                float(ht1)
            except:
                return {'MSG': '回撤1填写有误'}
        if ht2:
            try:
                float(ht2)
            except:
                return {'MSG': '回撤2填写有误'}
        if ht3:
            try:
                float(ht3)
            except:
                return {'MSG': '回撤3填写有误'}
        if ht1:
            try:
                float(ht1)
            except:
                return {'MSG': '回撤1填写有误'}
        if ht4:
            try:
                float(ht4)
            except:
                return {'MSG': '回撤4填写有误'}
        if ht5:
            try:
                float(ht5)
            except:
                return {'MSG': '回撤5填写有误'}
        if ht6:
            try:
                float(ht6)
            except:
                return {'MSG': '回撤6填写有误'}
        sql="select id from user_strategy where id=%s and usr_id=%s and coalesce(del_flag,0)=0"
        l,t=self.db.select(sql,[id,self.usr_id])
        if t==0:
            return {'MSG':'数据有误，无法修改'}
        sql="""update user_strategy set deal_num=%s,stop_pnl=%s,pnl_num=%s,
        stop_kx=%s,kx_num=%s,pnl_tag=%s,utime=now(),sy1=%s,sy2=%s,sy3=%s,sy4=%s,sy5=%s,sy6=%s,
        ht1=%s,ht2=%s,ht3=%s,ht4=%s,ht5=%s,ht6=%s,use_flag=%s where id=%s"""
        self.db.query(sql,[deal_num,stop_pnl,pnl_num,stop_kx,kx_num,pnl_tag,
                           sy1,sy2,sy3,sy4,sy5,sy6,ht1,ht2,ht3,ht4,ht5,ht6,use_flag,id])
        return {'code':'0','MSG': '数据修改成功'}

    def get_name_data(self,bu_id):
        sql='''select bu.title,
            convert_from(decrypt(apikey::bytea,%s, 'aes'),'SQL_ASCII') ,
            convert_from(decrypt(secretkey::bytea,%s, 'aes'),'SQL_ASCII') ,
            convert_from(decrypt(passphrase::bytea,%s, 'aes'),'SQL_ASCII') 
            from bourse_users bu 
            where  coalesce(bu.del_flag,0)=0 and  bu.usr_id=%s and bu.id=%s'''
        l,t=self.db.select(sql,[self.md5code,self.md5code,self.md5code,self.usr_id,bu_id])
        if t==0:
            return 1,[]
        return 0,l[0]

    def all_row_data(self):
        dR = {'code': '0', 'data':''}
        #帐户
        data={}
        sql="""select id,title from bourse_users
            where  coalesce(del_flag,0)=0 and usr_id=%s
        """
        l,t=self.db.select(sql,[self.usr_id])
        data['bourse_users']=l
        dR['data']=data
        return dR

    def delete_data(self):#删除单个（平仓） #  状态5已停止可以删除
        pk = self.pk
        sql="""select coalesce(status,0),t_instrument_id from user_strategy 
        where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
        l,t=self.db.select(sql,[self.usr_id,pk])
        if t==0:
            return {'code': '1', 'MSG': '数据不存在'}
        status,instrument_id=l[0]
        if status not in (0,5):
            return {'code': '1', 'MSG': '未停止无法删除'}
        self.db.query("update user_strategy set del_flag=1,del_time=now()  where id= %s;", [pk])
        # remark='%s--提交删除--%s'%(self.getToday(9),instrument_id)
        # run_log.push(self.usr_id,instrument_id,remark)
        return {'code': '0', 'MSG': '删除成功'}

    def Alldelete_data(self):#删除选择（平仓）  状态5已停止可以删除
        pk = self.REQUEST.getlist('item_id')
        #要先判断是否已经平仓成功，
        if pk != []:
            sql = ""
            parm = []
            t_instrument_id=''
            for i in pk:
                sqli = """select coalesce(status,0),t_instrument_id from user_strategy 
                        where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
                l, t = self.db.select(sqli, [self.usr_id, i])
                if t == 0:
                    continue
                status, instrument_id = l[0]
                if status not in (0,5):
                    continue
                t_instrument_id+=instrument_id+','
                sql += "update user_strategy set del_flag=1,del_time=now()  where id= %s;"
                parm.append(i)
            if sql != "":
                self.db.query(sql, parm)
            # remark = '%s--提交批量删除--%s'%(self.getToday(9),t_instrument_id)
            # run_log.push(self.usr_id,t_instrument_id, remark)
            return {'code': '0', 'MSG': '批量删除成功'}
        return {'code': '1', 'MSG': '批量删除失败'}

    def clean_all_data(self):#持仓全平选择    状态2运行中
        pk = self.REQUEST.getlist('item_id')
        if pk != []:
            sql = ""
            parm = []
            t_instrument_id=''
            for i in pk:
                sqli = """select coalesce(status,0),t_instrument_id from user_strategy 
                        where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
                l, t = self.db.select(sqli, [self.usr_id, i])
                if t == 0:
                    continue
                status, instrument_id = l[0]
                if status!=2:
                    continue
                t_instrument_id += instrument_id + ','
                sql += "update user_strategy set status=6,utime=now()  where id= %s;"
                parm.append(i)
            if sql != "":
                self.db.query(sql, parm)

            # remark = '%s--提交批量持仓全平--%s'%(self.getToday(9),t_instrument_id)
            # run_log.push(self.usr_id,t_instrument_id, remark)
            return {'code': '0', 'MSG': '批量持仓全平成功'}
        return {'code': '1', 'MSG': '批量持仓全平失败'}

    def pasue_all_data(self):#停止选择   状态2运行中
        pk = self.REQUEST.getlist('item_id')
        if pk != []:
            sql = ""
            parm = []
            t_instrument_id=''
            for i in pk:
                sqli = """select coalesce(status,0),t_instrument_id from user_strategy 
                        where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
                l, t = self.db.select(sqli, [self.usr_id, i])
                if t == 0:
                    continue
                status, instrument_id = l[0]
                if status!=2:
                    continue
                t_instrument_id += instrument_id + ','
                sql += "update user_strategy set status=3,utime=now()  where id= %s;"
                parm.append(i)
            if sql != "":
                self.db.query(sql, parm)
            # remark = '%s--提交批量停止--%s'%(self.getToday(9),t_instrument_id)
            # run_log.push(self.usr_id,t_instrument_id, remark)
            return {'code': '0', 'MSG': '批量停止成功'}
        return {'code': '1', 'MSG': '批量停止失败'}

    def run_all_data(self):#运行选择  状态0，5可运行
        pk = self.REQUEST.getlist('item_id')
        if pk != []:
            sql = ""
            parm = []
            t_instrument_id=''
            for i in pk:
                sqli = """select coalesce(status,0),t_instrument_id from user_strategy 
                                where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
                l, t = self.db.select(sqli, [self.usr_id, i])
                if t == 0:
                    continue
                status, instrument_id = l[0]
                if status not in (0,5):
                    continue
                t_instrument_id += instrument_id + ','
                sql += "update user_strategy set status=1,utime=now()  where id= %s;"
                parm.append(i)
            if sql != "":
                self.db.query(sql, parm)
            # remark = '%s--提交批量运行--%s'%(self.getToday(9),t_instrument_id)
            # run_log.push(self.usr_id,t_instrument_id, remark)
            return {'code': '0', 'MSG': '批量运行成功'}
        return {'code': '1', 'MSG': '批量运行失败'}

    def pasue_r_data(self):#停止单个  状态2运行中
        pk = self.pk
        sql = """select coalesce(status,0),t_instrument_id from user_strategy 
                where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
        l, t = self.db.select(sql, [self.usr_id, pk])
        if t == 0:
            return {'code': '1', 'MSG': '数据不存在'}
        status, instrument_id = l[0]
        if status != 2:
            return {'code': '1', 'MSG': '未运行无法停止'}

        self.db.query("update user_strategy set status=3,utime=now()  where id= %s", [pk])
        # remark = '%s--提交停止--%s' % (self.getToday(9), instrument_id)
        # run_log.push(self.usr_id, instrument_id, remark)
        return {'code': '0', 'MSG': '停止成功'}

    def run_r_data(self):#运行单个  状态0，5可运行
        pk = self.pk
        sql = """select coalesce(status,0),t_instrument_id from user_strategy 
                        where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
        l, t = self.db.select(sql, [self.usr_id, pk])
        if t == 0:
            return {'code': '1', 'MSG': '数据不存在'}
        status, instrument_id = l[0]
        if status not in (0,5):
            return {'code': '1', 'MSG': '该状态无法运行'}

        self.db.query("update user_strategy set status=1,utime=now()  where id= %s", [pk])
        # remark = '%s--提交运行--%s' % (self.getToday(9), instrument_id)
        # run_log.push(self.usr_id, instrument_id, remark)
        return {'code': '0', 'MSG': '运行成功'}

    def clean_r_data(self):#平仓单个  状态2 可平仓
        pk = self.pk
        sql = """select coalesce(status,0),t_instrument_id from user_strategy 
                                where coalesce(del_flag,0)=0 and usr_id=%s and id=%s"""
        l, t = self.db.select(sql, [self.usr_id, pk])
        if t == 0:
            return {'code': '1', 'MSG': '数据不存在'}
        status, instrument_id = l[0]
        if status != 2:
            return {'code': '1', 'MSG': '未运行无法平仓'}
        self.db.query("update user_strategy set status=6,utime=now()  where id= %s", [pk])
        # remark = '%s--提交平仓--%s' % (self.getToday(9), instrument_id)
        # run_log.push(self.usr_id, instrument_id, remark)
        return {'code': '0', 'MSG': '平仓成功'}

    def edit_row_data(self):

        sql="""select deal_num,stop_pnl,pnl_num,stop_kx,kx_num,pnl_tag,sy1,sy2,sy3,sy4,sy5,sy6,
        ht1,ht2,ht3,ht4,ht5,ht6,coalesce(use_flag,0)use_flag
         from user_strategy where usr_id=%s and id=%s and coalesce(del_flag,0)=0"""
        l,t=self.db.fetchall(sql,[self.usr_id,self.pk])
        if t==0:
            return {'code': '1'}
        return {'code': '0', 'data':l[0]}






