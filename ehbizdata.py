# -*- coding: utf-8 -*-
__author__ = 'vincent'
import mysql.connector
import operator


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

def incomedata(starttime,endtime):#流水类
    #渠道流水
    select_sql='''
          SELECT
    DATE_FORMAT(a.`pay_date`,'%Y-%m-%d'),c.`shop_name`,a.`pay_type`,SUM(a.`pay_amount`)
    FROM
    `pay_info_record`a
    LEFT JOIN
    `tbl_order`b
    ON b.`order_no`=a.`order_no`
    LEFT JOIN
    `tbl_shop_info`c
    ON c.`shop_no`=b.`shop_no`
    WHERE
    a.`pay_date`>"{}"
    and a.`pay_date`<DATE_ADD("{}", INTERVAL 1 DAY)
    AND c.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
    AND c.`shop_name` IS NOT NULL
    AND a.`pay_status`="success"
    GROUP BY DATE_FORMAT(a.`pay_date`,'%Y-%m-%d'),c.`shop_name`,a.`pay_type`
        '''.format(starttime,endtime)
    allincomedata=dbsql(select_sql)#原始流水数据
    dayincomelist=[t[0]for t in allincomedata]
    dayinlist=set(dayincomelist)
    dayinlist=list(dayinlist)
    dayinlist.sort()#日期列表
#--------------------------渠道流水趋势--------------------------------------------------------------------------------
    #channelincomelist=[t[3]for t in allincomedata]
    #channlist=set(channelincomelist)#渠道列表
    onlineincom_list=[]
    lineincom_list=[]
    dayintal_list=[]
    for  iday in dayinlist:
        dayintotal=0
        onlinechannincom=0
        linechannincom=0
        for idata in allincomedata:
                if idata[0]==iday:
                   dayintotal=dayintotal+idata[3]
                   dayintotal=round(dayintotal)
                   if idata[2]==1:
                        onlinechannincom=onlinechannincom+idata[3]
                        onlinechannincom=round(onlinechannincom,2)
                   elif idata[2]==3:
                        linechannincom=linechannincom+idata[3]
                        linechannincom=round(linechannincom,2)
        dayintal_list.append(dayintotal)
        onlineincom_list.append(onlinechannincom)
        lineincom_list.append(linechannincom)

#--------------------------站点流水趋势--------------------------------------------------------------------------------
    shopincomelist=[t[1]for t in allincomedata]
    shoplist=set(shopincomelist)
    shoplist=list(shoplist)


    num=0
    shopnumlist=[]
    for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopincome=0
             for idata in allincomedata:
                 if  idata[0]==iday:
                     if idata[1]==ishop:
                         shopincome=shopincome+idata[3]
                         shopincome=round(shopincome,2)
             shopnumlist[num].append(shopincome)
        num=num+1

    return dayinlist ,onlineincom_list,lineincom_list,shoplist,shopnumlist,dayintal_list

def powerincomedata(starttime,endtime):#流水类
    #渠道流水
    select_sql='''
          SELECT
    DATE_FORMAT(a.`pay_date`,'%Y-%m-%d'),c.`shop_name`,a.`pay_type`,SUM(a.`pay_amount`)
    FROM
    `pay_info_record`a
    LEFT JOIN
    `tbl_order`b
    ON b.`order_no`=a.`order_no`
    LEFT JOIN
    `tbl_shop_info`c
    ON c.`shop_no`=b.`shop_no`
    WHERE
    a.`pay_date`>"{}"
    and a.`pay_date`<DATE_ADD("{}", INTERVAL 1 DAY)
    AND c.`shop_no`IN("14803348590903554653","14836694012369535164","14937902738181683764","14938834358936096746","14937905385175861793","14937781453413755100","14950180711887532177","14951593512010506079")
    AND c.`shop_name` IS NOT NULL
    AND a.`pay_status`="success"
    GROUP BY DATE_FORMAT(a.`pay_date`,'%Y-%m-%d'),c.`shop_name`,a.`pay_type`
        '''.format(starttime,endtime)
    allincomedata=dbsql(select_sql)#原始流水数据
    dayincomelist=[t[0]for t in allincomedata]
    dayinlist=set(dayincomelist)
    dayinlist=list(dayinlist)
    dayinlist.sort()#日期列表


