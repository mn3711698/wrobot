# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  /custom/features.py
##############################################################################

# 注意，策略，止盈，止损，这三个方法提供给有需要自定义使用个人的相关处理，

def Strategy():#策略
    # 止盈，止损请判断无策略信号进行处理
    # 策略有效的返回值有五个：1 为开多,-1为开空,11为平多,-11为平空,0为无信号
    # 1,-1,11,-11,0
    return ''#返回空就是表示不使用自定义策略，其他值为使用个人策略处理。

def Stop_profit_now(stop_pnl,pnl_num,pt,parameters):#止盈处理
    # stop_pnl:止盈处理类型,pnl_num:止盈量
    # longnum：多单持仓, longcost：多单均价, longpnl：多单盈利, shortnum：空单持仓, shortcost：空单均价, shortpnl：空单盈利, last：最新价
    # 返回值 11,-11   当需要平多返回11，当需要平空返回-11,其他值不处理
    longnum,longcost,longpnl,shortnum,shortcost,shortpnl,long_pnl_ratio,short_pnl_ratio,last = pt

    h_longpnl,h_shortpnl,h_last,pnl_tag,l_last,sy1,sy2,sy3,sy4,sy5,sy6,ht1,ht2,ht3,ht4,ht5,ht6=parameters
    # 可选值说明
    # 0:由策略自动处理；
    # 1:“获利止盈”就是当收益大于填写的“止盈量”时在无策略信号下就平仓;
    # 2:“开仓比止盈”就是当“开仓比”大于填写的“止盈量”时在无策略信号下就平仓，
    # 多单“开仓比”=(“最新价”-"开仓价")/"开仓价",空单“开仓比”=("开仓价"-“最新价”)/"开仓价"
    # 3:“获利回撤止盈”就是记录的“最高收益”，当收益回撤时，(“最高收益”-“当前收益”) /“最高收益”大于下方填写的“止盈量”在无策略信号下就平仓;
    # 4: “开仓比回撤止盈”就是记录的“最高价”或“最低价”，当价格回撤时多单是(“最高价”-“最新价”) / “最高价”，空单是(“最新价”-“最低价”) / “最新价”，大于下方填写的“止盈量”在无策略信号下就平仓;
    # 5: “价格比止盈”就是记录的“最高价”或“最低价”，多单是(“最新价”-“开仓价”) / (“最高价”-“开仓价”)，空单是(“开仓介”-“最新价”) / (“开仓介”-“最低价”)，大于下方填写的“止盈量”在无策略信号下就平仓;
    # 6: “动态止盈”就是记录的“最高价”或“最低价”，多单是当“开仓价”*(1 + "参考量") <“现价”并且“现价”*(1 + "止盈量") <“最高价”会平仓，空单是“开仓介”*(1 -“参考量”) > "现价"
    # 并且“现价”*(1 - "止盈量") >“最低价”会平仓;
    # 7: “多级动态止盈”当策略没有信号时，根据下方计算判断是否需要进行止盈处理:如下
    # 多单：当“收益”大于"收益1"并且“收益”小于"收益2"并且“最高价”大于(“最新价”乘以(1+“回撤1”))时平仓
    # 多单：当“收益”大于"收益2"并且“收益”小于"收益3"并且“最高价”大于(“最新价”乘以(1+“回撤2”))时平仓
    # 多单：当“收益”大于"收益3"并且“收益”小于"收益4"并且“最高价”大于(“最新价”乘以(1+“回撤3”))时平仓
    # 多单：当“收益”大于"收益4"并且“收益”小于"收益5"并且“最高价”大于(“最新价”乘以(1+“回撤4”))时平仓
    # 多单：当“收益”大于"收益5"并且“收益”小于"收益6"并且“最高价”大于(“最新价”乘以(1+“回撤5”))时平仓
    # 多单：当“收益”大于"收益6"并且“最高价”大于(“最新价”乘以(1+“回撤6”))时平仓
    # 空单：当“收益”大于"收益1"并且“收益”小于"收益2"并且“最低价”小于(“最新价”乘以(1-“回撤1”))时平仓
    # 空单：当“收益”大于"收益2"并且“收益”小于"收益3"并且“最低价”小于(“最新价”乘以(1-“回撤2”))时平仓
    # 空单：当“收益”大于"收益3"并且“收益”小于"收益4"并且“最低价”小于(“最新价”乘以(1-“回撤3”))时平仓
    # 空单：当“收益”大于"收益4"并且“收益”小于"收益5"并且“最低价”小于(“最新价”乘以(1-“回撤4”))时平仓
    # 空单：当“收益”大于"收益5"并且“收益”小于"收益6"并且“最低价”小于(“最新价”乘以(1-“回撤5”))时平仓
    # 空单：当“收益”大于"收益6"并且“最低价”小于(“最新价”乘以(1-“回撤6”))时平仓

    if str(stop_pnl)=='0':
        return ''
    elif str(stop_pnl)=='1':
        if longnum>0 and longpnl > float(pnl_num):# 平多
            return 11
        elif shortnum>0 and shortpnl> float(pnl_num):# 平空
            return -11
    elif str(stop_pnl) == '2':
        if longnum > 0 and (last-longcost)/longcost > float(pnl_num):  # 平多
            return 11
        elif shortnum > 0 and (shortcost-last)/shortcost > float(pnl_num):  # 平空
            return -11
    elif str(stop_pnl) == '3':
        if longnum > 0 and float(h_longpnl) != 0 and (float(h_longpnl) - longpnl) / float(h_longpnl) > float(pnl_num):  # 平多
            return 11
        elif shortnum > 0 and float(h_shortpnl) > 0 and (float(h_shortpnl) - shortpnl) / float(h_shortpnl) > float(pnl_num):  # 平空
            return -11
    elif str(stop_pnl) == '4':
        if longnum > 0 and (float(h_last) - longcost) / longcost > float(pnl_num):  # 平多
            return 11
        elif shortnum > 0 and (shortcost - float(l_last)) / shortcost > float(pnl_num):  # 平空
            return -11
    elif str(stop_pnl) == '5':
        if longnum > 0 and last < float(h_last) and longcost != float(h_last) and (last - longcost) / (float(h_last) - longcost) > float(pnl_num):  # 平多
            return 11
        elif shortnum > 0 and last > float(l_last) and shortcost != float(l_last) and (shortcost - last) / (shortcost - float(l_last)) > float(pnl_num):  # 平空
            return -11
    elif str(stop_pnl) == '6':
        if longnum > 0 and last < float(h_last) and longcost * (1 + float(pnl_tag)) < last and last * (1 + float(pnl_num)) < float(h_last):  # 平多
            return 11
        elif shortnum > 0 and  last < float(l_last) and shortcost * (1 - float(pnl_tag)) > last and last * (1 - float(pnl_num)) > float(l_last):  # 平空
            return -11
    elif str(stop_pnl) == '7':##########################
        if longnum > 0:  # 平多
            # 多单：当“收益”大于"收益1"并且“收益”小于"收益2"并且“最高价”大于(“最新价”乘以(1+“回撤1”))时平仓
            # 多单：当“收益”大于"收益2"并且“收益”小于"收益3"并且“最高价”大于(“最新价”乘以(1+“回撤2”))时平仓
            # 多单：当“收益”大于"收益3"并且“收益”小于"收益4"并且“最高价”大于(“最新价”乘以(1+“回撤3”))时平仓
            # 多单：当“收益”大于"收益4"并且“收益”小于"收益5"并且“最高价”大于(“最新价”乘以(1+“回撤4”))时平仓
            # 多单：当“收益”大于"收益5"并且“收益”小于"收益6"并且“最高价”大于(“最新价”乘以(1+“回撤5”))时平仓
            # 多单：当“收益”大于"收益6"并且“最高价”大于(“最新价”乘以(1+“回撤6”))时平仓
            if longpnl>float(sy1) and longpnl<float(sy2) and float(h_last)>(last*(1+float(ht1))):
                return 11
            elif longpnl>float(sy2) and longpnl<float(sy3) and float(h_last)>(last*(1+float(ht2))):
                return 11
            elif longpnl>float(sy3) and longpnl<float(sy4) and float(h_last)>(last*(1+float(ht3))):
                return 11
            elif longpnl>float(sy4) and longpnl<float(sy5) and float(h_last)>(last*(1+float(ht4))):
                return 11
            elif longpnl>float(sy5) and longpnl<float(sy6) and float(h_last)>(last*(1+float(ht5))):
                return 11
            elif longpnl>float(sy6) and float(h_last)>(last*(1+float(ht6))):
                return 11

        elif shortnum > 0:  # 平空
            # 空单：当“收益”大于"收益1"并且“收益”小于"收益2"并且“最低价”小于(“最新价”乘以(1-“回撤1”))时平仓
            # 空单：当“收益”大于"收益2"并且“收益”小于"收益3"并且“最低价”小于(“最新价”乘以(1-“回撤2”))时平仓
            # 空单：当“收益”大于"收益3"并且“收益”小于"收益4"并且“最低价”小于(“最新价”乘以(1-“回撤3”))时平仓
            # 空单：当“收益”大于"收益4"并且“收益”小于"收益5"并且“最低价”小于(“最新价”乘以(1-“回撤4”))时平仓
            # 空单：当“收益”大于"收益5"并且“收益”小于"收益6"并且“最低价”小于(“最新价”乘以(1-“回撤5”))时平仓
            # 空单：当“收益”大于"收益6"并且“最低价”小于(“最新价”乘以(1-“回撤6”))时平仓
            if shortpnl>float(sy1) and shortpnl<float(sy2) and float(l_last) >0 and float(l_last)<(last*(1-float(ht1))):
                return -11
            elif shortpnl>float(sy2) and shortpnl<float(sy3) and float(l_last) >0 and float(l_last)<(last*(1-float(ht2))):
                return -11
            elif shortpnl>float(sy3) and shortpnl<float(sy4) and float(l_last) >0 and float(l_last)<(last*(1-float(ht3))):
                return -11
            elif shortpnl>float(sy4) and shortpnl<float(sy5) and float(l_last) >0 and float(l_last)<(last*(1-float(ht4))):
                return -11
            elif shortpnl>float(sy5) and shortpnl<float(sy6) and float(l_last) >0 and float(l_last)<(last*(1-float(ht5))):
                return -11
            elif shortpnl>float(sy6) and float(l_last) >0 and float(l_last)<(last*(1-float(ht1))):
                return -11

    return ''


