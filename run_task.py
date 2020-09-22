# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################

import traceback
import time
import random
from basic.JD_TOOL import db,robot_bugerror
from function_scheduling_distributed_framework import patch_frame_config,task_deco
patch_frame_config(REDIS_HOST='127.0.0.1',REDIS_PASSWORD='',REDIS_PORT=6379,REDIS_DB=7)


def get_random_no(E_R=2, T=''):
    if E_R == 0:
        cur_random_no = "%s%s" % (time.time(), random.random())
        return cur_random_no.replace('.', '')
    elif E_R == 1:
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
        romcode = str(time.time()).split('.')[-1]  # [3:]
        order_number = T + danhao[2:] + romcode
        return order_number

    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    danhao = time.strftime("%Y%m%d%H%M%S", timeArray)
    romcode = str(time.time()).split('.')[-1]  # [3:]
    upperCase = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ]
    Dstr = random.sample(upperCase, E_R)
    D_c = ''.join(Dstr)
    random_no = D_c + danhao[2:] + romcode
    return random_no

def time_to(ti):
    ti = ti.replace("T", " ").replace(".000Z", "")
    data_sj = time.strptime(ti, "%Y-%m-%d %H:%M:%S")  # 定义格式
    time_int = int(time.mktime(data_sj))
    return time_int

