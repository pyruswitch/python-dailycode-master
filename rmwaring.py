__author__ = 'vincent'
from pyquery import PyQuery as Pq
import time
import datetime
import StrUtil
import urllib
from testlogin import  Login
from testmail import send_mail


mailto_dict={"梁 其师":"qishi.liang@zuolin.com",
"Peng Hansen":"peng@zuolin.com",
"周 荟荣":"hera.zhou@zuolin.com",
"冯 业猛":"jack.feng@zuolin.com",
"Yang  Kelven":"kelven.yang@zuolin.com",
"杨 娟":"BBfly.yang@zuolin.com",
"王 重纲":"chonggang.wang@zuolin.com",
"郭 晓晶":"caroline.guo@zuolin.com",
"林 玉生":"ys.lin@zuolin.com",
"阳 兰芬":"catherine.yang@zuolin.com",
"韦 宁":"vincent.wei@zuolin.com",
"吴 寒":"han.wu@zuolin.com",
"杨 承立":"cl.yang@zuolin.com",
"韦 晟敢":"janson.wei@zuolin.com",
"冯 译萱":"yx.feng@zuolin.com",
"姚 业":"alex.yao@zuolin.com",
"熊 庆":"qing.xiong@zuolin.com",
"庄 家华":"jh.zhuang@zuolin.com",
"邱 露权":"Lewis.qiu@zuolin.com",
"李 祥涛":"xt.li@zuolin.com",
"戴 云":"stefan.dai@zuolin.com",
"林 龙":"long.lin@zuolin.com",
"陈 慕葶":"muting.chen@zuolin.com",
"丁 浩":"hao.ding@zuolin.com",
"谢 玲俐":"ll.xie@zuolin.com",
"耿 莉":"li.geng@zuolin.com",
"陈 伟杰":"weijie.chen@zuolin.com",
"刘 金文":"jinwen.liu@zuolin.com",
"龙 莎莎":"ss.long@zuolin.com",
"林 园":"yuan.lin@zuolin.com",
"宋 少良":"kevin.song@zuolin.com",
"吕 欣欣":"xinxin.lv@zuolin.com",
"熊 颖":"ying.xiong@zuolin.com",
"孙 存贤":"sky.sun@zuolin.com",
"高 磊":"lei.gao@zuolin.com",
"石 雨佳":"yujia.shi@zuolin.com",
"陆 勇":"yong.lu@zuolin.com",
"邓 荣君":"rj.deng@zuolin.com",
"方 丽娇":"lj.fang@zuolin.com",
"周 鹏":"peng.zhou@zuolin.com",
"颜 少凡":"sf.yan@zuolin.com",
"顾 芳丞":"fc.gu@zuolin.com",
"张 晓红":"xh.zhang@zuolin.com",
"许 娟":"juan.xu@zuolin.com",
"姚 绮云":"qiyun.yao@zuolin.com",
"李 磊":"lei.li@zuolin.com",
"黄 百途":"baitu.huang@zuolin.com",
"王 蓉蓉":"rr.wang@zuolin.com",
"孙 稳":"wen.sun@zuolin.com",
"刘 仲熙":"jessi.liu@zuolin.com",
"颜 婷":"ting.yan@zuolin.com",
"张 大伟":"dawei.zhang@zuolin.com",
"唐 彤":"tong.tang@zuolin.com",
"陈 航宇":"hy.chen@zuolin.com",
"唐 勇":"yong.tang@zuolin.com",
"刘 昕晖":"xh.liu@zuolin.com",
"朱 兰兰":"lanlan.zhu@zuolin.com",
"赖 凡":"fan.lai@zuolin.com",
"唐 艳芳":"yf.tang@zuolin.com",
"朱 睿":"ray.zhu@zuolin.com",
"杨 丹":"dan.yang@zuolin.com",
"田 晓强":"xq.tian@zuolin.com",
"李 佳兵":"jiabing.li@zuolin.com",
"何 智辉":"kyle.he@zuolin.com",
} #收件人(列表)
mail_host="smtp.mxhichina.com"            #使用的邮箱的smtp服务器地址
mail_user="devops@zuolin.com"                           #用户名
mail_pass="abc123!@#"                             #密码
mail_postfix="zuolin.com"                     #邮箱的后缀

get_ck=Login.redlogin("http://devops.lab.everhomes.com/login")
idlist=[52,54,55,56,57,58,59,60]
for id in idlist:
 get_page=Login.get_req("http://devops.lab.everhomes.com/projects/devops/issues?query_id={}".format(id))
 doc=Pq(get_page)
 tr_list=doc("#content > form:nth-child(4) > div > table > tbody>tr")
 for tr in tr_list:
    topic="#"+doc(tr)(" td.subject > a").text()+"#"
    tourl="http://devops.lab.everhomes.com/"+doc(tr)(" td.subject > a").attr("href")
    name=doc(tr)(" td.assigned_to > a").text()
    date=doc(tr)("td").eq(-2).text()
    if date=="":
        content="warning!!!\n"+'<html><body><p>您主题为 <a style="font-family:verdana;color:3366CC  ;font-size:18px;"  href='+tourl+'><u>'+topic+'</u></a>的任务目前处于预警状态且未填预期截止时间请及时处理</p></body></html>'
    else:
      date=datetime.datetime.strptime(date,"%Y-%m-%d")
      delay=(datetime.datetime.now()-date).days
      if delay>0:
        content="warning!!!\n"+'<html><body><p>您主题为 <a style="font-family:verdana;color:3366CC  ;font-size:18px;"  href='+tourl+'><u>'+topic+'</u></a>的任务已延期'+str(delay)+'天请及时处理<p></body></html>'
      else:
        content="warning!!!\n"+'<html><body><p>您主题为 <a style="font-family:verdana;color:3366CC  ;font-size:18px;"  href='+tourl+'><u>'+topic+'</u></a>的任务距离截止日期还剩'+str(abs(delay))+'天请及时处理</p></body></html>'
    addr=mailto_dict[name]

    if send_mail(addr,topic,content) : #邮件主题和邮件内容
      print(addr)
      print("done!")
      print(content)
    else:
        print( "failed!")