#--------------------------站点流水趋势--------------------------------------------------------------------------------
    shopincomelist=[t[1]for t in allincomedata]
    shoplist=set(shopincomelist)
    shoplist=list(shoplist)


    num=0
    shopnumlist=[]
    for ishop in shoplist:
        shopnumlist.append([])
        for iday in dayinlist:
             shopincome=0
             for idata in allincomedata:
                 if  idata[0]==iday:
                     if idata[1]==ishop:
                         shopincome=shopincome+idata[3]
                         shopincome=round(shopincome,2)
             shopnumlist[num].append(shopincome)
        num=num+1
    shopinlunchlist=[]
    for iday in dayinlist:
                shopintotallunch=0
                for idata in allincomedata:
                     if  idata[0]==iday:
                         shopintotallunch=shopintotallunch+int(idata[3])
                shopinlunchlist.append(shopintotallunch)
    shoplist.append("合计")
    shopnumlist.append((shopinlunchlist))
    return dayinlist ,shoplist,shopnumlist


def  ftaccountpro(starttime,endtime):#金融品类占比
     selectsql='''SELECT
c.`cat_name`,ROUND(SUM(a.`price`*a.`quantity`),2),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
d.`basic_state`!=1
AND a.`shop_no`="14622779991551986272"
AND d.`payment_time`>"{}"
and d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),c.`cat_name`
 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist
def tecaccountpro(starttime,endtime):#大堂品类
     selectsql='''SELECT
c.`cat_name`,ROUND(SUM(a.`price`*a.`quantity`),2),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
d.`basic_state`!=1
AND a.`shop_no`="14477417463124576784"
AND d.`payment_time`>"{}"
and d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),c.`cat_name`
 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist



def lunchdata(starttime,endtime):#午餐类
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
 a.`payment_time`>"{}"
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`basic_state`!=1
AND e.`cat_name`="盒饭"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),c.`shop_name`
     '''.format(starttime,endtime)
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
     shoplist.append("合计")
     shopnumlist.append((shopinlunchlist))
     return dayinlist ,shoplist,shopnumlist

def suppliersaledata(starttime,endtime):#午餐供应商
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
 a.`payment_time`>"{}"
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`basic_state`!=1
AND e.`cat_name`="盒饭"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),e.`supplier_name` '''.format(starttime,endtime)

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
def shopwastagedata(starttime,endtime):#损耗
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
and d.`supplier_name`not like"%金兴%"
and d.`supplier_name`not like"%网购%"
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
AND a.`create_time`>"{}"
AND a.`create_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
'''.format(starttime,endtime)
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

def ftbreakfastdata(starttime,endtime):#金融早餐
     selectsql='''
SELECT
a.`prod_name`,SUM(a.`quantity`),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_commodity_category_group`e
ON c.`commo_no`=e.`commo_no`
LEFT JOIN
`tbl_commodity_category`f
ON f.`id`=e.`cate_id`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
f.name="早餐"
AND
d.`basic_state`!=1
AND f.`shop_no`="14477417463124576784"
AND d.`shop_no`="14622779991551986272"
AND d.`payment_time`>"{}"
AND d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),a.`prod_name`

 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist
def tecbreakfastdata(starttime,endtime):#大堂-早餐
     selectsql='''SELECT
a.`prod_name`,SUM(a.`quantity`),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_commodity_category_group`e
ON c.`commo_no`=e.`commo_no`
LEFT JOIN
`tbl_commodity_category`f
ON f.`id`=e.`cate_id`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
f.`name`="早餐"
AND
d.`basic_state`!=1
AND f.`shop_no`="14477417463124576784"
AND d.`shop_no`="14477417463124576784"
AND d.`payment_time`>"{}"
and  d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),a.`prod_name`

 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist

def catesaledata(starttime,endtime):#品类
     selectsql='''SELECT