@task_deco('printlog',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def printlog(cname,errors):
    sql="insert into print_log(cname,errors,ctime)values(%s,%s,now())"
    db.query(sql,[cname,errors])
    return

@task_deco('ustatus',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def update_status(usr_id,us_id,status):

    try:
        sql = "update user_strategy set status=%s,utime=now() where usr_id=%s and id=%s;"
        db.query(sql, [status, usr_id, us_id])
    except:
        robot_bugerror(traceback, ctype='update_status')
    return

@task_deco('tlog',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def trading_log(remark,usr_id,symbol,num,tp_okexs):
    #us_id  user_strategy的id
    try:
        id=get_random_no(E_R=0)
        sql="""insert into trading_log(id,usr_id,deal_num,instrument_id,remark,ctime,tp_okexs)
        values(%s,%s,%s,%s,%s,now(),%s);"""
        db.query(sql,[id,usr_id,num,symbol,remark,tp_okexs])
    except:
        robot_bugerror(traceback, ctype='trading_log')
    return

@task_deco('sp',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def save_position(usr_id,instrument_id,pt,us_id,result,ctype,client_oid,remark):
    try:
        if ctype != 0:#2永续
            robot_bugerror('获取持仓故障%s:%s:%s'%(client_oid,instrument_id,result), ctype='ok')
            return

        longnum, longcost, longpnl, shortnum, shortcost, shortpnl, long_pnl_ratio, short_pnl_ratio,last = pt

        if longnum>0:
            profit_loss = longpnl
        else:
            profit_loss = shortpnl

        sql = """update user_strategy set longnum=%s,longcost=%s,longpnl=%s,
                shortnum=%s,shortcost=%s,shortpnl=%s,ptime=now(),long_pnl_ratio=%s,short_pnl_ratio=%s,
                hold_position=%s,profit_loss=%s where id=%s;"""
        parm = [longnum, longcost, longpnl, shortnum, shortcost, shortpnl,
                long_pnl_ratio, short_pnl_ratio,longnum,profit_loss, us_id]

        db.query(sql, parm)
        if longnum == 0 and shortnum == 0:
            update_reset.push(usr_id, us_id)

        if longnum != 0 or shortnum != 0:
            sql = """update positions set holds=%s,results=%s,ctime=now(),longnum=%s,longcost=%s,longpnl=%s,
            shortnum=%s,shortcost=%s,shortpnl=%s,long_pnl_ratio=%s,short_pnl_ratio=%s,lasts=%s where client_oid=%s;"""
            parm = [remark, '%s' % result,
                    longnum,longcost,longpnl,shortnum,shortcost,shortpnl,long_pnl_ratio,short_pnl_ratio,last,client_oid]
            db.query(sql, parm)

    except:
        robot_bugerror(traceback, ctype='save_position')
    return


@task_deco('spt',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def stop_profit(usr_id,instrument_id,ptlist,results,ctype,deal_num,highest,lowhest,client_oid):
    try:
        longnum, longcost, longpnl, shortnum, shortcost, shortpnl, long_pnl_ratio, short_pnl_ratio, last = ptlist
        if ctype==0:
            if longnum == 0 and shortnum==0:
                return
            id=get_random_no(E_R=0)
            sql="""insert into stop_profit(id,usr_id,instrument_id,
            longnum,longcost,longpnl,shortnum,shortcost,shortpnl,ctime,long_pnl_ratio,short_pnl_ratio,
            results,lasts,highest,lowhest,client_oid)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s,%s,%s,%s,%s);"""
            parm=[id,usr_id,instrument_id,longnum,longcost,longpnl,shortnum,
                  shortcost,shortpnl,long_pnl_ratio,short_pnl_ratio,results,last,highest,lowhest,client_oid]
            db.query(sql,parm)
        elif ctype==1:
            if longnum!=0:
                #def spl_log(remark, symbol, deal_num, num, costs, pnl, lasts):
                stop_profit_log.push(results, instrument_id, deal_num, longnum, longcost, longpnl, last,highest,lowhest,client_oid)#多单
            elif shortnum!=0:
                stop_profit_log.push(results, instrument_id, deal_num, shortnum, shortcost, shortpnl, last,highest,lowhest,client_oid)#空单
    except:
        robot_bugerror(traceback, ctype='stop_profit')
    return

@task_deco('splog',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def stop_profit_log(remark,symbol,deal_num,num,costs,pnl,lasts,highest,lowhest,client_oid):

    try:
        id=get_random_no(E_R=0)
        sql="""insert into stop_profit_log(id,instrument_id,deal_num,num,costs,pnl,lasts,remark,ctime,highest,lowhest,client_oid)
        values(%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s);"""
        db.query(sql,[id,symbol,deal_num,num,costs,pnl,lasts,remark,highest,lowhest,client_oid])
    except:
        robot_bugerror(traceback, ctype='stop_profit_log')
    return

@task_deco('upre',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def update_reset(usr_id,us_id):
    #ctype 0空单，1多单
    try:
        sql = """update user_strategy set h_longpnl='0',h_shortpnl='0',
        htime=now(),h_last='0',l_last='0' where usr_id=%s and id=%s;"""
        parm = [usr_id, us_id]
        db.query(sql, parm)
    except:
        robot_bugerror(traceback, ctype='update_reset')
    return

@task_deco('uep',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def update_earnings_price(usr_id,us_id,ctype,flag,last,pnl,client_oid):
    #ctype 0:空单,1:多单
    #flag  'H'高价，'L':低价
    try:
        if ctype==0:#空单
            if flag=='H':#更高价
                sql = """update user_strategy set htime=now(),h_last=%s where usr_id=%s and id=%s;
                update positions set highest=%s where client_oid=%s;
                """
                parm = [last, usr_id, us_id,last,client_oid]
                db.query(sql, parm)
            else:#更低价
                sql = """update user_strategy set h_shortpnl=%s,htime=now(),l_last=%s where usr_id=%s and id=%s;
                update positions set lowhest=%s where client_oid=%s;
                """
                parm = [pnl, last, usr_id, us_id,last,client_oid]
                db.query(sql, parm)
        else:#多单
            if flag == 'H':#更高价
                sql = """update user_strategy set h_longpnl=%s,htime=now(),h_last=%s where usr_id=%s and id=%s;
                 update positions set highest=%s where client_oid=%s;
                """
                parm = [pnl, last, usr_id, us_id,last,client_oid]
                db.query(sql, parm)
            else:#更低价
                sql = """update user_strategy set htime=now(),l_last=%s where usr_id=%s and id=%s;
                update positions set lowhest=%s where client_oid=%s;
                """
                parm = [last, usr_id, us_id,last,client_oid]
                db.query(sql, parm)
    except:
        robot_bugerror(traceback, ctype='update_earnings_price')
    return

@task_deco('cou',log_level=50,is_print_detail_exception=False,create_logger_file=False,broker_kind=2)
def client_oid_update(us_id,client_oid,usr_id,symbol):
    try:
        id = get_random_no(E_R=0)
        sql = """update user_strategy set client_oid=%s where id=%s;
        insert into positions(id,usr_id,instrument_id,client_oid,ctime)values(%s,%s,%s,%s,now());
        """
        parm = [client_oid, us_id,id,usr_id,symbol,client_oid]
        db.query(sql, parm)


    except:
        robot_bugerror(traceback, ctype='client_oid_update')
    return

if __name__ == '__main__':


    ################################# 日志任务
    printlog.consume()#策略运行日志
    trading_log.consume()#策略运行日志
    stop_profit_log.consume()#止盈日志
    save_position.consume()#持仓处理
    ############################
    update_status.consume()#更新状态
    stop_profit.consume()#止盈处理
    update_reset.consume()#止盈记录
    update_earnings_price.consume()#更新收益与价格记录
    client_oid_update.consume()#
    ###############

