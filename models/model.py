#coding:utf-8
##############################################################################
# Author：QQ173782910
##############################################################################
"""models/model.py"""

from sqlalchemy import create_engine,Column, Integer,Text,DateTime,SMALLINT,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from dbconfig import tiger,scott,host,port,dbname
url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (scott, tiger, host,port,dbname)
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)

############################
class bourse_users(Base):
    """ 用户交易所帐户"""
    __tablename__ = "bourse_users"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    title = Column(Text,  nullable=True,comment='帐户名称')
    bourse_id = Column(Integer, nullable=True, index=True,comment='交易所id')
    apikey= Column(Text,  nullable=True,comment='okex_APIKey')
    secretkey= Column(Text,  nullable=True,comment='okex_SecretKey')
    passphrase= Column(Text,  nullable=True,comment='okex_PassPhrase')
    del_flag= Column(SMALLINT,  nullable=True,index=True)
    del_ctime = Column(DateTime, nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)

class celery_log(Base):
    """ celery处理log"""
    __tablename__ = "celery_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    errors = Column(Text,  nullable=True,index=True)
    cname = Column(Text,  nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)

class login_log(Base):
    """ 登录日志"""
    __tablename__ = "login_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    login_id = Column(Text, nullable=True, index=True)
    login_ip = Column(Text, nullable=True)
    http_user_agent = Column(Text, nullable=True)
    login_type = Column(Text, nullable=True)
    login_status = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)

class menu_func(Base):
    """ 后台菜单"""
    __tablename__ = "menu_func"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    menu_id = Column(Integer, nullable=True, index=True)
    ctype = Column(SMALLINT, nullable=True)
    menu_name = Column(Text, nullable=True)
    menu = Column(Integer, nullable=True)
    sort = Column(Integer, nullable=True,index=True)
    parent_id = Column(Integer, nullable=True,index=True)
    func_id = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True,index=True)
    img = Column(Text, nullable=True)