def Stop_loss_now(stop_kx,kx_num,pt):#止损处理
    # stop_kx:止损处理类型,kx_num：止损量
    # longnum：多单持仓, longcost：多单均价, longpnl：多单盈利, shortnum：空单持仓, shortcost：空单均价, shortpnl：空单盈利, last：最新价
    # 返回值 11,-11   当需要平多返回11，当需要平空返回-11,其他值不处理
    longnum,longcost,longpnl,shortnum,shortcost,shortpnl,long_pnl_ratio,short_pnl_ratio,last = pt
    # 可选值说明 0:由策略自动处理；1:“亏损止损”就是当亏损大于下方填写的“止损量”时在无策略信号下就平仓;
    # 2“开仓比止损”就是当“开仓比”大于下方填写的“止损量”时在无策略信号下就平仓，
    # 多单：“最新价”比“开仓价”小，“开仓比”=("开仓价"-“最新价”)/"开仓价"
    # 空单：“最新价”比“开仓价”大，“开仓比”=(“最新价”-"开仓价")/"开仓价"
    # 3:“现价止损”就是多单：“现价”<="开仓价"X（1-"止损量"）,空单:“现价”>="开仓价"X（1+"止损量"）
    # 4:“开仓价止损”就是多单:“现价”<="开仓价"-"止损量",空单:“现价”>="开仓价"+"止损量"

    if str(stop_kx)=='0':
        return ''
    elif str(stop_kx)=='1':
        if longnum > 0 and longpnl < -float(kx_num):  # 平多
            return 11
        elif shortnum > 0 and shortpnl < -float(kx_num):  # 平空
            return -11
    elif str(stop_kx)=='2':
        if longnum > 0 and (longcost-last) / longcost > float(kx_num):  # 平多
            return 11
        elif shortnum > 0 and (last-shortcost) / shortcost > float(kx_num):  # 平空
            return -11
    elif str(stop_kx) == '3':
        if longnum > 0 and longcost * (1 - float(kx_num)) > last:  # 平多
            return 11
        elif shortnum > 0 and last > shortcost * (1 + float(kx_num)):  # 平空
            return -11
    elif str(stop_kx) == '4':
        if longnum > 0 and longcost - float(kx_num) > last:  # 平多
            return 11
        elif shortnum > 0 and last > shortcost + float(kx_num):  # 平空
            return -11

    return ''


