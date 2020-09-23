# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  """admin/dl/BASE_DL.py"""
##############################################################################

import base64
import json
import time
import random
import traceback
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from basic.VIEW_TOOL import cDL
from basic.JD_TOOL import robot_bugerror
import okexapi.account_api as account

class cBASE_DL(cDL):

    def get_user_tag(self):
        sql = """select id,cname
            from user_tag where usr_id=%s order by sort"""

        L, t = self.db.select(sql, [self.usr_id])
        return L

    def sendMselectData(self, ListData, hid_cols=0):
        # 发送mselect列表数据
        # 这里重写是因为要处理那个显示和实际的列不一样
        # hid_cols 隐藏后面多少列
        res = {'list': [], 'value': []}
        if len(ListData) > 0:
            if hid_cols != 0:  # 不为零说明需要隐藏后面的N 列
                tmp_list = []
                for r in ListData:
                    row_tmp = eval('r[:-%s]' % hid_cols)  # 例子 row_tmp = r[:-2]
                    tmp_list.append(row_tmp)
                res['list'] = tmp_list
            else:
                res['list'] = ListData  # 显示用的结果集
            tmp = []
            for row in ListData:
                try:
                    t = '###'.join(row)  # 要保证row 里面全部都是字符串类型的，要不然会报错，当然下面我处理了
                except TypeError:
                    row_tmp = []
                    for r in row:
                        row_tmp.append(str(r))
                    t = '###'.join(row_tmp)
                tmp.append(t)
            res['value'] = tmp# 选择用的结果集
        return res


    def local_ajax_getTree(self):
        L=[]
        # sql = """
        #     select
        #         id,pid,cname,ilevel
        #         from category
        #         where usr_id=%s and  COALESCE(del_flag,0)=0 or id=1
        #         order by ilevel,paixu,id
        # """
        # lT, iN = self.db.select(sql,self.usr_id_p)
        # if iN>0:
        #     L = lT
        return L

    def local_ajax_getGoods(self):

        keywords = self.GP('keyword', '')
        tree_pk = self.GP('tree_pk', '')
        rL = []
        sql = """
        select open_id as id,nick_name from wechat_mall_user 
        where coalesce(status,0)=0 and coalesce(del_flag,0)=0 and usr_id=%s
        """
        parm=[self.usr_id]
        if keywords!='':#name
            sql+="and  (nick_name like %s or open_id like %s ) "
            parm.append('%%%s%%,%%%s%%'%(keywords,keywords))
        # if tree_pk != '' and tree_pk != '1':#category_ids
        #     sql += "and  category_ids like %s "
        #     parm.append('%%%s%%' % tree_pk)
        sql += """  order by id """
        lT, iN = self.db.fetchall(sql,parm)
        if iN > 0:
            rL = [lT, iN]

        return rL

    def decryption_data(self,data):
        #key = self.GJ('key', '')
        try:
            cipher_text = base64.b64decode(data.encode('utf8'))
            rsa_private_key = self.pemkey.encode('utf8')
            rsakey = RSA.importKey(rsa_private_key)
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            text = cipher.decrypt(cipher_text, None)
            V = json.loads(text.decode('utf8'))
            return V
        except Exception as e:
            print(e)
            return {}

    def get_random_no(self,E_R=2, T=''):
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

    def apikey_check(self,api_key,secret_key,passphrase):

        accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)
        try:
            result = accountAPI.coin_transfer('', '', 1, 1, 5, sub_account='', instrument_id='', to_instrument_id='')
        except:
            robot_bugerror(traceback,'apikey_check')
            return 3
        if result["code"] == 30006:
            #print("密钥校验有误")
            return 1
        elif result["code"] == 30012:
            #print("没有权限哦")
            return 2
        else:
            return 0






