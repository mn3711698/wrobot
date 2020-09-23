# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  admin/dl/home_dl.py
##############################################################################

from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL import cBASE_DL


class chome_dl(cBASE_DL):

    def init_data(self):
        self.FDT = [
            ['交易标的', "u.usr_name", '', ''],  # 0
            ['交易数量/张', "u.usr_name", '', ''],  # 1
            ['时间周期', "u.mobile", '', ''],  # 2
            ['运行说明', "u.mobile", '', ''],  # 3

            ['持仓量', "u.usr_name", '', ''],  # 4
            ['开仓价', "u.usr_name", '', ''],  # 5
            ['盈亏', "u.usr_name", '', ''],  # 6
            ['最低价', "u.usr_name", '', ''],  # 7
            ['最新价', "u.usr_name", '', ''],  # 8


            ['处理说明', "u.login_lock_time", '', ''],  # 9
            ['记录时间', "u.mobile", '', ''],  # 10
            ['多单/空单处理及计算说明', "u.mobile", '50%', ''],  # 11
            ['最高价', "u.mobile", '', ''],  # 12
            ['系统订单号', "u.mobile", '', ''],  # 13

        ]

        self.GNL1 = self.parse_GNL([0, 1, 2, 3,10])
        self.GNL2 = self.parse_GNL([13,0,11,4,5, 6,8,12,7,10])
        self.GNL3 = self.parse_GNL([13,0,9,1,4,5,6,8,12,7,10])
        self.GNL4 = self.parse_GNL([13,0,11,4,5, 6,8,12,7,10])

    #在子类中重新定义
    def myInit(self):
        self.tab = self.GP("tab", "1")

    def mRight(self):
        if self.tab=='1':#策略运行日志
            sql = """
             select  instrument_id,deal_num,tp_okexs,remark 
             ,to_char(ctime,'YYYY-MM-DD HH24:MI:SS') 
             from trading_log tl  order by ctime desc limit 100;
            """
        elif self.tab=='2':#持仓日志
            # sql = """
            # select instrument_id,results ,longnum,longcost,longpnl,long_pnl_ratio,
            # shortnum,shortcost,shortpnl,short_pnl_ratio,lasts,to_char(ctime,'YYYY-MM-DD HH24:MI:SS')
            # from stop_profit sp  order by ctime desc limit 200;
            # """
            sql="""
            select client_oid,instrument_id,holds ,longnum,longcost,longpnl,
            shortnum,shortcost,shortpnl,lasts,highest,lowhest,to_char(ctime,'YYYY-MM-DD HH24:MI:SS') 
            from positions sp  order by ctime desc limit 40;
            """
        elif self.tab=='3':#止盈止损日志
            sql = """
            select client_oid,instrument_id,remark,deal_num,num,costs,pnl,lasts,highest,lowhest,to_char(ctime,'YYYY-MM-DD HH24:MI:SS') 
             from stop_profit_log spl order by ctime desc limit 40;
                """
        else:
            sql = """
            select client_oid,instrument_id,results ,longnum,longcost,longpnl,long_pnl_ratio,
            shortnum,shortcost,shortpnl,short_pnl_ratio,lasts,highest,lowhest,to_char(ctime,'YYYY-MM-DD HH24:MI:SS')
            from stop_profit sp  
            """
        parm = []
        if self.tab=='4':
            if self.qqid!='':
                sql+= " where (client_oid=%s or results like %s)"
                parm=[self.qqid,'%%%s%%'%self.qqid]
            sql+=" order by ctime desc limit 1000;"


        L, iTotal_length, iTotal_Page, pageNo, select_size = self.db.select_for_grid(sql, self.pageNo,20,parm)
        PL = [pageNo, iTotal_Page, iTotal_length, select_size]
        return PL, L