def remark_to_positions_save(stop_pnl,pnl_num,stop_kx,kx_num,pt,parameters):
    longnum,longcost,longpnl,shortnum,shortcost,shortpnl,long_pnl_ratio,short_pnl_ratio,last = pt

    h_longpnl, h_shortpnl,h_last,pnl_tag,l_last,sy1,sy2,sy3,sy4,sy5,sy6,ht1, ht2, ht3, ht4, ht5, ht6 = parameters
    remark = ''
    if longnum != 0:
        remark = '多单'
        if longpnl > 0:  # 止盈
            remark += ',止盈'
            if str(stop_pnl) == '1':
                # and longpnl > float(self.pnl_num)
                # “获利止盈”就是当收益大于下方填写的“止盈量”时在无策略信号下就平仓
                remark += ',获利止盈,longpnl:%s>pnl_num:%s' % (longpnl, float(pnl_num))
            elif str(stop_pnl) == '2':
                # and (last - longcost) / longcost > float(self.pnl_num)
                # “开仓比止盈”就是当“开仓比”大于下方填写的“止盈量”时在无策略信号下就平仓，
                # 多单“开仓比”=(“最新价”-"开仓价")/"开仓价",空单“开仓比”=("开仓价"-“最新价”)/"开仓价"
                # self.cut_long()  # 平多
                remark += """,开仓比止盈,(last-longcost)/longcost:%s>pnl_num:%s
                            """ % ((last - longcost) / longcost, float(pnl_num))

            elif str(stop_pnl) == '3':
                if float(h_longpnl) == 0:
                    remark += """,获利回撤止盈,float(self.h_longpnl) == 0:%s
                                """ % (h_longpnl)
                else:
                    # and float(self.h_longpnl) != 0 and (
                    # float(self.h_longpnl) - longpnl) / float(self.h_longpnl) > float(self.pnl_num):
                    # “获利回撤止盈”就是记录的“最高收益”，当收益回撤时，
                    # (“最高收益”-“当前收益”)/“最高收益”大于下方填写的“止盈量”在无策略信号下就平仓;
                    remark += """
                                ,获利回撤止盈,float(self.h_longpnl)-longpnl)/float(self.h_longpnl):%s>self.pnl_num:%s
                                """ % ((float(h_longpnl) - longpnl) / float(h_longpnl), float(pnl_num))

            elif str(stop_pnl) == '4':
                # and (float(self.h_last) - longcost) / longcost > float(self.pnl_num)
                # “开仓比回撤止盈”就是记录的“最高价”或“最低价”，
                # 当价格回撤时多单是(“最高价”-“开仓价”)/“开仓价”，
                # 空单是(“开仓价”-“最低价”)/“开仓价”，大于填写的“止盈量”在无策略信号下就平仓;
                remark += """,开仓比回撤止盈,(float(self.h_last)-longcost)/longcost:%s>self.pnl_num:%s
                                    """ % ((float(h_last) - longcost) / longcost, float(pnl_num))

            elif str(stop_pnl) == '5':
                if last > float(h_last):
                    remark += """,价格比止盈,(last-longcost)/(float(self.h_last)-longcost):%s>self.pnl_num:%s
                                """ % ((last - longcost) / (float(h_last) - longcost), float(pnl_num))
                else:
                    # and (last - longcost) / (float(self.h_last) - longcost) > float(self.pnl_num)
                    # “价格比止盈”就是记录的“最高价”或“最低价”，
                    # 多单是(“最新价”-“开仓价”)/(“最高价”-“开仓价”)，
                    # 空单是(“开仓介”-“最新价”)/(“开仓介”-“最低价”)，
                    # 大于填写的“止盈量”在无策略信号下就平仓
                    remark += """,价格比止盈,(last-longcost)/(float(self.h_last)-longcost):%s>self.pnl_num:%s
                                        """ % ((last - longcost) / (float(h_last) - longcost), float(pnl_num))
            elif str(stop_pnl) == '6':
                # “动态止盈”就是记录的“最高价”或“最低价”，
                # 多单是当“开仓价”*(1+"参考量")<“现价”并且“现价”*(1+"止盈量")<“最高价”会平仓，
                # 空单是“开仓介”*(1-“参考量”)>"现价"并且“现价”*(1-"止盈量")>“最低价”;
                remark += """,动态止盈,longcost*(1+float(self.pnl_tag)):%s < last:%s 
                            and last*(1+float(self.pnl_num)):%s < float(self.h_last):%s 
                            and  last:%s<float(self.h_last):%s
                            """ % (
                longcost * (1 + float(pnl_tag)), last, last * (1 + float(pnl_num)), float(h_last), last,
                float(h_last))
            elif str(stop_pnl) == '7':
                if longpnl > float(sy1) and longpnl < float(sy2):
                    remark += """,多级动态止盈,longpnl:%s > float(sy1):%s and longpnl:%s < float(sy2):%s and float(h_last):%s > (last * (1 + float(ht1))):%s
                    """ % (longpnl,float(sy1), longpnl , float(sy2) , float(h_last) , (last*(1 + float(ht1))))


                elif longpnl > float(sy2) and longpnl < float(sy3):
                    remark += """,多级动态止盈,longpnl:%s > float(sy2):%s and longpnl:%s < float(sy3):%s and float(h_last):%s > (last * (1 + float(ht2))):%s
                                        """ % (
                    longpnl, float(sy2), longpnl, float(sy3), float(h_last), (last * (1 + float(ht2))))


                elif longpnl > float(sy3) and longpnl < float(sy4):
                    remark += """,多级动态止盈,longpnl:%s > float(sy3):%s and longpnl:%s < float(sy4):%s and float(h_last):%s > (last * (1 + float(ht3))):%s
                                        """ % (
                    longpnl, float(sy3), longpnl, float(sy4), float(h_last), (last * (1 + float(ht3))))


                elif longpnl > float(sy4) and longpnl < float(sy5):
                    remark += """,多级动态止盈,longpnl:%s > float(sy4):%s and longpnl:%s < float(sy5):%s and float(h_last):%s > (last * (1 + float(ht4))):%s
                                        """ % (
                    longpnl, float(sy4), longpnl, float(sy5), float(h_last), (last * (1 + float(ht4))))


                elif longpnl > float(sy5) and longpnl < float(sy6):
                    remark += """,多级动态止盈,longpnl:%s > float(sy5):%s and longpnl:%s < float(sy6):%s and float(h_last):%s > (last * (1 + float(ht5))):%s
                                        """ % (
                    longpnl, float(sy5), longpnl, float(sy6), float(h_last), (last * (1 + float(ht5))))


                elif longpnl > float(sy6):
                    remark += """,多级动态止盈,longpnl:%s > float(sy6):%s and float(h_last):%s > (last * (1 + float(ht6))):%s
                                        """ % (
                    longpnl, float(sy6), float(h_last), (last * (1 + float(ht6))))

            else:
                remark += """,策略止盈,self.stop_pnl:%s""" % stop_pnl

        elif longpnl < 0:  # 止损
            remark += ',止损'
            if str(stop_kx) == '1':
                # and longpnl < -float(self.kx_num)
                remark += ',亏损止损：longpnl：%s < -float(self.kx_num):%s' % (longpnl, -float(kx_num))

            elif str(stop_kx) == '2':
                # and (longcost - last) / longcost > float(self.kx_num)
                remark += """,开仓比止损：(longcost-last)/longcost：%s > float(self.kx_num):%s
                            """ % ((longcost - last) / longcost, float(kx_num))

            elif str(stop_kx) == '3':  # "开仓价"X（1-"止损量"）>=“现价”
                # and longcost * (1 - float(self.kx_num)) > last
                remark += """,现价止损：longcost*(1-float(self.kx_num))：%s > last:%s
                                    """ % (longcost * (1 - float(kx_num)), last)

            elif str(stop_kx) == '4':  # "开仓价"-"止损量">“现价”
                # and longcost * (1 - float(self.kx_num)) > last
                remark += """,开仓价止损：longcost-float(self.kx_num)：%s > last:%s
                                    """ % (longcost - float(kx_num), last)

            else:
                remark += ',策略止损:self.stop_kx:%s' %stop_kx
        else:
            remark += ',无盈亏'

    elif shortnum != 0:
        remark = '空单'
        if shortpnl > 0:  # 止盈
            remark += ',止盈'
            if str(stop_pnl) == '1':
                # and shortpnl > float(self.pnl_num)
                # “获利止盈”就是当收益大于下方填写的“止盈量”时在无策略信号下就平仓
                remark += ',获利止盈：shortpnl：%s > float(self.pnl_num):%s' % (shortpnl, float(pnl_num))

            elif str(stop_pnl) == '2':
                # and (shortcost - last) / shortcost > float(self.pnl_num)
                # “开仓比止盈”就是当“开仓比”大于下方填写的“止盈量”时在无策略信号下就平仓，
                # 多单“开仓比”=(“最新价”-"开仓价")/"开仓价",空单“开仓比”=("开仓价"-“最新价”)/"开仓价"
                remark += """,开仓比止盈：(shortcost-last)/shortcost：%s > float(self.pnl_num):%s
                            """ % ((shortcost - last) / shortcost, float(pnl_num))

            elif str(stop_pnl) == '3':
                # and float(self.h_shortpnl)>0
                # and (float(self.h_shortpnl) - longpnl) / float(self.h_shortpnl) > float(self.pnl_num)
                # “获利回撤止盈”就是记录的“最高收益”，当收益回撤时，
                # (“最高收益”-“当前收益”)/“最高收益”大于下方填写的“止盈量”在无策略信号下就平仓;
                if float(h_shortpnl) == 0:
                    remark += ',获利回撤止盈：float(self.h_shortpnl)=0:%s' % float(h_shortpnl)
                else:
                    remark += """
                            ,获利回撤止盈：float(self.h_shortpnl)-longpnl)/float(self.h_shortpnl):%s > float(self.pnl_num):%s
                                """ % ((float(h_shortpnl) - longpnl) / float(h_shortpnl), float(pnl_num))

            elif str(stop_pnl) == '4':
                # and (shortcost - float(self.h_last)) / shortcost > float(self.pnl_num)
                # “开仓比回撤止盈”就是记录的“最高价”或“最低价”，
                # 当价格回撤时多单是(“最高价”-“开仓价”)/“开仓价”，
                # 空单是(“开仓价”-“最低价”)/“开仓价”，大于下方填写的“止盈量”在无策略信号下就平仓;
                remark += """
                        ,开仓比回撤止盈：(shortcost-float(self.h_last))/shortcost:%s > float(self.pnl_num):%s
                        """ % ((float(h_shortpnl) - longpnl) / float(h_shortpnl), float(pnl_num))

            elif str(stop_pnl) == '5':
                if last < float(h_last):
                    remark += """
                    ,价格比止盈：(shortcost-last)/(shortcost-float(self.l_last)):%s > float(self.pnl_num):%s
                    """ % ((shortcost - last) / (shortcost - float(l_last)), float(pnl_num))
                else:
                    # and (shortcost - last) / (shortcost - float(self.l_last)) > float(self.pnl_num)
                    # “价格比止盈”就是记录的“最高价”或“最低价”，
                    # 多单是(“最新价”-“开仓价”)/(“最高价”-“开仓价”)，
                    # 空单是(“开仓介”-“最新价”)/(“开仓介”-“最低价”)，
                    # 大于下方填写的“止盈量”在无策略信号下就平仓
                    remark += """
                                ,价格比止盈：(shortcost-last)/(shortcost-float(self.l_last)):%s > float(self.pnl_num):%s
                                """ % ((shortcost - last) / (shortcost - float(l_last)), float(pnl_num))
            elif str(stop_pnl) == '6':
                remark += """
                ,动态止盈：shortcost*(1-float(self.pnl_tag)):%s > last:%s and last*(1-float(self.pnl_num))：%s > float(self.l_last):%s  and  last:%s<float(self.l_last):%s
                """ % (shortcost * (1 - float(pnl_tag)), last, last * (1 - float(pnl_num)), float(l_last), last,float(l_last))

            elif str(stop_pnl)=='7':
                if shortpnl > float(sy1) and shortpnl < float(sy2) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy1):%s and shortpnl:%s < float(sy2):%s and float(l_last):%s < (last * (1 - float(ht1))):%s
                    """%(shortpnl,float(sy1),shortpnl,float(sy2),float(l_last),(last * (1 - float(ht1))))

                elif shortpnl > float(sy2) and shortpnl < float(sy3) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy2):%s and shortpnl:%s < float(sy3):%s and float(l_last):%s < (last * (1 - float(ht2))):%s
                    """%(shortpnl, float(sy2), shortpnl, float(sy3), float(l_last), (last * (1 - float(ht2))))

                elif shortpnl > float(sy3) and shortpnl < float(sy4) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy3):%s and shortpnl:%s < float(sy4):%s and float(l_last):%s < (last * (1 - float(ht3))):%s
                    """%(shortpnl, float(sy3), shortpnl, float(sy4), float(l_last), (last * (1 - float(ht3))))

                elif shortpnl > float(sy4) and shortpnl < float(sy5) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy4):%s and shortpnl:%s < float(sy5):%s and float(l_last):%s < (last * (1 - float(ht4))):%s
                    """%(shortpnl, float(sy4), shortpnl, float(sy5), float(l_last), (last * (1 - float(ht4))))

                elif shortpnl > float(sy5) and shortpnl < float(sy6) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy5):%s and shortpnl:%s < float(sy6):%s and float(l_last):%s < (last * (1 - float(ht5))):%s
                    """%(shortpnl, float(sy5), shortpnl, float(sy6), float(l_last), (last * (1 - float(ht5))))

                elif shortpnl > float(sy6) and float(l_last) >0:
                    remark += """,多级动态止盈：shortpnl：%s > float(sy6):%s and float(l_last):%s < (last * (1 - float(ht6))):%s
                    """%(shortpnl, float(sy6), float(l_last), (last * (1 - float(ht6))))

            else:
                remark += ',策略止盈,self.stop_pnl:%s' % stop_pnl

        elif shortpnl < 0:  # 止损
            remark += ',止损'
            if str(stop_kx) == '1':
                # and shortpnl < -float(self.kx_num)
                remark += ',亏损止损:shortpnl:%s < -float(self.kx_num):%s' % (shortpnl, -float(kx_num))

            elif stop_kx == 2:
                # and (last - shortcost) / shortpnl > float(self.kx_num)
                remark += """
                            ,开仓比止损:(last-shortcost)/shortpnl:%s > float(self.kx_num):%s
                            """ % ((last - shortcost) / shortpnl, float(kx_num))

            elif str(stop_kx) == '3':
                # and last >= shortcost * (1 + float(self.kx_num))
                # “现价”>="开仓价"X（1+"止损量"）
                remark += """
                            ,现价止损:last:%s > shortcost*(1+float(self.kx_num)):%s
                            """ % (last, shortcost * (1 + float(kx_num)))
            elif str(stop_kx) == '4':
                # and last >= shortcost * (1 + float(self.kx_num))
                # “现价”>="开仓价"X（1+"止损量"）
                remark += """
                            ,现价止损:last:%s > shortcost+float(self.kx_num):%s
                            """ % (last, shortcost + float(kx_num))
            else:
                remark += ',策略止损,self.stop_kx:%s' %stop_kx
        else:
            remark += ',无盈亏'
    return remark





