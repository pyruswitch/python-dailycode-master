# -*- coding: utf-8 -*-
__author__ = 'vincent'
#from openpyxl import Workbook
#from openpyxl.reader.excel import load_workbook
import mysql.connector
import operator
import datetime

def dbsql (selectsql):#数据库查询

    user="ning.wei12"
    pwd="wn3633"
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



def incomedata():#流水数据

    selectsql='''SELECT
    DATE_FORMAT(a.`pay_date`,'%Y-%m-%d'),c.`shop_name`,a.`pay_no`,a.`pay_type`,a.`order_no`,a.`order_type`,a.`pay_amount`,a.`online_pay_style_no`,a.`realm`
    FROM
    `pay_info_record`a
    LEFT JOIN
    `tbl_order`b
    ON b.`order_no`=a.`order_no`
    LEFT JOIN
    `tbl_shop_info`c
    ON c.`shop_no`=b.`shop_no`
    WHERE
    a.`pay_date`>"2016-11-01"
    AND c.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
    AND c.`shop_name` IS NOT NULL
    AND a.`pay_status`="success"'''

    allincomedata=dbsql(selectsql)#原始流水数据
    dayincomelist=[t[0]for t in allincomedata]
    dayinlist=set(dayincomelist)
    dayinlist=list(dayinlist)
    dayinlist.sort()#日期列表
#--------------------------渠道流水趋势--------------------------------------------------------------------------------
    channelincomelist=[t[3]for t in allincomedata]
    channlist=set(channelincomelist)#渠道列表
    onlineincom_list=[]
    lineincom_list=[]
    dayintal_list=[]
    for  iday in dayinlist:
        dayintotal=0
        onlinechannincom=0
        linechannincom=0
        for idata in allincomedata:
                if idata[0]==iday:
                   dayintotal=dayintotal+idata[6]
                   dayintotal=round(dayintotal)
                   if idata[3]==1:
                        onlinechannincom=onlinechannincom+idata[6]
                        onlinechannincom=round(onlinechannincom,2)
                   elif idata[3]==3:
                        linechannincom=linechannincom+idata[6]
                        linechannincom=round(linechannincom,2)
        dayintal_list.append(dayintotal)
        onlineincom_list.append(onlinechannincom)
        lineincom_list.append(linechannincom)

#--------------------------站点流水趋势--------------------------------------------------------------------------------
    shopincomelist=[t[1]for t in allincomedata]
    shoplist=set(shopincomelist)


    num=0
    shopnumlist=[]
    for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopincome=0
             for idata in allincomedata:
                 if  idata[0]==iday:
                     if idata[1]==ishop:
                         shopincome=shopincome+idata[6]
                         shopincome=round(shopincome,2)
             shopnumlist[num].append(shopincome)
        num=num+1

    return dayinlist ,onlineincom_list,lineincom_list,shoplist,shopnumlist,dayintal_list

def lunchsaledata():#午餐销量
     selectsql='''
         SELECT DISTINCT
c.`shop_name`,SUM(b.`quantity`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
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
WHERE
 a.`payment_time`>"2016-11-01 00:00:00"
AND a.`basic_state`!=1
AND e.`cat_name`="盒饭"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),c.`shop_name`
     '''
     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopincomelist=[t[0]for t in allincomedata]
     shoplist=set(shopincomelist)
     shoplist=list(shoplist)
     shopinlunchlist=[]

     num=0
     shopnumlist=[]
     for ishop in shoplist:
            shopnumlist.append([])
            for iday in dayinlist:
                 shoplunchsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==ishop:
                             shoplunchsale=shoplunchsale+idata[1]
                             shoplunchsale=int(shoplunchsale)
                 shopnumlist[num].append((shoplunchsale))
            num=num+1
     for iday in dayinlist:
                shopintotallunch=0
                for idata in allincomedata:
                     if  idata[2]==iday:
                         shopintotallunch=shopintotallunch+int(idata[1])
                shopinlunchlist.append(shopintotallunch)
     return dayinlist ,shoplist,shopnumlist,shopinlunchlist