c.`cat_name`,SUM(a.`quantity`),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
c.`cat_name`!="盒饭"
AND
d.`basic_state`!=1
AND a.`shop_no`="14622779991551986272"
AND d.`payment_time`>"{}"
AND d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),c.`cat_name`
 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist
def teccatesaledata(starttime,endtime):#品类
     selectsql='''SELECT
c.`cat_name`,SUM(a.`quantity`),DATE_FORMAT(d.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order_item`a
LEFT JOIN
`tbl_model`b
ON a.`prod_no`=b.`model_no`
LEFT JOIN
`tbl_commodity`c
ON c.`commo_no`=b.`commo_no`
LEFT JOIN
`tbl_order`d
ON d.`order_no`=a.`order_no`
WHERE
c.`cat_name`!="盒饭"
AND
d.`basic_state`!=1
AND a.`shop_no`="14477417463124576784"
AND d.`payment_time`>"{}"
AND d.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
GROUP BY DATE_FORMAT(d.`payment_time`,'%Y-%m-%d'),c.`cat_name`
 '''.format(starttime,endtime)

     allincomedata=dbsql(selectsql)#原始流水数据
     dayincomelist=[t[2]for t in allincomedata]
     dayinlist=set(dayincomelist)
     dayinlist=list(dayinlist)
     dayinlist.sort()#日期列表
     catenamelist=[t[0]for t in allincomedata]
     catenamelist=set(catenamelist)
     catenamelist=list(catenamelist)


     num=0
     catnumlist=[]
     for isup in catenamelist:
            catnumlist.append([])
            for iday in dayinlist:
                 catsale=0
                 for idata in allincomedata:
                     if  idata[2]==iday:
                         if idata[0]==isup:
                             catsale=catsale+idata[1]
                             catsale=int(catsale)
                 catnumlist[num].append((catsale))
            num=num+1

     return dayinlist ,catenamelist,catnumlist

def userdata(starttime,endtime):
     selectsql='''
    SELECT
DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),a.`pay_type`,COUNT(DISTINCT a.`buyer_no`)
FROM
`tbl_order` a
LEFT JOIN
`tbl_shop_info`b
ON b.`shop_no`=a.`shop_no`
WHERE
a.`payment_time`>"{}"
and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),a.`pay_type`
    '''.format(starttime,endtime)#渠道用户趋势
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

def onlineshopuserdata(starttime,endtime):
     selectsql='''
    SELECT
DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`,COUNT(a.`buyer_no`)
FROM
`tbl_order` a
LEFT JOIN
`tbl_shop_info`b
ON b.`shop_no`=a.`shop_no`
WHERE
a.`payment_time`>"{}"
and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
AND a.`pay_type`=1
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`
    '''.format(starttime,endtime)
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

def lineshopuserdata(starttime,endtime):
     selectsql='''
    SELECT
DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`,COUNT(a.`buyer_no`)
FROM
`tbl_order` a
LEFT JOIN
`tbl_shop_info`b
ON b.`shop_no`=a.`shop_no`
WHERE
a.`payment_time`>"{}"
and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
AND a.`pay_type`=3
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'),b.`shop_name`
    '''.format(starttime,endtime)
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

