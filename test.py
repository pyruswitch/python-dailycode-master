# coding=utf-8
# -*- coding: utf-8 -*-
__author__ = 'wuhan'
import  datetime
import time
import urllib
from functools import reduce
from time import sleep
import mysql.connector
import random
import math
import calendar
from tqdm import tqdm
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
'''def mod(x, y):
    t = x % y
    while (t != 0):
        x = y
        y = t
        t = x % y
    return y


print(mod(20, 10))'''
'''datetime=datetime.datetime(2016, 7, 15, 13, 12, 19)
ostime=datetime.strftime("%H")


times=str(ostime)+"—"+str(int(ostime)+1)
print(ostime)
print(times)
'''



'''adict={"a":"bcde","c":"d","e":"f"}

value=adict["a"]
print(value)'''
'''d1 = datetime.datetime.strptime('2012-03-05 17:41:20', '%Y-%m-%d %H:%M:%S')
d2 = datetime.datetime.strptime('2012-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
delta = d1 - d2
print (delta.days)'''
'''url="http://www.newrank.cn/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#伪装浏览器
request = urllib.request.Request(url=url, headers=headers)
#构造请求
m_fp = urllib.request.urlopen(request, timeout=500)
#访问网站获取源码
html_str = m_fp.read().decode('utf-8')'''
'''li=[("a",1),("b",2),("c",3),("d",4),("e",5)]
#testsum=reduce(lambda x,y:sum(x[1]for x  in li), li)
testsum=min(x[1] for x  in li)
print(testsum)'''
'''user="ning.wei12"
pwd="wn3633"
host="bizdb.zuolin.com"
db="ehbiz"
port="18306"

cnx=mysql.connector.connect(user=user,password=pwd,database=db,host=host,port=port)
cursor=cnx.cursor()
def test():
    userbase_sql='''

''' SELECT
    a.`buyer_no`,a.`buyer_nick_name`,a.`buyer_phone`,COUNT(a.`buyer_no`),SUM(a.`paid_total`),AVG(a.`paid_total`), MIN(a.`payment_time`),MAX(a.`payment_time`),
   (SELECT b.`paid_total` FROM `tbl_order`b
   WHERE b.`buyer_no`=a.`buyer_no`AND b.`payment_time`=MIN(a.`payment_time`))AS firstpaid
   FROM
   `tbl_order`a
   WHERE
   a.`payment_time`>"2015-12-25"
   GROUP BY a.`buyer_no`
   ORDER BY COUNT(a.`buyer_no`)DESC''''''

    cursor.execute(userbase_sql)
    usbdata=cursor.fetchall()
for i in tqdm(range(1,2)):
    test()'''

'''a=[1,2,3]
print(len(a))'''

'''a=1
b=2
c=3
d1={}
d1[a]={}
d1[a][b]={}
d1[a][b]=c
print(d1)'''
'''shoplist=["a","b"]
shopsupdict={}
suplist=[["c","d"],["c","d"]]
prolist=[[1,2,3],[4,5],[6,7],[8,9]]
suppronum=0
shopsupnum=0
for shopi in shoplist:
    shopsupdict[shopi]={}
    supi=suplist[shopsupnum]
    for supdata in supi :
        shopsupdict[shopi][supdata]={}
        shopsupdict[shopi][supdata]=prolist[suppronum]
        suppronum=suppronum+1
    shopsupnum=shopsupnum+1
print(shopsupdict)
'''
'''a=[1,2,3,4,5,6]
b=[6,3,8,3,1,4,10,1,12,15]
new=[]
for i in b :
    if i not in a:
        new.append(i)
for newi in new:
    b.remove(newi)
sorted(b,key=a.index)
for newi in  new:
    b.append(newi)
print(b)'''
'''count=23
all=23
alen=4
endnum=math.ceil(count/alen)
countli=[]
amount=0
if count <10:
   endnum=math.ceil(count/2)
elif 10<count<30 :
    endnum=math.ceil(count/4)
else :
    endnum=math.ceil(count/6)
while count>=2:
  a=random.randint(2,endnum)
  count=count-a
  countli.append(a)
  amount=amount+a
  print(amount)
  if count==1:
      countli.append(count)
      break
  if len(countli)+1==alen:
      countli.append(all-amount)
      break

print(sorted(countli,reverse=True))'''
'''now = datetime.datetime.now()
today_year = now.year
data_list_todays = []
today_year_months = range(1,now.month+1)
for today_year_month in today_year_months:
    # 定义date_list 去年加上今年的每个月
    data_list = '%s/%s' % (today_year, today_year_month)
    #通过函数append，得到今年的列表
    data_list_todays.append(data_list)
print (data_list_todays)'''

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os

def text1():
    print("'Tick1! The time is: {}".format(datetime.now()))

def text2():
    print("'Tick2! The time is: {}".format(datetime.now()))

def tick1():
    text1()
    scheduler.add_job(text1, 'interval', minutes = 1)

def tick2():
    text2()
    scheduler.add_job(text2, 'interval', minutes =3)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick1, 'cron', day_of_week='mon-sun', hour=15, minute=49,end_date='2017-12-30')
    scheduler.add_job(tick2, 'cron', day_of_week='mon-sun', hour=15, minute=49,end_date='2017-12-30')

    try:
        scheduler.start()
    except(KeyboardInterrupt, SystemExit):
        scheduler.shutdown()











