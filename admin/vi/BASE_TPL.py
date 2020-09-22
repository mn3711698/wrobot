# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910
##############################################################################
"""admin/vi/BASE_TPL.py"""

from basic.VIEW_TOOL import cVIEWS

class cBASE_TPL(cVIEWS):

    def goPartUpload(self):
        url = self.dl.Upload()
        return self.jsons({'url': url})

    def goPartPem_upload(self):
        url = self.dl.Pem_upload()
        return self.jsons({'url': url})

    def goPartSave_type(self):#增加广告类型
        dR=self.dl.save_type()
        return self.jsons(dR)

    def goPartSave_ctype(self):#增加广告类型
        dR=self.dl.save_ctype()
        return self.jsons(dR)

    def goPartDel_qiniu_pic(self):#删除七牛照片
        dR=self.dl.del_qiniu_pic()
        return self.jsons(dR)






