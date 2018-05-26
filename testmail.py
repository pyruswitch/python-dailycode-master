__author__ = 'vincent'

import smtplib
from email.mime.text import MIMEText


mailto_dict={'韦宁':'vincent.wei@zuolin.com',"邱 露权":"Lewis.qiu@zuolin.com","熊 庆":"qing.xiong@zuolin.com"}        #收件人(列表)
mail_host="smtp.mxhichina.com"            #使用的邮箱的smtp服务器地址
mail_user="devops@zuolin.com"                             #用户名
mail_pass="abc123!@#"                             #密码
mail_postfix="zuolin.com"                     #邮箱的后缀
def send_mail(mailtoaddr,sub,content):
    me="devpos"+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='html',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] =";".join(mailtoaddr)                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host,25)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me,mailtoaddr, msg.as_string())
        server.close()
        return True
    except Exception :
            print(Exception)
    return False
                              #发送2封，不过会被拦截的。。。
if __name__ == '__main__':
        tourl="http://devops.lab.everhomes.com/projects/devops/issues?query_id=46"
        topic=" test16"
        content='<html><body>' +' <a style="font-family:verdana;color:3366CC  ;font-size:22px;"  href='+tourl+'><u>'+topic+'</u></a>' + '</body></html>'
        #names=["韦宁"]
        #mailtoaddr=[]
        addr=[mailto_dict["韦宁"],mailto_dict["邱 露权"],mailto_dict["熊 庆"]]
        #addr="vincent.wei@zuolin.com"
            #mailtoaddr.append(addr)
        send_mail(addr,topic,content)  #邮件主题和邮件内容
        #print(mailtoaddr)
        print("done!")
else:
        print( "failed!")