# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  admin/vi/H001.py
##############################################################################

from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL import cBASE_TPL

class cH001(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'H001_dl'

    def goPartList(self):
        self.assign('NL', self.dl.GNL)
        self.initHiddenLocal()  # 初始隐藏域
        self.navTitle = '我的帐户'
        self.getBreadcrumb() #获取面包屑
        L1,info = self.dl.getInfo()
        self.assign('info',info)
        self.assign('dataList', L1)
        return self.runApp('H001_list.html')

    def goPartSearch(self):
        dR = self.dl.Search_data()
        return self.jsons(dR)

    def goPartupps(self):
        dR = self.dl.upps_data()
        return self.jsons(dR)

    def goPartbourse_users(self):
        dR=self.dl.bourse_users_data()
        return self.jsons(dR)

    def goPartdel_r(self):
        dR=self.dl.del_r_data()
        return self.jsons(dR)
    
    
    
    
        
 