class mtc_t(Base):
    """ 关联说明表"""
    __tablename__ = "mtc_t"

    seq = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    id = Column(Integer, nullable=True, index=True)
    ctype = Column(Text, nullable=True, index=True)
    txt1 = Column(Text, nullable=True, index=True)
    txt2 = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True)
    sort = Column(Integer, nullable=True)
    del_flag = Column(SMALLINT, nullable=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class positions(Base):
    """ 持仓记录"""
    __tablename__ = "positions"

    id = Column(Text, primary_key=True, nullable=False,index=True)
    usr_id = Column(Integer,nullable=True, index=True)
    instrument_id = Column(Text, nullable=True,comment='标的名称')
    holds = Column(Text, nullable=True, comment='持仓记录')
    results = Column(Text, nullable=True, comment='返回记录')
    longnum = Column(Text, nullable=True, comment='多单持仓')
    longcost = Column(Text, nullable=True, comment='多单均价')
    longpnl = Column(Text, nullable=True, comment='多单盈利')
    shortnum = Column(Text, nullable=True, comment='空单持仓')
    shortcost= Column(Text, nullable=True, comment='空单均价')
    shortpnl = Column(Text, nullable=True, comment='空单盈利')
    long_pnl_ratio= Column(Text, nullable=True, comment='多单盈利率')
    short_pnl_ratio= Column(Text, nullable=True, comment='空单盈利率')
    lasts= Column(Text, nullable=True, comment='最新价')
    highest = Column(Text, nullable=True, comment='最高价')
    lowhest = Column(Text, nullable=True, comment='最低价')
    client_oid = Column(Text, nullable=True,index=True,  comment='机器人订单id')
    ctime = Column(DateTime, nullable=True, index=True)

class print_log(Base):
    """ 打印记录"""
    __tablename__ = "print_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    errors = Column(Text, nullable=True)
    cname = Column(Text, nullable=True, index=True)
    ctime = Column(DateTime, nullable=True, index=True)

class run_log(Base):

    """ 运行日志"""
    __tablename__ = "run_log"

    id = Column(Text, primary_key=True, nullable=False, index=True)
    usr_id = Column(Integer,nullable=True,index=True)
    instrument_id = Column(Text, nullable=True, comment='商品')
    remark = Column(Text, nullable=True, comment='说明')
    ctime = Column(DateTime, nullable=True, index=True)

class stop_profit(Base):
    """ 持仓流水"""
    __tablename__ = "stop_profit"

    id = Column(Text, primary_key=True, nullable=False, index=True)
    usr_id = Column(Integer,nullable=True,index=True)
    instrument_id = Column(Text, nullable=True, comment='交易对')
    holds = Column(Text, nullable=True, comment='持仓')
    results = Column(Text, nullable=True, comment='持仓')
    longnum = Column(Text, nullable=True, comment='多单张数')
    longcost = Column(Text, nullable=True, comment='多单开仓价')
    longpnl = Column(Text, nullable=True, comment='当前多单持仓收益')
    shortnum = Column(Text, nullable=True, comment='空单张数')
    shortcost = Column(Text, nullable=True, comment='空单开仓价')
    shortpnl = Column(Text, nullable=True, comment='当前空单持仓收益')
    long_pnl_ratio = Column(Text, nullable=True, comment='当前多单收益率')
    short_pnl_ratio = Column(Text, nullable=True, comment='当前空单收益率')
    lasts = Column(Text, nullable=True, comment='最新价')
    highest = Column(Text, nullable=True, comment='最高价')
    lowhest = Column(Text, nullable=True, comment='最低价')
    client_oid = Column(Text, nullable=True, comment='机器人订单id')
    ctime = Column(DateTime, nullable=True, index=True)

class stop_profit_log(Base):
    """ 止盈止损日志"""
    __tablename__ = "stop_profit_log"

    id = Column(Text, primary_key=True, nullable=False, index=True)
    usr_id = Column(Integer,nullable=True,index=True)
    instrument_id = Column(Text, nullable=True, comment='交易标的')
    deal_num = Column(Text, nullable=True, comment='交易张数')
    num = Column(Text, nullable=True, comment='持仓量')
    costs = Column(Text, nullable=True, comment='开仓价')
    pnl = Column(Text, nullable=True, comment='收益')
    lasts = Column(Text, nullable=True, comment='最新价')
    highest= Column(Text, nullable=True, comment='最高价')
    lowhest = Column(Text, nullable=True, comment='最低价')
    client_oid = Column(Text, nullable=True, comment='机器人订单id')
    remark = Column(Text, nullable=True, comment='说明')
    ctime = Column(DateTime, nullable=True, index=True)


class trading_log(Base):
    """ 交易日志"""
    __tablename__ = "trading_log"

    id = Column(Text, primary_key=True, nullable=False, index=True)
    usr_id = Column(Integer,nullable=True,index=True)
    bu_title = Column(Text, nullable=True, comment='帐户')
    s_cname = Column(Text, nullable=True, comment='策略')
    t_cname = Column(Text, nullable=True, comment='标的名称')
    instrument_id = Column(Text, nullable=True, comment='商品')
    deal_num = Column(Integer, nullable=True, comment='买卖数量')
    moneys = Column(Float, nullable=True, comment='当前价格')
    tp_okexs = Column(Text, nullable=True, comment='时间周期秒')
    sj = Column(Text, nullable=True, comment='')
    yk = Column(Text, nullable=True, comment='')
    remark = Column(Text, nullable=True, comment='')
    del_flag = Column(SMALLINT, nullable=True, index=True)
    del_time = Column(DateTime, nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)
    utime = Column(DateTime, nullable=True)

class use_log(Base):
    """ 操作记录log"""
    __tablename__ = "use_log"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True,index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    viewid = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True, index=True)

