# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910 admin/vi/A001.py
##############################################################################

from importlib import reload
from basic.JD_TOOL import DEBUG
if DEBUG == '1':
    import admin.vi.BASE_TPL
    reload(admin.vi.BASE_TPL)
from admin.vi.BASE_TPL import cBASE_TPL



class cA001(cBASE_TPL):
    
    def setClassName(self):
        self.dl_name = 'A001_dl'


    def goPartList(self):

        self.getBreadcrumb() #获取面包屑
        self.assign('NL', self.dl.GNL)
        PL, L = self.dl.mRight()
        self.assign('dataList', L)
        self.getPagination(PL)
        return self.runApp('A001_list.html')


    def goPartsave_deal(self):
        dR=self.dl.save_deal_data()
        return self.jsons(dR)

    def goPartupdeal(self):
        dR=self.dl.updeal_data()
        return self.jsons(dR)

    def goPartedit_row(self):
        dR=self.dl.edit_row_data()
        return self.jsons(dR)


    def goPartall_row(self):
        dR=self.dl.all_row_data()
        return self.jsons(dR)

    def goPartAlldelete(self):#删除选择
        dR=self.dl.Alldelete_data()
        return self.jsons(dR)

    def goPartclean_all(self):#持仓全平选择
        dR=self.dl.clean_all_data()
        return self.jsons(dR)

    def goPartpasue_all(self):#停止选择
        dR=self.dl.pasue_all_data()
        return self.jsons(dR)

    def goPartrun_all(self):#运行选择
        dR=self.dl.run_all_data()
        return self.jsons(dR)

    def goPartpasue_r(self):#停止单个
        dR=self.dl.pasue_r_data()
        return self.jsons(dR)

    def goPartrun_r(self):#运行单个
        dR=self.dl.run_r_data()
        return self.jsons(dR)

    def goPartclean_r(self):#平仓单个
        dR=self.dl.clean_r_data()
        return self.jsons(dR)


    def initPagiUrl(self):
        url = self.sUrl
        if self.part:
            url += "&part=%s" % self.part
        return url

    def pagination(self, count, page, pagesize=10, url='', params={}):
        self.assign('iTotal_length',count)
        pagenum = 6
        prepage = pagesize
        curpage = int(page)
        pagestr = ''
        pagestrs = '''<div class="pagination_div">
                        <div class="jumppage"  style="position:relative;float:right;display:inline-block;margin:28px 50px 20px auto;">
                        <span style="color:#333333;"></span>
                    </div>
                            <div style="clear:both"></div>
                        </div>
                    '''

        start = (curpage - 1) * pagesize + 1
        end = start + pagesize - 1
        if end > count:
            end = count

        if url.find('?') >= 0:
            url += '&'
        else:
            url += '?'
        paramurl = '&'.join('%s=%s' % (k, v) for k, v in params.items())
        if paramurl != '': url += paramurl + '&'
        # print url
        realpages = 1
        if (float(count) > prepage):
            t = float(count) / prepage
            if t > int(t):
                realpages = int(t) + 1
            else:
                realpages = int(t)
            # realpages = @ceil()
            if (realpages < pagenum):
                froms = 1
                to = realpages
            else:
                offset = (pagenum / 2)
                froms = curpage - offset
                to = froms + pagenum
                if (froms < 1):
                    froms = 1
                    to = froms + pagenum - 1
                elif (to > realpages):
                    to = realpages
                    froms = realpages - pagenum + 1

            pagestr += '<li><a href="%spageNo=1">第一页</a></li>' % url
            if curpage - 1 > 0: pagestr += '<li><a href="%spageNo=%s">上一页</a></li>' % (url, curpage - 1)

            for i in range(int(froms), int(to) + 1):
                if (i == curpage):
                    pagestr += '<li class="active"><a>%s</a></li>' % (i)
                else:
                    pagestr += '<li><a href="%spageNo=%s">%s</a></li>' % (url, i, i)
            if (curpage < realpages): pagestr += '<li><a href="%spageNo=%s">下一页</a></li>' % (url, curpage + 1)
            pagestr += '<li><a href="%spageNo=%s">最后页</a></li>' % (url, realpages)
            pagestr = '<ul class="pagination" style="display:inline-block;padding-left:10px;">%s</ul>' % (pagestr)
            pagestrs = '''
                <div class="pagination_div">
                        %s
                    <div class="jumppage"  style="position:relative;float:right;display:inline-block;margin:28px 50px 20px auto;">
                        <span style="color:#333333;">共有&nbsp;%s&nbsp;条记录,此为第%s-%s条</span>
                    </div>
                    <div style="clear:both"></div>
                </div>
                <script>
                    function gotopage(page){
                        var keywork=$('input[name=help_search_input]').val();
                        var page=checkPage(page)
                        var url="%s";
                        if($("input[name=pageSize]").length > 0){
                            var pageSize=$("input[name=pageSize]").val();
                            url += "&pageSize="+pageSize;
                        }
                        window.location.href=url+"&pageNo="+page;
                    }

                    function jumppage(){
                        var page=$("input[name=jumppage]").val();
                        gotopage(page);
                    }
                    function checkNum(obj){
                        if(!$(obj).val().match(/^[0-9]+[0-9]*]*$/)){
                            $(obj).val('1');
                        }
                    }

                    function checkPage(page){
                        var total=$("input[name=total]").val();
                        var pageSize=$("input[name=pageSize]").val();
                        var total_pages=Math.ceil(total/pageSize);
                        if ( parseInt(page,10) < 1 || total_pages==0){
                            page=1;
                        }else{
                            if (parseInt(page,10) > parseInt(total_pages,10)){
                                page=parseInt(total_pages,10);
                            }
                        }
                        return page;
                    }
                </script>
            ''' % (pagestr, count, start, end, url)

        return pagestrs

    
    
    
        
 