# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################
"""admin/vi/home.py"""

from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)

from admin.vi.BASE_TPL import cBASE_TPL


class chome(cBASE_TPL):

    def setClassName(self):
        self.dl_name = 'home_dl'

    def specialinit(self):

        self.tab_data = ['策略运行日志','持仓日志', '止盈止损日志','持仓流水']
        self.assign('tab_data', self.tab_data)
        self.assign('tab', self.dl.tab)

    def initPagiUrl(self):

        url = self.sUrl
        if self.dl.tab:
            url += "&tab=%s" %self.dl.tab
        if self.dl.qqid:
            url += "&qqid=%s" % self.dl.qqid
        return url

    def goPartList(self):
        self.currentUrl = self.sUrl
        self.assign('currentUrl', self.currentUrl)
        self.getBreadcrumb()  # 获取面包屑
        self.assign('NL1', self.dl.GNL1)
        self.assign('NL2', self.dl.GNL2)
        self.assign('NL3', self.dl.GNL3)
        self.assign('NL4', self.dl.GNL4)
        PL, L = self.dl.mRight()
        self.getPagination(PL)
        self.assign('dataList', L)
        return self.runApp('home.html')

    def getPagination(self, PL):
        self.cur_page = PL[0]
        self.total_pages = PL[1]
        PagiUrl = self.initPagiUrl()
        html_pager = self.pagination(PL[2], self.cur_page,PL[3], url=PagiUrl)
        self.assign('html_pager', html_pager)