class user_strategy(Base):
    """ 用户策略"""
    __tablename__ = "user_strategy"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    usr_id = Column(Integer, nullable=True, index=True)
    bu_id = Column(Integer, nullable=True, index=True,comment='用户交易所帐户id')
    bu_title = Column(Text, nullable=True,comment='用户交易所帐户名称')
    bu_api = Column(Text, nullable=True,comment='用户交易所帐户api')
    bu_secret = Column(Text, nullable=True,comment='用户交易所帐户secret')
    bu_passp = Column(Text, nullable=True,comment='用户交易所帐户pass')
    t_instrument_id = Column(Text, nullable=True, comment='交易标的')
    tp_okexs = Column(Integer, nullable=True, comment='时间周期秒')
    deal_num = Column(Integer, nullable=True, comment='交易数量/张')
    status = Column(SMALLINT, nullable=True, index=True, comment='状态，0停止，1运行中')
    hold_position = Column(Float, nullable=True, comment='持仓')
    profit_loss = Column(Float, nullable=True, comment='持仓盈亏')
    longnum = Column(Text, nullable=True,  comment='多单持仓')
    longcost = Column(Text, nullable=True, comment='多单均价')
    longpnl = Column(Text, nullable=True,  comment='多单盈利')
    shortnum = Column(Text, nullable=True,  comment='空单持仓')
    shortcost = Column(Text, nullable=True,  comment='空单均价')
    shortpnl = Column(Text, nullable=True,  comment='空单盈利')
    h_longpnl = Column(Text, nullable=True,  comment='当前最高多单盈利')
    h_shortpnl = Column(Text, nullable=True,  comment='当前最高空单盈利')
    h_last = Column(Text, nullable=True,  comment='此单最高价')
    l_last = Column(Text, nullable=True, comment='此单最低价')
    htime= Column(DateTime, nullable=True, comment='最高值最后更新时间')
    ptime = Column(DateTime, nullable=True, comment='最后更新时间')
    long_pnl_ratio = Column(Text, nullable=True, comment='当前多单盈利率')
    short_pnl_ratio = Column(Text, nullable=True,  comment='当前空单盈利率')
    contract_val = Column(Text, nullable=True,  comment='合约面值')
    stop_pnl = Column(SMALLINT, nullable=True,  comment='止盈处理类型')
    pnl_num = Column(Text, nullable=True,  comment='止盈量')
    stop_kx = Column(Text, nullable=True,  comment='止损处理')
    kx_num = Column(Text, nullable=True,  comment='止损量')
    pnl_tag = Column(Text, nullable=True,  comment='参考量')
    sy1 =Column(Text, nullable=True,  comment='收益1')
    ht1 = Column(Text, nullable=True,  comment='回撤1')
    sy2 = Column(Text, nullable=True,  comment='收益2')
    ht2 = Column(Text, nullable=True,  comment='回撤2')
    sy3 = Column(Text, nullable=True,  comment='收益3')
    ht3 = Column(Text, nullable=True,  comment='回撤3')
    sy4 = Column(Text, nullable=True,  comment='收益4')
    ht4 = Column(Text, nullable=True,  comment='回撤4')
    sy5 = Column(Text, nullable=True,  comment='收益5')
    ht5 = Column(Text, nullable=True,  comment='回撤5')
    sy6 = Column(Text, nullable=True,  comment='收益6')
    ht6 = Column(Text, nullable=True,  comment='回撤6')
    client_oid= Column(Text, nullable=True,  comment='机器人订单id')
    use_flag = Column(SMALLINT, nullable=True,  comment='是否禁止策略平仓0允许1禁止')
    del_flag = Column(SMALLINT, nullable=True, index=True)
    del_time = Column(DateTime, nullable=True)
    ctime = Column(DateTime, nullable=True)
    utime = Column(DateTime, nullable=True)


class users(Base):
    """ 系统用户表"""
    __tablename__ = "users"

    usr_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    login_id = Column(Text, nullable=True, index=True)
    passwd = Column(Text, nullable=True)
    status = Column(SMALLINT, nullable=True, index=True)
    mini_openid = Column(Text, nullable=True, index=True)
    wx_openid = Column(Text, nullable=True, index=True)
    with_flag = Column(SMALLINT, nullable=True)
    expire_flag = Column(SMALLINT, nullable=True)
    expire_time = Column(DateTime, nullable=True)
    login_lock = Column(SMALLINT, nullable=True)
    login_lock_time = Column(DateTime, nullable=True)
    vip_flag = Column(Integer, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_ip = Column(Text, nullable=True)
    vip_days = Column(Integer, nullable=True)
    invite_days = Column(Integer, nullable=True)
    random_no = Column(Text, nullable=True, index=True)
    auth_login = Column(Text, nullable=True)
    auth_ps = Column(Text, nullable=True)
    del_flag = Column(SMALLINT, nullable=True, index=True)
    cid = Column(Integer, nullable=True)
    ctime = Column(DateTime, nullable=True)
    uid = Column(Integer, nullable=True)
    utime = Column(DateTime, nullable=True)

class webapge_log(Base):
    """ 接口故障记录"""
    __tablename__ = "webapge_log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, index=True)
    errors = Column(Text, nullable=True)
    cname = Column(Text, nullable=True)
    ctime = Column(DateTime, nullable=True)


######################################################

def createall(engine_):
    try:
        Base.metadata.drop_all(engine_)
    except:
        pass
    Base.metadata.create_all(engine_)