def newusertype(starttime,endtime):
     selectsql='''
    SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"{}"
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"{}"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''.format(starttime,endtime,starttime)#渠道新用户趋势
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

def onlinenewuser(starttime,endtime):
     selectsql='''
  SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"{}"
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
 AND a.`pay_type`=1
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"{}"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''.format(starttime,endtime,starttime)
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
def linenewuser(starttime,endtime):
     selectsql='''
  SELECT
 a.`buyer_no`,c.`shop_name`,a.`pay_type`,COUNT(a.`buyer_no`),MIN(DATE_FORMAT(a.`payment_time`,'%Y-%m-%d'))
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"{}"
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
 AND a.`pay_type`=3
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
 AND a.`buyer_no`NOT IN (SELECT
 a.`buyer_no`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`<"{}"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750"))
 GROUP BY a.`buyer_no`
 ORDER BY COUNT(a.`buyer_no`)DESC
    '''.format(starttime,endtime,starttime)
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
def benefitalldata(starttime,endtime):
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
 a.`payment_time`>"{} "
 and  a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY DATE_FORMAT(a.`payment_time`,'%Y-%m-%d') '''.format(starttime,endtime)
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
def shopdiscount(starttime,endtime):
     selectsql='''
    SELECT DISTINCT
c.`shop_name`,COUNT(a.`order_no`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>"{} "
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
  AND a.`discount_total`!=""
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY c.`shop_name`,DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
    '''.format(starttime,endtime)
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
             shopnumlist[num].append(float(shopusercount))
        num=num+1
     return dayinlist,shoplist,shopnumlist
def shopactivity(starttime,endtime):
     selectsql='''
    SELECT DISTINCT
c.`shop_name`,COUNT(a.`order_no`),DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
FROM
`tbl_order`a
LEFT JOIN `tbl_shop_info`c
ON a.`shop_no`=c.`shop_no`
LEFT JOIN `tbl_order_activity_contact`f
ON a.`order_no`=f.`order_no`
LEFT JOIN `tbl_activity`g
ON g.activity_no=f.activity_no
WHERE
 a.`payment_time`>"{} "
 and a.`payment_time`<=DATE_ADD("{}", INTERVAL 1 DAY)
 AND a.`activity_benefit_amount`!=""
AND a.`basic_state`!=1
AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
GROUP BY c.`shop_name`,DATE_FORMAT(a.`payment_time`,'%Y-%m-%d')
    '''.format(starttime,endtime)
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
             shopnumlist[num].append(float(shopusercount))
        num=num+1
     return dayinlist,shoplist,shopnumlist

def lossuser():
    selectsql='''
    SELECT
 c.`shop_name`,a.`buyer_nick_name`,a.`buyer_phone`,COUNT(a.`buyer_no`),SUM(a.`paid_total`),AVG(a.`paid_total`), MAX(a.`paid_total`)
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>"2016-06-01"
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
#a.`shop_no`里边可以换成你想要看的站点的店铺编号
 AND a.`pay_type`=1
 AND a.`buyer_phone`
 AND a.`buyer_phone`NOT IN(
 SELECT
a.`buyer_phone`
 FROM
 `tbl_order`a
 LEFT JOIN
 `tbl_shop_info`c
 ON c.`shop_no`=a.`shop_no`
 WHERE
 a.`payment_time`>DATE_SUB(CURDATE(), INTERVAL 3 WEEK)
 AND a.`shop_no`IN("14622779991551986272","14477417463124576784","14667588471072254231","14923963824806752750")
 AND a.`pay_type`=1)
 GROUP BY  c.`shop_name`,a.`buyer_no`

    '''
    alldata=dbsql(selectsql)#原始流水数据
    lossuserli=[]
    for idata in alldata:
        if idata[3]>10:
            if idata[5]>10:
                datacount=int(idata[3])
                dataamount=round(idata[4],1)
                dataavg=round(idata[5],1)
                datamax=round(idata[6],1)
                idatali=[idata[0],idata[1],idata[2],datacount,dataamount,dataavg,datamax]
                lossuserli.append(idatali)
    lossuserli.sort(key=operator.itemgetter(3,4),reverse=True)
    return lossuserli
if __name__ == '__main__':
    #list1,list2,list3,list4,list5,list6=incomedata()
    #print(list1,'\n',list2,'\n',list3,'\n',list4,'\n',list5,'\n',list6)
    list1=lossuser()
    print(list1)