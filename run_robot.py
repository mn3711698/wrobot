
import time
import traceback
import gevent
from gevent import monkey
monkey.patch_all()
from robot.trade_future import FutureTrade
from robot.trade_swap import SwapTrade
from basic.JD_TOOL import robot_bugerror,md5code
from run_task import update_status
from basic.DB_TOOL import DB_pg
from dbconfig import scott, tiger, host, port, dbname
try:
    link =[host,port, dbname,scott, tiger]
    db = DB_pg(link)
except:
    raise NameError('db link error')

class RunTrade():


    def __init__(self,params):#持仓及资产相关的初始化放在这
        #params:[api, secret, passp, symbol, 300时间周期, 1张数, usr_id, status, us_id]
        self.apikey, self.secretkey, self.passphrase, self.symbol,self.time_period,self.num,self.status,self.usr_id, \
        self.us_id, self.bu_title, self.h_longpnl, self.h_shortpnl, \
        self.stop_pnl, self.pnl_num, self.stop_kx, self.kx_num, self.h_last, self.pnl_tag, self.l_last, \
        self.sy1, self.sy2, self.sy3, self.sy4, self.sy5, self.sy6, \
        self.ht1, self.ht2, self.ht3, self.ht4, self.ht5, self.ht6,self.client_oid = params

        if 'SWAP' in self.symbol:
            self.robot = SwapTrade(params)
        else:
            self.robot = FutureTrade(params)
        self.params = params


    def run(self):

        #1准备运行，2运行中，3准备停止，4停止中，5已停止X，6准备平仓，7平仓中，8已平仓，
        if self.status==1:#准备运行只更新状态就好了。
            update_status.push(self.usr_id,self.us_id,2)#

        elif self.status == 3:  #准备停止，更新状态进行平仓
            update_status.push(self.usr_id,self.us_id,4)#
            self.robot.close_all()#如何判断平仓成功？
            return
        elif self.status == 4:#停止中，判断平仓成功就更新状态停止，如果没未平仓成功，那是接着做平仓操作还是等待平仓成功？
            update_status.push(self.usr_id,self.us_id,5)#
            return
        elif self.status == 6:#准备平仓，更新状态，调用平仓
            update_status.push(self.usr_id,self.us_id,7)
            self.robot.close_all()  # 如何判断平仓成功？
            return
        elif self.status == 7:#平仓中，判断是平否平仓成功，成功就更新状态,未平仓就等待
            update_status.push(self.usr_id,self.us_id,8)#
            return
        elif self.status == 8:#平仓功能，更新状态返回
            update_status.push(self.usr_id,self.us_id,2)#
            return
        self.robot.realtrade()#每交易一次，更新仓位，仓位变化做存储，以交易对为基准



def fetch(a):

    try:
        RunTrade(a).run()
    except:
        robot_bugerror(traceback,'begin_run_error')


if __name__ == "__main__":

    try:
        while True:
            sql = """select convert_from(decrypt(bu_api::bytea, %s, 'aes'),'SQL_ASCII'),
            convert_from(decrypt(bu_secret::bytea, %s, 'aes'),'SQL_ASCII'),
            convert_from(decrypt(bu_passp::bytea, %s, 'aes'),'SQL_ASCII'),
            t_instrument_id,tp_okexs,deal_num, coalesce(status,0),usr_id,id,bu_title,
            coalesce(h_longpnl,'0'),coalesce(h_shortpnl,'0'),
            stop_pnl,coalesce(pnl_num,'0'),stop_kx,coalesce(kx_num,'0'),coalesce(h_last,'0')
            ,coalesce(pnl_tag,'0'),coalesce(l_last,'0'),
            coalesce(sy1,'0'),coalesce(sy2,'0'),coalesce(sy3,'0'),coalesce(sy4,'0'),coalesce(sy5,'0'),coalesce(sy6,'0'),
            coalesce(ht1,'0'),coalesce(ht2,'0'),coalesce(ht3,'0'),coalesce(ht4,'0'),coalesce(ht5,'0'),coalesce(ht6,'0'),
            coalesce(client_oid,'')
            from user_strategy where coalesce(del_flag,0)=0 and coalesce(status,0) not in (0,5)
            """
            l, t = db.select(sql, [md5code, md5code, md5code])
            if t>0:
                gevent.joinall([gevent.spawn(fetch, x) for x in l])
            time.sleep(2)
    except:
        robot_bugerror(traceback,'begin_user_strategy_error')




