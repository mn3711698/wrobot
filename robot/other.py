
from run_task import trading_log,save_position,stop_profit,update_reset,update_earnings_price,printlog,client_oid_update

def log(word,usr_id=0,symbol='',num=0,tp_okexs=0):  # 输出日志，用于展示
    #提交日志任务注意ws显示及写数据库
    # f = open('logs.txt', mode='a+')
    # f.write(time.strftime("%Y-%m-%d %H:%M:%S  ", time.localtime()) + word + '\n')
    # f.close()
    #0为运行日志,1为交易日志
    #all_log.push(word, ctype,usr_id,symbol,num,tp_okexs)
    trading_log.push(word, usr_id, symbol, num, tp_okexs)

def update_ep(usr_id,us_id,ctype,flag,last,pnl,client_oid):
    # ctype 0:空单,1:多单
    # flag  'H'高价，'L':低价
    update_earnings_price.push(usr_id, us_id, ctype, flag, last, pnl,client_oid)

def print_log(cname,errors):
    printlog.push(cname,errors)
    return

def clientoid_update(us_id,client_oid,usr_id,symbol):
    client_oid_update.push(us_id,client_oid,usr_id,symbol)

def updatereset(usr_id,us_id):
    update_reset.push(usr_id,us_id)

def saveposition(usr_id,instrument_id,pt,us_id,result,ctype=0,client_oid=0,remark=''):
    #ctype==0 正常，1故障
    save_position.push(usr_id,instrument_id,pt,us_id,result,ctype,client_oid,remark)
#####################################################################


def stopprofit(usr_id,instrument_id,ptlist,results,ctype,deal_num,highest,lowhest,client_oid):
    stop_profit.push(usr_id,instrument_id,ptlist,results,ctype,deal_num,highest,lowhest,client_oid)