def lunchpercentdata():#午餐流水占比销量
     selectsql='''
         SELECT
c.`shop_name`,e.`cat_name`,SUM(d.`price`*b.`quantity`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
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
WHERE
 a.`payment_time`>"2016-11-01 "
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY c.`shop_name`,e.`cat_name`,DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
     '''
     allincomedata=dbsql(selectsql)#原始数据
     dayincomelist=[t[3]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopincomelist=[t[0]for t in allincomedata]
     shoplist=set(shopincomelist)
     shoplist=list(shoplist)
     shopinlunchlist=[]

     num=0
     shopnumlist=[]
     for ishop in shoplist:
            shopnumlist.append([])
            for iday in dayinlist:
                 shoplunchsale=0
                 lunchpri=0
                 otherpri=0
                 for idata in allincomedata:
                     if  idata[3]==iday:
                         if idata[0]==ishop:
                             if idata[1]=="盒饭":
                                lunchpri=lunchpri+idata[2]
                             else:
                                otherpri=otherpri+idata[2]
                 if (lunchpri+otherpri)==0:
                         shoplunchsale=0
                 else:
                         shoplunchsale=round((lunchpri/(lunchpri+otherpri)),2)
                 shopnumlist[num].append((shoplunchsale))
            num=num+1
     for iday in dayinlist:
                shopintotallunch=0
                lunchpri=0
                otherpri=0
                for idata in allincomedata:
                     if  idata[3]==iday:
                         if idata[1]=="盒饭":
                                lunchpri=lunchpri+idata[2]
                         else:
                                otherpri=otherpri+idata[2]
                if (lunchpri+otherpri)==0:
                         shopintotallunch=0
                else:
                   shopintotallunch=round((lunchpri/(lunchpri+otherpri)),2)
                shopinlunchlist.append(shopintotallunch)
     return dayinlist ,shoplist,shopnumlist,shopinlunchlist

def suppliersaledata():#午餐供应商
     selectsql='''SELECT DISTINCT
e.`supplier_name`,SUM(b.`quantity`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
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
WHERE
 a.`payment_time`>"2016-11-01 00:00:00"
AND a.`basic_state`!=1
AND e.`cat_name`="盒饭"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),e.`supplier_name` '''

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     supincomelist=[t[0]for t in allincomedata]
     suplist=set(supincomelist)
     suplist=list(suplist)


     num=0
     supnumlist=[]
     for isup in suplist:
            supnumlist.append([])
            for iday in dayinlist:
                 suplunchsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             suplunchsale=suplunchsale+idata[1]
                             suplunchsale=int(suplunchsale)
                 supnumlist[num].append((suplunchsale))
            num=num+1

     return dayinlist ,suplist,supnumlist

def shopwastagedata():#损耗
     selectsql=''' SELECT DISTINCT
c.`shop_name`,d.`cat_name`,d.`supplier_name`,b.`commo_name`,a.`reduce_stock_type`,a.`description`,a.`stock`,a.`price`,DATE_FORMAT(a.`create_time`,'%Y-%m-%d')
FROM
`tbl_shop_commodity_log`a
LEFT JOIN
`tbl_shop_model`b
ON a.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN
`tbl_commodity`d
ON a.`commo_no`=d.`commo_no`
WHERE
 a.`operate_type`=2
AND a.`reduce_stock_type`=2
AND a.`create_time`>"2016-11-01" '''
     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[8]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     supwastlist=[t[2]for t in allincomedata]
     supwastlist=set(supwastlist)
     waslist=list(supwastlist)


     num=0
     supwaslist=[]
     for iwas in waslist:
            supwaslist.append([])
            for iday in dayinlist:
                 supwastage=0
                 for idata in allincomedata:
                     if  idata[8]==iday:
                         if idata[2]==iwas:
                             supwastage=supwastage+idata[6]
                             supwastage=int(supwastage)
                 supwaslist[num].append((supwastage))
            num=num+1

     return dayinlist ,waslist,supwaslist

def userdata():
     selectsql='''
    SELECT
DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),a.`pay_type`,COUNT(DISTINCT a.`buyer_no`)
FROM
`tbl_order` a
LEFT JOIN
`tbl_shop_info`b
ON b.`shop_no`=a.`shop_no`
WHERE
a.`payment_time`>"2016-11-01"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),a.`pay_type`
    '''#渠道用户趋势
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[0]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     typelist=[t[1]for t in alldata]
     typelist=set(typelist)
     typelist=list(typelist)
     onlineuserlist=[]
     lineuserlist=[]
     totaluserlist=[]

     for iday in dayinlist:
         userintotal=0
         onlineusercount=0
         lineusercount=0
         for idata in alldata:
                  if idata[0]==iday:
                     userintotal=userintotal+int(idata[2])
                     if idata[1]==1:
                        onlineusercount=onlineusercount+int(idata[2])
                     elif idata[1]==3:
                        lineusercount=lineusercount+int(idata[2])
         totaluserlist.append(userintotal)
         onlineuserlist.append(onlineusercount)
         lineuserlist.append(lineusercount)
     return dayinlist,totaluserlist,onlineuserlist,lineuserlist
def shopuserdata():
     selectsql='''
    SELECT
DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`,COUNT(a.`buyer_no`)
FROM
`tbl_order` a
LEFT JOIN
`tbl_shop_info`b
ON b.`shop_no`=a.`shop_no`
WHERE
a.`payment_time`>"2016-11-01"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`
    '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[0]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopnamelist=[t[1]for t in alldata]
     shoplist=set(shopnamelist)
     shoplist=list(shoplist)


     num=0
     shopnumlist=[]
     for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopusercount=0
             for idata in alldata:
                 if  idata[0]==iday:
                     if idata[1]==ishop:
                         shopusercount=shopusercount+int(idata[2])
             shopnumlist[num].append(shopusercount)
        num=num+1
     return dayinlist,shoplist,shopnumlist
def newusertype():
     selectsql='''
    SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"2016-11-01"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"2016-11-01"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''#渠道新用户趋势
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[4]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     typelist=[t[2]for t in alldata]
     typelist=set(typelist)
     typelist=list(typelist)
     onlinenewuserlist=[]
     linenewuserlist=[]
     totalnewuserlist=[]

     for iday in dayinlist:
         userintotal=0
         onlineusercount=0
         lineusercount=0
         for idata in alldata:
                  if idata[4]==iday:
                     userintotal=userintotal+1
                     if idata[2]==1:
                        onlineusercount=onlineusercount+1
                     elif idata[2]==3:
                        lineusercount=lineusercount+1
         totalnewuserlist.append(userintotal)
         onlinenewuserlist.append(onlineusercount)
         linenewuserlist.append(lineusercount)
     return dayinlist,totalnewuserlist,onlinenewuserlist,linenewuserlist

def onlinenewuser():
     selectsql='''
  SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"2016-11-01"
 AND a.`pay_type`=1
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"2016-11-01"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[4]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopnamelist=[t[1]for t in alldata]
     shoplist=set(shopnamelist)
     shoplist=list(shoplist)


     num=0
     shopnumlist=[]
     for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopusercount=0
             for idata in alldata:
                 if  idata[4]==iday:
                     if idata[1]==ishop:
                         shopusercount=shopusercount+1
             shopnumlist[num].append(shopusercount)
        num=num+1
     return dayinlist,shoplist,shopnumlist
def linenewuser():
     selectsql='''
  SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"2016-11-01"
 AND a.`pay_type`=3
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"2016-11-01"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[4]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopnamelist=[t[1]for t in alldata]
     shoplist=set(shopnamelist)
     shoplist=list(shoplist)


     num=0
     shopnumlist=[]
     for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopusercount=0
             for idata in alldata:
                 if  idata[4]==iday:
                     if idata[1]==ishop:
                         shopusercount=shopusercount+1
             shopnumlist[num].append(shopusercount)
        num=num+1
     return dayinlist,shoplist,shopnumlist
def benefitalldata():
     selectsql='''
    SELECT DISTINCT
SUM(a.`discount_total`),SUM(a.`activity_benefit_amount`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>"2016-11-01 "
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d') '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[2]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     discountlist=[]
     activilist=[]
     totallist=[]

     for iday in dayinlist:
         benefittotal=0
         discocount=0
         activicount=0
         for idata in alldata:
                  if idata[2]==iday:
                     disdata=idata[0]
                     actividata=idata[1]
                     if disdata==None:
                         disdata=0
                     if actividata==None:
                         actividata=0

                     disdata=float(disdata)

                     actividata=float(actividata)
                     benefittotal=disdata+actividata+benefittotal
                     discocount=disdata+discocount
                     activicount=actividata+activicount
         totallist.append(benefittotal)
         discountlist.append(discocount)
         activilist.append(activicount)
     return dayinlist,discountlist,activilist,totallist
def shopdiscount():
     selectsql='''
    SELECT DISTINCT
c.`shop_name`,SUM(a.`discount_total`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>"2016-11-01 "
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY c.`shop_name`,DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
    '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[2]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopnamelist=[t[0]for t in alldata]
     shoplist=set(shopnamelist)
     shoplist=list(shoplist)


     num=0
     shopnumlist=[]
     for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopusercount=0
             for idata in alldata:
                 if  idata[2]==iday:
                     if idata[0]==ishop:
                         shopdisc=idata[1]
                         if shopdisc==None:
                             shopdisc=0
                         shopusercount=shopusercount+shopdisc
             shopnumlist[num].append(shopusercount)
        num=num+1
     return dayinlist,shoplist,shopnumlist
def shopactivity():
     selectsql='''
    SELECT DISTINCT
c.`shop_name`,SUM(a.`activity_benefit_amount`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>"2016-11-01 "
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14721933954264944406","14629620426739375504")
GROUP BY c.`shop_name`,DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
    '''
     alldata=dbsql(selectsql)#原始流水数据
     daylist=[t[2]for t in alldata]
     dayinlist=set(daylist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     shopnamelist=[t[0]for t in alldata]
     shoplist=set(shopnamelist)
     shoplist=list(shoplist)


     num=0
     shopnumlist=[]
     for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopusercount=0
             for idata in alldata:
                 if  idata[2]==iday:
                     if idata[0]==ishop:
                         shopdisc=idata[1]
                         if shopdisc==None:
                             shopdisc=0
                         shopusercount=shopusercount+shopdisc
             shopnumlist[num].append(shopusercount)
        num=num+1
     return dayinlist,shoplist,shopnumlist







def datahtmlstr(list):#html数据列表字符串处理
    str_list = ""
    for i in list:
       try:
           i + 1
       except TypeError:
            str_list =str_list+ "'"+ str(i)+ "'"+","
       else:
           str_list = str_list+str(i)+ ","
    str_list = "[" + str_list + "]"
    return str_list


def incomehtml_str():#html拼接
    #list1 = ["周一", "周二", "周三", "周四", "周五", "周六"]

    #list2 = [5, 20, 36, 10, 10, 20]
    #list3=[6, 7, 30, 40, 50, 54]
    list1,list2,list3,list4,list5,listintotal=incomedata()#流水
    list4=list(list4)
    shoptrend_str=""
    shopi=0
    #---------站点流水html格式拼接-----------------
    for incomelist_i in list5:
         shopname="'"+str(list4[shopi])+"'"

         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(incomelist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if shoptrend_str=="":
             shoptrend_str=list_str
         else:
            shoptrend_str=shoptrend_str+list_str
         shopi=shopi+1
    return list1,list2,list3,list4 ,listintotal,shoptrend_str


def application(environ, start_response):#html
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '''
   <!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">

  <title>测试</title>
<style type="text/css">
    body {
	font-family: Cambria, Arial;
	background: #333;
}

	.tabs {
		width: 100%;
		 height:100%;
		max-width: 100%;
		max-height: 500px;
		margin: 50px auto;
	}

		input {
			opacity: 0;
		}

		label {
			cursor: pointer;
			background: -webkit-linear-gradient(#666, #555);
			color: #eee;
			border-radius: 5px 5px 0 0;
			padding: 1.5% 3%;
			float: left;
			margin-right: 2px;
			font: italic 1em cambria;
		}

			label:hover {
				background: -webkit-linear-gradient(#777, #666);
			}

			input:checked + label {
				background: #fff;
				color: #333;
			}

		.tabs input:nth-of-type(1):checked ~ .panels .panel:first-child,
		.tabs input:nth-of-type(2):checked ~ .panels .panel:nth-child(2),
		.tabs input:nth-of-type(3):checked ~ .panels .panel:nth-child(3),
		.tabs input:nth-of-type(4):checked ~ .panels .panel:last-child {
			opacity: 1;
			-webkit-transition: .3s;
		}

		.panels {
			float: left;
			clear: both;
			position: relative;
			width: 100%;
			background: #fff;
			border-radius: 0 10px 10px 10px;
			min-height: 1500px;
		}

			.panel {
				width: 100%;
				opacity: 0;
				position: absolute;
				background: #fff;
				border-radius: 0 10px 10px 10px;
				padding: 4%;
				box-sizing: border-box;
			}

				.panel h2 {
					margin: 0;
					font-family: Arial;
				}
				</style>
   <script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.8.0.js"></script>
    <script src="http://echarts.baidu.com/dist/echarts.js"></script>
	<script type="text/javascript">
$(document).ready(function(){
     $("#one").click(function(){
    $("div.panel").html("<div></div> <p>This is Panel one</p>");
});
   $("#two").click(function(){
    $("div.panel").html("This is Panel two");


  });
   $("#three").click(function(){
    $("div.panel").html("This is Panel Three");


  });
   $("#four").click(function(){
    $("div.panel").html("This is Panel four");


  });
});
</script>
</head>

<body>
<div style="text-align:center;clear:both;">
</div>
  <article class="tabs">

		<input checked id="one" name="tabs" type="radio">
	    <label for="one">流水</label>

	    <input id="two" name="tabs" type="radio" value="Two">
	    <label for="two">销量</label>

	    <input id="three" name="tabs" type="radio">
	    <label for="three">用户</label>

	    <input id="four" name="tabs" type="radio">
	    <label for="four">优惠</label>

	    <div class="panels">

		    <div class="panel" style="opacity:100">
<!--------第一个渠道流水趋势图------------------------------------------------------------------------->
  <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '渠道流水趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['线上','线下','合计']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : true,
            data : ''' + datahtmlstr(incomehtml_str()[0]) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 元'
            }

        }
    ],
    series : [
        {
            name:'线上',
            type:'bar',
            data:''' + datahtmlstr(incomehtml_str()[1]) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,
                                   position: 'top',
                                },
                                labelLine :{show:true}
                            }
                        } ,
        },
        {
            name:'线下',
            type:'bar',
            data:''' + datahtmlstr(incomehtml_str()[2]) + ''',

           itemStyle:{
                            normal:{
                                label:{
                                   show: true,
                                   position: 'top',
                                },
                                labelLine :{show:true}
                            }
                        } ,

        },
                {
            name:'合计',
            type:'line',

            data:''' + datahtmlstr(incomehtml_str()[4]) + ''',

           itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,

        }
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
    <!--------第二个站点流水趋势图------------------------------------------------------------------------->
   <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main1" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main1'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点流水趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(incomehtml_str()[3])+'''
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ''' + datahtmlstr(incomehtml_str()[0]) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 元'
            }
        }
    ],
    series : ['''+str(incomehtml_str()[5])+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>




		    </div>


		</div>

    </article>

</body>

</html>
    '''
    return [body.encode('utf-8')]
