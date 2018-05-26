# -*- coding: utf-8 -*-
__author__ = 'vincent'
import mysql.connector
import operator
from testlogin import  Login
import smtplib
from email.mime.text import MIMEText
import datetime
import time




mail_host="smtp.mxhichina.com"            #使用的邮箱的smtp服务器地址
mail_user="devops@zuolin.com"                           #用户名
mail_pass="abc123!@#"                             #密码
mail_postfix="zuolin.com"


def send_mail(mailtoaddr,sub,content):
    me="devpos"+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailtoaddr)          #将收件人列表以‘；’分隔
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


def dbsql (selectsql):#数据库查询

    user="ning.wei15"
    pwd="wn3333"
    host="bizdb.zuolin.com"
    db="ehbiz"
    port="18306"

    cnx=mysql.connector.connect(user=user,password=pwd,database=db,host=host,port=port)
    cursor=cnx.cursor()
    select_sql=selectsql

    cursor.execute(select_sql)
    alldata=cursor.fetchall()
    #alldata.sort(key=operator.itemgetter(0))
    return alldata

def bookinglunch():
    select_sql='''
   SELECT DISTINCT
c.`shop_name`,a.`order_no`,a.`buyer_nick_name`,a.`buyer_phone`,a.`pay_type`,e.`cat_name`,e.`supplier_name`,b.`prod_name`,e.`model`,d.`current_prime_price`,b.`price`,b.`quantity`,a.`price_total`,a.`discount_total`,a.`paid_total`,a.`activity_benefit_amount`,g.`description`,a.`payment_time`
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN  `tbl_order_item`b
ON b.`order_no`=a.`order_no`
LEFT JOIN `tbl_model`d
ON b.`prod_no`=d.`model_no`
LEFT JOIN `tbl_commodity`e
ON d.`commo_no`=e.`commo_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>date_format(now(),'%Y-%m-%d')
AND a.`basic_state`!=1
AND a.`shop_no`IN("14923963824806752750","14477417463124576784","14622779991551986272")
and e.`cat_name`like"%盒饭%"
and date_format(a.`payment_time`,'%H')>=14
AND DATE_FORMAT(a.`payment_time`,'%H')<=20
        '''
    alldata=dbsql(select_sql)
    content=""
    for data in alldata:

         data=str(data)
         content=content+'<br>'+data
    addr={"vincent.wei@zuolin.com","Lewis.qiu@zuolin.com"}
    today = datetime.date.today()
    topic=str(today.strftime("%Y/%m/%d"))+"-午餐预定情况"
    if send_mail(addr,topic,content) : #邮件主题和邮件内容
      print(addr)
      print("done!")
      print(content)
    else:
        print( "failed!")

if __name__ == '__main__':
    while True:
       current_time = time.localtime(time.time())
       if((current_time.tm_hour == 20) and (current_time.tm_min == 10) and (current_time.tm_sec == 0)):
            bookinglunch()
       time.sleep(1)