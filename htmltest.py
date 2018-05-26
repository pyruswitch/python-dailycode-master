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


def application(environ, start_response):#html拼接
    #list1 = ["周一", "周二", "周三", "周四", "周五", "周六"]

    #list2 = [5, 20, 36, 10, 10, 20]
    #list3=[6, 7, 30, 40, 50, 54]
    list1,list2,list3,list4,list5,listintotal=incomedata()#流水
    list6,list7,list8,shopinlunchlist=lunchsaledata()#午餐站点
    list7.append("合计")
    list9,list10,list11=suppliersaledata()#午餐供应商
    list12,list13,list14=shopwastagedata()#损耗
    list15,list16,list17,list18=userdata()#总用户
    list19,list20,list21=shopuserdata()#站点用户
    list22,list23,list24,list25=newusertype()#新用户
    list26,list27,list28=onlinenewuser()#线上站点新用户
    list29,list30,list31=linenewuser()#线下站点新用户
    list32,list33,list34,list35=benefitalldata()#优惠数据
    list36,list37,list38=shopdiscount()#站点优惠券数据
    list39,list40,list41=shopactivity()#站点活动优惠
    list42,list43,list44,list45=lunchpercentdata()#午餐流水占比
    list43.append("合计")
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
    #---------站点午餐html格式拼接-----------------
    lunchshop_str=""
    lunchshopi=0
    for lunchsalelist_i in  list8:
         shopname="'"+str(list7[lunchshopi])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'bar',
            data:''' + datahtmlstr(lunchsalelist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,
                                   position: 'top',
                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if lunchshop_str=="":
             lunchshop_str=list_str
         else:
            lunchshop_str=lunchshop_str+list_str
         lunchshopi=lunchshopi+1
        #---------站点午餐占比html格式拼接-----------------
    lunchpercentshop_str=""
    lunchshopi=0
    for lunchsalelist_i in  list44:
         shopname="'"+str(list43[lunchshopi])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'bar',
            data:''' + datahtmlstr(lunchsalelist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,
                                   position: 'top',
                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if lunchpercentshop_str=="":
             lunchpercentshop_str=list_str
         else:
            lunchpercentshop_str=lunchpercentshop_str+list_str
         lunchshopi=lunchshopi+1
 #---------供应商午餐html格式拼接-----------------
    lunchsup_str=""
    lunchsupi=0
    for lunchsupsalelist_i in  list11:
         supname="'"+str(list10[lunchsupi])+"'"
         list_str='''{
            name:'''+supname+''',
            type:'line',
            data:''' + datahtmlstr(lunchsupsalelist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if lunchsup_str=="":
             lunchsup_str=list_str
         else:
            lunchsup_str=lunchsup_str+list_str
         lunchsupi=lunchsupi+1
    #---------供应商损耗html格式拼接-----------------
    lunchwas_str=""
    lunchwasi=0
    for lunchwassalelist_i in  list14:
         supname="'"+str(list13[lunchwasi])+"'"
         list_str='''{
            name:'''+supname+''',
            type:'line',
            data:''' + datahtmlstr(lunchwassalelist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if lunchwas_str=="":
             lunchwas_str=list_str
         else:
            lunchwas_str=lunchwas_str+list_str
         lunchwasi=lunchwasi+1
    #---------站点用户html格式拼接-----------------
    shopuser_str=""
    shopui=0
    for shopuserlist_i in  list21:
         shopname="'"+str(list20[shopui])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(shopuserlist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if shopuser_str=="":
             shopuser_str=list_str
         else:
            shopuser_str=shopuser_str+list_str
         shopui=shopui+1
    #---------线上站点新用户html格式拼接-----------------
    shopnewuser_str=""
    shopnui=0
    for shopnewuserlist_i in  list28:
         shopname="'"+str(list27[shopnui])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(shopnewuserlist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if shopnewuser_str=="":
             shopnewuser_str=list_str
         else:
            shopnewuser_str=shopnewuser_str+list_str
         shopnui=shopnui+1
    #---------线下站点新用户html格式拼接-----------------
    lineshopnewuser_str=""
    shopnui=0
    for lineshopnewuserlist_i in  list31:
         shopname="'"+str(list30[shopnui])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(lineshopnewuserlist_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if lineshopnewuser_str=="":
             lineshopnewuser_str=list_str
         else:
            lineshopnewuser_str=lineshopnewuser_str+list_str
         shopnui=shopnui+1
    #---------站点优惠券html格式拼接-----------------
    shopdiscount_str=""
    shopnui=0
    for shopdiscount_i in  list38:
         shopname="'"+str(list37[shopnui])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(shopdiscount_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if shopdiscount_str=="":
             shopdiscount_str=list_str
         else:
            shopdiscount_str=shopdiscount_str+list_str
         shopnui=shopnui+1
    #---------站点活动优惠html格式拼接-----------------
    shopactivity_str=""
    shopnui=0
    for shopdiscount_i in  list41:
         shopname="'"+str(list40[shopnui])+"'"
         list_str='''{
            name:'''+shopname+''',
            type:'line',
            data:''' + datahtmlstr(shopdiscount_i) + ''',
            itemStyle:{
                            normal:{
                                label:{
                                   show: true,

                                },
                                labelLine :{show:true}
                            }
                        } ,
        },'''
         if shopactivity_str=="":
             shopactivity_str=list_str
         else:
            shopactivity_str=shopactivity_str+list_str
         shopnui=shopnui+1





    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '''<html>
<head>
<meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="http://echarts.baidu.com/dist/echarts.js"></script>
<style type="text/css">

h1 {background-color: 	#C0C0C0}

</style>

</head>

<body>

<h1>小站日常数据监控</h1>
<h2>☞流水趋势</h2>
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
            data : ''' + datahtmlstr(list1) + '''
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
            data:''' + datahtmlstr(list2) + ''',
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
            data:''' + datahtmlstr(list3) + ''',

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

            data:''' + datahtmlstr(listintotal) + ''',

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
        data:'''+datahtmlstr(list4)+'''
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
            data : ''' + datahtmlstr(list1) + '''
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
    series : ['''+str(shoptrend_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<!--------第三个午餐销量趋势图------------------------------------------------------------------------->
<h2>☞午餐趋势<h2/>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main2" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main2'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点午餐趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list7)+'''
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
            data : ''' + datahtmlstr(list6) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 份'
            }
        }
    ],
    series : ['''+str(lunchshop_str)+ '''

    {
            name:'合计',
            type:'line',

            data:''' + datahtmlstr(shopinlunchlist) + ''',

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
<!--------第14个站点午餐流水占比趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main13" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main13'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点午餐流水占比'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list43)+'''
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
            data : ''' + datahtmlstr(list42) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} '
            }
        }
    ],
    series : [

    {
            name:'合计',
            type:'line',

            data:''' + datahtmlstr(list45) + ''',

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
<!--------第四个供应商午餐销量趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main3" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main3'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '供应商午餐趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list10)+'''
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
            data : ''' + datahtmlstr(list9) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 份'
            }
        }
    ],
    series : ['''+str(lunchsup_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<!--------第五个供应商损耗趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main4" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main4'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '供应商损耗趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list13)+'''
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
            data : ''' + datahtmlstr(list12) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 份'
            }
        }
    ],
    series : ['''+str(lunchwas_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>

<h2>☞用户趋势<h2/>
<!--------第六个渠道用户趋势图------------------------------------------------------------------------->
  <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main5" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main5'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '渠道用户趋势'
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
            data : ''' + datahtmlstr(list15) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 人'
            }

        }
    ],
    series : [
        {
            name:'线上',
            type:'bar',
            data:''' + datahtmlstr(list17) + ''',
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
            data:''' + datahtmlstr(list18) + ''',

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

            data:''' + datahtmlstr(list16) + ''',

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
<!--------第7个站点用户趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main6" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main6'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点用户趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list20)+'''
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
            data : ''' + datahtmlstr(list19) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 人'
            }
        }
    ],
    series : ['''+str(shopuser_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<!--------第8个渠道用户趋势图------------------------------------------------------------------------->
  <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main7" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main7'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '新用户趋势'
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
            data : ''' + datahtmlstr(list22) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 人'
            }

        }
    ],
    series : [
        {
            name:'线上',
            type:'bar',
            data:''' + datahtmlstr(list24) + ''',
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
            data:''' + datahtmlstr(list25) + ''',

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

            data:''' + datahtmlstr(list23) + ''',

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
<!--------第9个线上站点新用户趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main8" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main8'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点线上新用户趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list27)+'''
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
            data : ''' + datahtmlstr(list26) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 人'
            }
        }
    ],
    series : ['''+str(shopnewuser_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<!--------第10个线下站点新用户趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main9" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main9'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '站点线下新用户趋势'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list30)+'''
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
            data : ''' + datahtmlstr(list29) + '''
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} 人'
            }
        }
    ],
    series : ['''+str(lineshopnewuser_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<h2>☞优惠情况<h2/>
<!--------第11个优惠情况图------------------------------------------------------------------------->
  <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main10" style="width: 1500px;height:500px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main10'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '每日优惠情况'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['优惠券','平台活动','合计']
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
            data : ''' + datahtmlstr(list32) + '''
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
            name:'优惠券',
            type:'bar',
            data:''' + datahtmlstr(list33) + ''',
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
            name:'平台活动',
            type:'bar',
            data:''' + datahtmlstr(list34) + ''',

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

            data:''' + datahtmlstr(list35) + ''',

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
    <!--------第12个线下站点新用户趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main11" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main11'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '各站点优惠券使用情况'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list37)+'''
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
            data : ''' + datahtmlstr(list36) + '''
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
    series : ['''+str(shopdiscount_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
        <!--------第13个线下站点新用户趋势图------------------------------------------------------------------------->
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <div id="main12" style="width: 1500px;height:600px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main12'));

        // 指定图表的配置项和数据
        var option = {
            title : {
        text: '各站点平台活动参与情况'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:'''+datahtmlstr(list40)+'''
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
            data : ''' + datahtmlstr(list39) + '''
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
    series : ['''+str(shopactivity_str)+ '''
    ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
<h3>更多数据敬请期待…………</h3>




</body>
</html>'''
    return [body.encode('utf-8')]
