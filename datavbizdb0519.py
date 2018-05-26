__author__ = 'vincent'
import mysql.connector
import operator
import collections
import  datetime
import time
import random
from decimal import *

def dbsql (selectsql,account):#数据库查询

    user=account["user"]
    pwd=account["pwd"]
    host=account["host"]
    db=account["db"]
    port=account["port"]

    cnx=mysql.connector.connect(user=user,password=pwd,database=db,host=host,port=port)
    cursor=cnx.cursor()
    select_sql=selectsql

    cursor.execute(select_sql)
    alldata=cursor.fetchall()
    #alldata.sort(key=operator.itemgetter(0))
    return alldata

def substr(mainstr, startstr, endstr):
    try:
        start_index = mainstr.index(startstr) + len(startstr)
        try:
            end_index = mainstr.index(endstr, start_index + 1)
            return mainstr[start_index:end_index]
        except:
            return mainstr[start_index:]
    except:
        try:
            return mainstr[0:mainstr.index(endstr)]
        except:
            return mainstr



def parkorder(ns):#订单列表
    select_sql='''
    SELECT
DATE_FORMAT(a.`pay_date`,'%m-%d %H:%I'),b.`buyer_nick_name`,a.`order_no`,a.`order_type`,a.`pay_amount`,a.`online_pay_style_no`
FROM
`pay_info_record`a
LEFT JOIN
`tbl_order`b
ON a.`order_no`=b.`order_no`
LEFT JOIN
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
c.namespace_id={}

ORDER BY a.`pay_date` DESC
LIMIT 100
        '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    typedict={"dianshang":"电商","parking":"停车缴费","activitySignupOrder":"活动报名","rentalOrder":"资源预定"}
    allorderdata=dbsql(select_sql,account)#原始支付订单数据
    allorderdata.sort(key=operator.itemgetter(0),reverse=True)
    allorderdata=list(allorderdata)
    orderdict={}
    orderlist=[]
    dicti=1
    if allorderdata==[]:
        orderdict[dicti]={}
        orderdict[dicti]["paydate"]=0
        orderdict[dicti]["name"]=0
        orderdict[dicti]["ordertype"]=0
        orderdict[dicti]["payamount"]=0
        orderdict[dicti]["paychannel"]=0
        orderlist.append(orderdict[dicti])
    else:
        for ordervalue in allorderdata:
            orderdict[dicti]={}
            orderdict[dicti]["paydate"]=ordervalue[0]
            orderdict[dicti]["name"]=ordervalue[1]
            orderdict[dicti]["ordertype"]=typedict[ordervalue[3]]
            orderdict[dicti]["payamount"]=ordervalue[4]
            orderdict[dicti]["paychannel"]=ordervalue[5]
            orderlist.append(orderdict[dicti])
            dicti=dicti+1
    return orderlist

def ordertypecount(ns):#按数量统计订单类型
    select_sql='''
        SELECT
a.`order_type`,COUNT(a.`order_type`)
FROM
`pay_info_record`a
LEFT JOIN
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
YEAR(a.`pay_date`)=YEAR(NOW())
AND c.namespace_id={}
GROUP BY a.`order_type`
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    ordertypecount=dbsql(select_sql,account)#订单类型数量
    ordertypecount=list(ordertypecount)
    ordertypedict={}
    ordertypelist=[]
    dicti=1
    namedict={"activitySignupOrder":"活动报名","dianshang":"电商","parking":"停车缴费"}

    for ordervalue in ordertypecount:
        ordertypedict[dicti]={}
        if str(ordervalue[0]) in namedict:
            ordertypedict[dicti]["name"]=namedict[ordervalue[0]]
            ordertypedict[dicti]["value"]=ordervalue[1]
            ordertypelist.append(ordertypedict[dicti])
            dicti=dicti+1
    return ordertypelist

def ordertypeamount(ns):#按数量统计订单类型
    select_sql='''
   SELECT
a.`order_type`,SUM(a.`pay_amount`)
FROM
`pay_info_record`a
LEFT JOIN
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
YEAR(a.`pay_date`)=YEAR(NOW())
AND c.namespace_id={}
GROUP BY a.`order_type`
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    ordertypeamount=dbsql(select_sql,account)#订单类型总额
    ordertypeamount=list(ordertypeamount)
    ordertypedict={}
    ordertypelist=[]
    dicti=1
    namedict={"activitySignupOrder":"活动报名","dianshang":"电商","parking":"停车缴费"}

    for ordervalue in ordertypeamount:
        ordertypedict[dicti]={}
        if ordervalue[0]in namedict:
            ordertypedict[dicti]["name"]=namedict[ordervalue[0]]
            ordertypedict[dicti]["value"]=ordervalue[1]
            ordertypelist.append(ordertypedict[dicti])
            dicti=dicti+1
    return ordertypelist

def orderchannelcount(ns):#按数量统计支付渠道
    select_sql='''
   SELECT
a.`online_pay_style_no`,COUNT(a.`online_pay_style_no`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-09-01"
AND a.`pay_date`<"2017-10-21"
AND c.namespace_id={}
GROUP BY a.`online_pay_style_no`
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    orderchannnelcount=dbsql(select_sql,account)#订单渠道数量
    channeldict={}
    if orderchannnelcount==[]:
        channeldict["male"]=0
        channeldict["female"]=0
    else:
        name=str(orderchannnelcount[0][0])
        channeldict[name]=orderchannnelcount[0][1]
        name=str(orderchannnelcount[1][0])
        channeldict[name]=orderchannnelcount[1][1]
    return channeldict
def orderchannelamount(ns):#按金额统计支付渠道
    select_sql='''
  SELECT
a.`online_pay_style_no`,SUM(a.`pay_amount`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-09-01"
AND a.`pay_date`<"2017-10-21"
AND c.namespace_id={}
GROUP BY a.`online_pay_style_no`
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    orderchannelamount=dbsql(select_sql,account)#订单渠道数量
    orderchannelamount=list(orderchannelamount)
    return orderchannelamount

def monthamount(ns):#按月份统计金额
    select_sql='''
 SELECT
DATE_FORMAT(a.`pay_date`,'%m'),SUM(a.`pay_amount`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-01-01"
AND c.namespace_id={}
GROUP BY DATE_FORMAT(a.`pay_date`,'%m')
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    monthamount=dbsql(select_sql,account)#订单渠道数量
    monthamount=list(monthamount)
    return monthamount

def monthcount(ns):#按月份统计单量
    select_sql='''
 SELECT
DATE_FORMAT(a.`pay_date`,'%m'),COUNT(a.`order_no`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-01-01"
AND c.namespace_id={}
GROUP BY DATE_FORMAT(a.`pay_date`,'%m')
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    monthcount=dbsql(select_sql,account)#订单渠道数量
    monthcount=list(monthcount)
    return monthcount

def orderamount(ns):#总金额
    select_sql='''
 SELECT
SUM(a.`pay_amount`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-01-01"
AND c.namespace_id={}
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    orderamount=dbsql(select_sql,account)#订单渠道数量
    a=orderamount[0][0]
    return a

def ordercount(ns):#总单量
    select_sql='''
SELECT
COUNT(a.`order_no`)
FROM
`pay_info_record`a
left join
`tbl_mall_contact`c
ON a.`realm`=c.realm
WHERE
a.`pay_date`>"2017-01-01"
AND c.namespace_id={}
    '''.format(ns)
    account={"user":"ning.wei15","pwd":"wn3333","host":"bizdb.zuolin.com","db":"ehbiz","port":"18306",}
    ordercount=dbsql(select_sql,account)#订单渠道数量
    a=ordercount[0][0]
    return a

def tasktypecount(ns):#任务类型分布
    select_sql='''
SELECT
title, COUNT(*) FROM eh_flow_cases
WHERE namespace_id = {}
AND title IS NOT NULL
GROUP BY title;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    tasktypecount=dbsql(select_sql,account)#任务类型数量
    tasktypecountli=list(tasktypecount)
    taskdict={}
    tasklist=[]
    dicti=1
    for taskvalue in tasktypecountli:
        taskdict[dicti]={}
        taskdict[dicti]["name"]=substr(taskvalue[0],':"','"')
        taskdict[dicti]["value"]=str((taskvalue[1]))
        tasklist.append(taskdict[dicti])
        dicti=dicti+1
    return tasklist

def boardvita(ns):#模块活跃度
    select_sql='''

SELECT
	param, SUM(total_count) AS total_count FROM eh_stat_event_statistics
WHERE
	namespace_id = {} AND event_name = 'launchpad_on_launch_pad_item_click' AND event_version = '1.0' AND time_interval = 'DAILY'
GROUP BY param;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    tasktypecount=dbsql(select_sql,account)
    taskdict={}
    tasklist=[]
    dicti=1
    for taskvalue in tasktypecount:
        taskdict[dicti]={}
        taskdict[dicti]["name"]=substr(taskvalue[0],':"','"')
        taskdict[dicti]["value"]=str((taskvalue[1]))
        tasklist.append(taskdict[dicti])
        dicti=dicti+1
    return tasklist

def taskclose(ns):#已完成任务
    select_sql='''
SELECT COUNT(*) FROM eh_flow_cases
WHERE namespace_id = {}
AND  YEAR(create_time)=YEAR(NOW());
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    taskamount=dbsql(select_sql,account)#任务总数
    select_sql='''
SELECT COUNT(*) FROM eh_flow_cases
WHERE namespace_id = {}
AND  YEAR(create_time)=YEAR(NOW())AND status IN (0, 3, 4);
    '''.format(ns)
    closetaskamount=dbsql(select_sql,account)#任务类型数量
    alltaskdict={}
    if closetaskamount==[]:
        alltaskdict["tasktotal"]=0
        #closetaskdict["name"]="已完成任务数"
        alltaskdict["closetasktotal"]= 0
    else:
        #closetaskdict={}
        #alltaskdict["name"]="总任务数"
        alltaskdict["tasktotal"]=taskamount[0][0]
        #closetaskdict["name"]="已完成任务数"
        alltaskdict["closetasktotal"]= closetaskamount[0][0]
        #taskdictlist=[alltaskdict,closetaskdict]
    return alltaskdict

def daytaskorder(ns):#每日任务数
    select_sql='''
SELECT
	DATE_FORMAT(CAST(create_time AS DATE) ,"%m")AS create_date, COUNT(*) FROM eh_flow_cases
WHERE namespace_id = 1000000 AND  YEAR(create_time)=YEAR(NOW())
GROUP BY create_date;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    taskamount=dbsql(select_sql,account)#每日任务数
    taskdict={}
    tasklist=[]
    dicti=1
    if taskamount==[]:
        taskdict[dicti]={}
        taskdict[dicti]["date"]=0
        taskdict[dicti]["value"]=0
        tasklist.append(taskdict[dicti])
    else:
        for taskvalue in taskamount:
            taskdict[dicti]={}
            taskdict[dicti]["date"]=str(taskvalue[0])
            taskdict[dicti]["value"]=taskvalue[1]
            tasklist.append(taskdict[dicti])
            dicti=dicti+1
    return tasklist


def tasktyperespon(ns):#任务类型平均响应时间
    select_sql='''
SELECT
	title, AVG(DATEDIFF(last_step_time, create_time)) FROM eh_flow_cases
WHERE namespace_id = {} AND   title IS NOT NULL AND STATUS IN (0, 3, 4)
GROUP BY title;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    taskrespone=dbsql(select_sql,account)#每日任务数
    taskdict={}
    tasklist=[]
    dicti=1
    for taskvalue in taskrespone:
        taskdict[dicti]={}
        taskdict[dicti]["name"]=str(taskvalue[0])
        taskdict[dicti]["value"]=str( round(taskvalue[1], 1))
        tasklist.append(taskdict[dicti])
        dicti=dicti+1
    return tasklist

def taskresponse(ns):#总平均响应时间

    select_sql='''
SELECT
	 AVG(DATEDIFF(last_step_time, create_time)) FROM eh_flow_cases
WHERE namespace_id = {} AND   title IS NOT NULL AND STATUS IN (0, 3, 4);
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    responsetime=dbsql(select_sql,account)#任务类型数量
    taskdict={}
    taskdict["name"]="总平均响应时间"
    taskdict["value"]=str( round(responsetime[0][0], 1))
    return taskdict

def pengdingtask(ns):#新代办任务
    select_sql='''
SELECT
	 title, content, DATE_FORMAT(create_time,'%y/%m/%d') FROM eh_flow_cases
WHERE namespace_id = {} AND STATUS = 2 AND title IS NOT NULL
ORDER BY create_time DESC
LIMIT 100;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    pengdingtask=dbsql(select_sql,account)#新代办任务
    taskdict={}
    tasklist=[]
    dicti=1
    for taskvalue in pengdingtask:
        taskdict[dicti]={}
        taskdict[dicti]["name"]=str(taskvalue[0])
        taskdict[dicti]["content"]=str(taskvalue[1])
        taskdict[dicti]["date"]=str(taskvalue[2])
        tasklist.append(taskdict[dicti])
        dicti=dicti+1
    return tasklist

def taskstatus(ns):#任务状态分布
    select_sql='''
SELECT
	title, STATUS, COUNT(*) FROM eh_flow_cases
WHERE namespace_id = {} AND title IS NOT NULL
GROUP BY title, STATUS;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    taskstatus=dbsql(select_sql,account)#新代办任务
    taskdict={}
    tasklist=[]
    dicti=1
    namedict={"1":"初始化","2":"处理中","3":"已完成","4":"已完成"}
    if taskstatus==[]:
            taskdict[dicti]={}
            taskdict[dicti]["name"]=0
            taskdict[dicti]["status"]=0
            taskdict[dicti]["value"]=0
            tasklist.append(taskdict[dicti])
    else:
        for taskvalue in taskstatus:
            if str(taskvalue[1]) in namedict:
                taskdict[dicti]={}
                taskdict[dicti]["name"]=str(taskvalue[0])
                taskdict[dicti]["status"]=namedict[str(taskvalue[1])]
                taskdict[dicti]["value"]=str(taskvalue[2])
                tasklist.append(taskdict[dicti])
                dicti=dicti+1
    return tasklist

def  totalassets(ns):#总资产
    select_sql='''
SELECT
SUM(`turnover`)
FROM `eh_customer_economic_indicators`
where namespace_id={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    totalassets=dbsql(select_sql,account)#总资产
    assetsdict={}
    assetsdict["name"]="总资产"
    assetsdict["value"]=str(totalassets[0][0])
    select_sql='''
SELECT
SUM(`total_tax_amount`)
FROM `eh_customer_economic_indicators`
where namespace_id={}
    '''.format(ns)
    totaltax=dbsql(select_sql,account)#总税收
    taxdict={}
    taxdict["name"]="总税收"
    taxdict["value"]=str(totaltax[0][0])
    select_sql='''
SELECT
SUM(`corp_employee_amount`)
FROM `eh_enterprise_customers`
where namespace_id={}
    '''.format(ns)
    totalpeople=dbsql(select_sql,account)#总人数
    peopledict={}
    peopledict["name"]="总人数"
    peopledict["value"]=str(totalpeople[0][0])
    dictlist=[assetsdict,taxdict,peopledict]
    return dictlist

def Companyespon(ns):#企业名册
    select_sql='''
SELECT  DISTINCT
 `eh_organizations`.name,`eh_addresses`.`address`,COUNT(`eh_organizations`.name)
 FROM
 eh_organizations
 LEFT JOIN
 `eh_organization_addresses`
 ON `eh_organization_addresses`.`organization_id`=`eh_organizations`.`id`
 LEFT JOIN
 `eh_addresses`
 ON
 `eh_addresses`.`id`=`eh_organization_addresses`.`address_id`
 WHERE
 `eh_organizations`.STATUS=2
 AND `eh_organizations`.parent_id=0
 AND `eh_organizations`.namespace_id={}
 GROUP BY `eh_organizations`.name
 LIMIT 100
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    companyespon=dbsql(select_sql,account)#企业名册
    companytype=[
"光机电",
"商业-其他",
"商业-超市",
"生物医药",
"软件",
"通信技术",
"集成电路"]
    companysize=["中型","大型","小型"]
    companydict={}
    companylist=[]
    dicti=1
    for value in companyespon:
        companydict[dicti]={}
        companydict[dicti]["name"]=str(value[0])
        name=companydict[dicti]["name"]
        if  "公司" in name:

            companydict[dicti]["type"]=random.sample(companytype,1)[0]
            companydict[dicti]["scale"]=random.sample(companysize,1)[0]
            companydict[dicti]["adress"]=str(value[1])
            companylist.append(companydict[dicti])
            dicti=dicti+1
    return companylist
def  settledenter(ns):#入驻企业
    select_sql='''
 SELECT
 COUNT(*)
 FROM
 eh_organizations
 WHERE
 STATUS=2
 AND parent_id=0
 AND namespace_id={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    settlecount=dbsql(select_sql,account)#总资产
    enterprisedict={}
    #settlecountdict["name"]="入驻企业数"
    enterprisedict["enterprisestotal"]=str(settlecount[0][0])
    select_sql='''
SELECT
   COUNT(DISTINCT(customer_id ))
 FROM
 `eh_contracts`
 WHERE
 YEAR(signed_time )=YEAR(NOW())and  namespace_id={}
    '''.format(ns)
    totalsign=dbsql(select_sql,account)#总税收

    #totalsigndict["name"]="今年签约数"
    enterprisedict["contract"]=str(totalsign[0][0])
    select_sql='''
SELECT
  COUNT(DISTINCT(customer_id) )
 FROM
 `eh_contracts`
 WHERE
 YEAR(contract_end_date)=YEAR(NOW()) and  namespace_id={}
    '''.format(ns)
    totalexpired=dbsql(select_sql,account)#总人数

    #expireddict["name"]="到期企业数"
    enterprisedict["expiration"]=str(totalexpired[0][0])

    return enterprisedict

def InviteBusiness(ns):#招商引资
    select_sql='''
SELECT
 COUNT(IF( level_item_id !=6 , id , NULL))AS "商务沟通", COUNT(IF( level_item_id =6 , id , NULL))AS "合同期"
 FROM
 eh_enterprise_customers
where namespace_id={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    inbus=dbsql(select_sql,account)#企业名册
    communidict={}
    bargaindict={}
    communidict["name"]="商务沟通"
    bargaindict["name"]="已成交"

    communidict["value"]=str(inbus[0][0])
    bargaindict["value"]=str(inbus[0][1])
    inbuslist=[communidict,bargaindict]
    return inbuslist

def Companytype(ns):#企业类型
    select_sql='''
SELECT
  b.`display_name`,COUNT(a.id)
 FROM
 `eh_enterprise_customers`a
 LEFT JOIN
`eh_var_field_items`b
 ON a.`corp_industry_item_id`=b.`id`
 WHERE
 b.`display_name`IS NOT NULL
 and a.namespace_id={}
 GROUP BY b.`display_name`

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    companytype=dbsql(select_sql,account)#企业类型
    companytypedict={}
    companytypelist=[]
    dicti=1
    for value in companytype:
        companytypedict[dicti]={}
        companytypedict[dicti]["name"]=str(value[0])
        companytypedict[dicti]["value"]=str(value[1])
        companytypelist.append(companytypedict[dicti])
        dicti=dicti+1
    return companytypelist

def occupancyrate(ns):#入住率
    select_sql='''
SELECT
a.`name`,((COUNT(IF(b.`living_status`=2,b.`address`,NULL)))/(COUNT(b.`address`)))AS "入住率"
FROM
`eh_buildings`a
LEFT JOIN
`eh_addresses`b
ON a.`name`=b.`building_name`
WHERE
a.`status`=2
AND a.`namespace_id`={}
GROUP BY a.`name`
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    occupancyrate=dbsql(select_sql,account)#入住率
    occupancyratedict={}
    occupancyratelist=[]
    dicti=1
    if occupancyrate==[]:
        occupancyratedict["name"]=0
        occupancyratedict["value"]=0
        occupancyratelist.append(occupancyratedict)
    else:
        for value in occupancyrate:
            occupancyratedict[dicti]={}
            occupancyratedict[dicti]["name"]=str(value[0])
            try:
               occupancyratedict[dicti]["value"]=str(round((value[1]*100),2))
            except Exception:
                occupancyratedict[dicti]["value"]=0
            occupancyratelist.append(occupancyratedict[dicti])
            dicti=dicti+1
    return occupancyratelist

def rentalamount(ns):#年租金收入

    select_sql='''
SELECT
SUM(`amount_received`)
FROM
 eh_payment_bills
 WHERE
 `bill_group_id`=1
 AND YEAR(`real_paid_time`)=YEAR(NOW())
 AND `namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    responsetime=dbsql(select_sql,account)#任务类型数量
    taskdict={}
    #taskdict["name"]="年租金收入"
    if str( responsetime[0][0])=="None":
        taskdict["yearrental"]=0
    else:
        taskdict["yearrental"]=str( round(responsetime[0][0], 2))
    select_leasedarea_sql='''
    SELECT
 ROUND(SUM(build_area),2)
 FROM
 eh_addresses
 WHERE
 living_status=2
 AND `namespace_id`={}
    '''.format(ns)
    leasedarea=dbsql(select_leasedarea_sql,account)
    if str( leasedarea[0][0])=="None":
        taskdict["leasedarea"]=0
    else:
        taskdict["leasedarea"]=str( round(leasedarea[0][0], 2))

    taskdict["unitrental"]=0

    return taskdict

def leasedarea(ns):#在租面积

    select_sql='''
 SELECT
 ROUND(SUM(build_area),2)
 FROM
 eh_addresses
 WHERE
 living_status=2
 AND `namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    responsetime=dbsql(select_sql,account)#任务类型数量
    areadict={}
    areadict["name"]="在租面积"
    if str( responsetime[0][0])=="None":
        areadict["value"]=0
    else:
        areadict["value"]=str( round(responsetime[0][0], 2))
    return areadict


def getBetweenDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%y/%m")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)

    return set(date_list)


def montharea(ns):#在租面积

    leasedarea_sql='''

 SELECT
 customer_id ,rent_size ,DATE_FORMAT(contract_start_date,"%y-%m-%d"),DATE_FORMAT(contract_end_date,"%y-%m-%d")
 FROM
 `eh_contracts`
 WHERE
 STATUS =2
 AND  YEAR(contract_end_date )>=YEAR(NOW())
AND rent_size IS NOT NULL
and `namespace_id`={}
    '''.format(ns)
    areaamount_sql='''
   SELECT
 ROUND(SUM(build_area),2)
 FROM
 eh_addresses
 WHERE
 `namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    leasedarea=dbsql(leasedarea_sql,account)#合同签约面积
    areaamount=dbsql(areaamount_sql,account)#园区总面积
    monthareadict={}
    now = datetime.datetime.now()
    today_year = now.year
    data_list_todays = []
    today_year_months = range(1,now.month+1)
    i=0
    areadata=10000
    rentaldata=500
    monthareadictlist=[]
    for today_year_month in today_year_months:
        # 定义date_list 去年加上今年的每个月
        data_list = '%s/%s' % (today_year, today_year_month)
        #通过函数append，得到今年的列表
        data_list_todays.append(data_list)

    if str(leasedarea)=="[]"or str(areaamount[0][0])=="None":
        for month in data_list_todays:
             monthareadict[i]={}
             monthareadict[i]["month"]=month
             monthareadict[i]["leasedarea"]=rentaldata
             monthareadict[i]["rentarea"]=areadata-rentaldata

             rentaldata=rentaldata+500
             monthareadictlist.append( monthareadict[i])
             i=i+1
    else:
        areadata=0
        rentaldata=round(areaamount[0][0],2)
        for month in data_list_todays:
            for value in leasedarea:
                monthareadict[i]={}
                monthareadict[i]["在租面积"]=0
                if month in getBetweenDay(value[2],value[3]):
                   monthareadict[i]["在租面积"]=areadata+round(value[1],2)
            monthareadict[i]["月份"]=month
            monthareadict[i]["待租面积"]=rentaldata-monthareadict[i]["在租面积"]
            monthareadictlist.append(monthareadict[i])
            i=i+1
    return monthareadictlist

def totalenergy(ns):#总能耗

    select_sql='''
SELECT
STR_TO_DATE(`eh_energy_month_statistics`.`date_str`,"%Y")AS taryear,SUM(IF(`meter_type`=1,`current_amount`,0))AS "水表",SUM(IF(`meter_type`=2,`current_amount`,0))AS"电表"
FROM
`eh_energy_month_statistics`
WHERE
`namespace_id`={}
AND YEAR(STR_TO_DATE(`eh_energy_month_statistics`.`date_str`,"%Y"))>=YEAR(DATE_SUB(NOW(),INTERVAL 1 YEAR))
GROUP BY taryear
ORDER BY taryear DESC
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    totalenergy=dbsql(select_sql,account)#能耗
    energyvaluedict={}
    energyvaluelist=[]


    try :
      energyvaluedict["水表"]=str(round((totalenergy[0][1]),2))
    except Exception:
       energyvaluedict["水表"]=0


    try:
      energyvaluedict["电表"]=str(round((totalenergy[0][2]),2))
    except Exception:
       energyvaluedict["电表"]=0
    try:
        energyvaluedict["总能耗"]=str(round((((totalenergy[0][2]*Decimal(0.1229))/1000)+((totalenergy[0][1]*Decimal(0.0857))/1000)),0))
    except Exception:
        energyvaluedict["总能耗"]="0"
    try:
      energyvaluedict["水表同比"]=str(round((totalenergy[0][1]-totalenergy[1][1])/totalenergy[1][1],0))
    except Exception:
        energyvaluedict["水表同比"]="0"
    try:
      energyvaluedict["电表同比"]=str(round((totalenergy[0][2]-totalenergy[1][2])/totalenergy[1][2],0))
    except Exception:
        energyvaluedict["电表同比"]="0"
    try:
     energyvaluedict["总能耗同比"]=str(round((((((totalenergy[0][2]*Decimal(0.1229))/1000)+((totalenergy[0][1]*Decimal(0.0857))/1000))-(((totalenergy[1][2]*Decimal(0.1229))/1000)+((totalenergy[1][1]*Decimal(0.0857))/1000)))/(((totalenergy[1][2]*Decimal(0.1229))/1000)+((totalenergy[1][1]*Decimal(0.0857))/1000))),0))
    except Exception:
        energyvaluedict["总能耗同比"]="0"
    energyvaluelist.append(energyvaluedict)

    return energyvaluelist

def buildmonthwatermeter(ns) :
    list=[{"month":1,"buildno":"A","value":597},{"month":1,"buildno":"B","value":697},{"month":2,"buildno":"B","value":683},{"month":2,"buildno":"A","value":725},{"month":3,"buildno":"A","value":805},{"month":3,"buildno":"B","value":783}]
    return list

def buildmonthelectr(ns) :
    list=[{"month":1,"buildno":"A","value":1297},{"month":1,"buildno":"B","value":1023},{"month":2,"buildno":"B","value":1183},{"month":2,"buildno":"A","value":1172},{"month":3,"buildno":"A","value":1305},{"month":3,"buildno":"B","value":1056}]
    return list

def watermetercureading(ns):#水表读数
    select_sql='''
SELECT a.`meter_id`,a.`meter_name`,a.`meter_number`,(SELECT b.`current_reading` FROM`eh_energy_date_statistics`b WHERE  b.`meter_id`=a.`meter_id`AND b.`create_time`=MAX(a.`create_time`))AS "current_reading"
 FROM `eh_energy_date_statistics` a
WHERE
a.`namespace_id`={}
AND a.`meter_type`=1
GROUP BY a.`meter_id`
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    watermeter=dbsql(select_sql,account)
    watermeterdict={}
    watermeterlist=[]
    dicti=1
    #statusdict={"0":"无状态","1":"待处理","2":"已完成","3":"已延期"}
    for value in watermeter:
        watermeterdict[dicti]={}
        #watermeterdict[dicti]["type"]="品质核查"
        watermeterdict[dicti]["name"]=str(value[1])+"***"+str(value[2])[-2:]
        #watermeterdict[dicti]["handler"]=value[1]
        #qualitytaskdict[dicti]["status"]=statusdict[str(value[2])]
        watermeterdict[dicti]["value"]=str(value[3])
        watermeterlist.append(watermeterdict[dicti])
        dicti=dicti+1
    return watermeterlist

def electrmetercureading(ns):#水表读数
    select_sql='''
SELECT a.`meter_id`,a.`meter_name`,a.`meter_number`,(SELECT b.`current_reading` FROM`eh_energy_date_statistics`b WHERE  b.`meter_id`=a.`meter_id`AND b.`create_time`=MAX(a.`create_time`))AS "current_reading"
 FROM `eh_energy_date_statistics` a
WHERE
a.`namespace_id`={}
AND a.`meter_type`=1
GROUP BY a.`meter_id`
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    electrmeter=dbsql(select_sql,account)
    electrmeterdict={}
    electrmeterlist=[]
    dicti=1
    #statusdict={"0":"无状态","1":"待处理","2":"已完成","3":"已延期"}
    for value in electrmeter:
        electrmeterdict[dicti]={}
        #watermeterdict[dicti]["type"]="品质核查"
        electrmeterdict[dicti]["name"]=str(value[1])+"***"+str(value[2])[-2:]
        #watermeterdict[dicti]["handler"]=value[1]
        #qualitytaskdict[dicti]["status"]=statusdict[str(value[2])]
        electrmeterdict[dicti]["value"]=str(value[3])
        electrmeterlist.append(electrmeterdict[dicti])
        dicti=dicti+1
    return electrmeterlist


def qualityinspetask(ns):#品质核查
    select_sql='''
SELECT
`eh_quality_inspection_tasks`.`task_name`,`eh_organization_members`.`contact_name`,`eh_quality_inspection_tasks`.`status`,DATE_FORMAT(`eh_quality_inspection_tasks`.`executive_start_time`,"%H:%i")
FROM
`eh_quality_inspection_tasks`
LEFT JOIN
`eh_organization_members`
ON `eh_organization_members`.`target_id`=`eh_quality_inspection_tasks`.`executor_id`
WHERE
`eh_quality_inspection_tasks`.`namespace_id`=999992
AND `eh_organization_members`.`target_type`="USER"
ORDER BY `eh_quality_inspection_tasks`.`executive_start_time` DESC
LIMIT 100
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    qualitytask=dbsql(select_sql,account)
    qualitytaskdict={}
    qualitytasklist=[]
    dicti=1
    statusdict={"0":"无状态","1":"待处理","2":"已完成","3":"已延期"}
    for value in qualitytask:
        qualitytaskdict[dicti]={}
        qualitytaskdict[dicti]["type"]="品质核查"
        qualitytaskdict[dicti]["name"]=value[0]
        qualitytaskdict[dicti]["handler"]=value[1]
        qualitytaskdict[dicti]["status"]=statusdict[str(value[2])]
        qualitytaskdict[dicti]["starttime"]=str(value[3])
        qualitytasklist.append(qualitytaskdict[dicti])
        dicti=dicti+1
    return qualitytasklist

def equipmentinspetask(ns):#品质核查
    select_sql='''
SELECT
`eh_equipment_inspection_tasks`.`task_name`, `eh_organization_members`.`contact_name`,`eh_equipment_inspection_tasks`.`status`,DATE_FORMAT(`eh_equipment_inspection_tasks`.`executive_start_time`,"%H:%i")
FROM
`eh_equipment_inspection_tasks`
LEFT JOIN
`eh_organization_members`
ON `eh_organization_members`.`target_id`=`eh_equipment_inspection_tasks`.`executor_id`
WHERE
`eh_organization_members`.`target_type`="USER"
AND `eh_equipment_inspection_tasks`.`namespace_id`=999992
ORDER BY `eh_equipment_inspection_tasks`.`executive_start_time`
LIMIT 100
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    equipmenttask=dbsql(select_sql,account)
    equipmenttaskdict={}
    equipmenttasklist=[]
    dicti=1
    statusdict={"0":"无状态","1":"待执行","2":"需维修","3":"待维修","4":"已完成","5":"已过期"}
    for value in equipmenttask:
        equipmenttaskdict[dicti]={}
        equipmenttaskdict[dicti]["type"]="物业巡检"
        equipmenttaskdict[dicti]["name"]=value[0]
        equipmenttaskdict[dicti]["handler"]=value[1]
        equipmenttaskdict[dicti]["status"]=statusdict[str(value[2])]
        equipmenttaskdict[dicti]["starttime"]=str(value[3])
        equipmenttasklist.append(equipmenttaskdict[dicti])
        dicti=dicti+1
    return equipmenttasklist

def todayquality(ns):#今日品质任务

    select_sql='''
SELECT
COUNT(`eh_quality_inspection_tasks`.`id`),COUNT(IF(`eh_quality_inspection_tasks`.`status`=1,`eh_quality_inspection_tasks`.`id`,NULL))AS "待办",
COUNT(IF(`eh_quality_inspection_tasks`.`status`=2,`eh_quality_inspection_tasks`.`id`,NULL))AS "已办",COUNT(IF(`eh_quality_inspection_tasks`.`status`=3,`eh_quality_inspection_tasks`.`id`,NULL))AS "已过期",
COUNT(IF(`eh_quality_inspection_tasks`.`result`IN (1,3,5),`eh_quality_inspection_tasks`.`id`,NULL))AS "整改"
FROM
`eh_quality_inspection_tasks`
WHERE
DATE_FORMAT(`eh_quality_inspection_tasks`.`executive_start_time`,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')
AND `eh_quality_inspection_tasks`.`namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    todayquality=dbsql(select_sql,account)#任务类型数量
    todayqualitydict={}
    todayqualitylist=[]

    todayqualitydict["total"]=todayquality[0][0]
    todayqualitydict["changerate"]=todayquality[0][1]
    todayqualitydict["finish"]=todayquality[0][2]
    todayqualitydict["expire"]=todayquality[0][3]
    try:
      todayqualitydict["expirerate"]=round(((todayquality[0][3])/(todayquality[0][0])),2)
    except Exception:
        todayqualitydict["expirerate"]="--"
    try:
      todayqualitydict["changerate"]=round(((todayquality[0][4])/(todayquality[0][0])),2)
    except Exception:
        todayqualitydict["changerate"]="--"
    try:
     todayqualitydict["complerate"]=round(((todayquality[0][2])/(todayquality[0][0])),2)
    except Exception:
        todayqualitydict["complerate"]="--"
    try:
     todayqualitydict["responrate"]=round((todayequipment[0][2]+todayequipment[0][1])/(todayequipment[0][0]),3)
    except Exception:
        todayqualitydict["responrate"]="--"

    return todayqualitylist

def todayequipment(ns):#今日巡检任务

    equipment_sql='''
SELECT
COUNT(`eh_equipment_inspection_tasks`.`id`),COUNT(IF(`eh_equipment_inspection_tasks`.`status`IN (1,2,3),`eh_equipment_inspection_tasks`.`id`,NULL))AS "待办",
COUNT(IF(`eh_equipment_inspection_tasks`.`status`=4,`eh_equipment_inspection_tasks`.`id`,NULL))AS "已办",COUNT(IF(`eh_equipment_inspection_tasks`.`status`=5,`eh_equipment_inspection_tasks`.`id`,NULL))AS "已过期"
FROM
`eh_equipment_inspection_tasks`
WHERE
DATE_FORMAT(`eh_equipment_inspection_tasks`.`executive_start_time`,'%Y-%m-%d')=DATE_FORMAT(NOW(),'%Y-%m-%d')
AND `eh_equipment_inspection_tasks`.`namespace_id`={}

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    todayequipment=dbsql(equipment_sql,account)#任务类型数量
    equipmentdict={}
    todayqualitylist=[]
    equipmentdict["total"]=todayequipment[0][0]
    equipmentdict["waitting"]=todayequipment[0][1]
    equipmentdict["finish"]=todayequipment[0][2]
    equipmentdict["expire"]=todayequipment[0][3]
    try:
      equipmentdict["complerate"]=round((todayequipment[0][2])/(todayequipment[0][0]),2)
    except Exception:
        equipmentdict["complerate"]="--"
    try:
      equipmentdict["responrate"]=round((todayequipment[0][2]+todayequipment[0][1])/(todayequipment[0][0]),3)
    except Exception:
        equipmentdict["responrate"]="--"

    return equipmentdict

def inspectiontasktype(ns):#任务类型分布

    equipment_sql='''
    SELECT
COUNT(`eh_equipment_inspection_tasks`.`id`),COUNT(IF(`eh_equipment_inspection_tasks`.`status`=4,`eh_equipment_inspection_tasks`.`id`,NULL))AS "已办"
FROM
`eh_equipment_inspection_tasks`
WHERE
DATE_FORMAT(`eh_equipment_inspection_tasks`.`executive_start_time`,'%Y')=DATE_FORMAT(NOW(),'%Y')
AND `eh_equipment_inspection_tasks`.`namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    equipmenttotal=dbsql(equipment_sql,account)
    tasktypedict={}
    tasktypelist=[]
    try:
      tasktypedict["equipment"]=equipmenttotal[0][0]
    except Exception:
       tasktypedict["equipment"]=0
    quality_sql='''
    SELECT
COUNT(`eh_quality_inspection_tasks`.`id`),COUNT(IF(`eh_quality_inspection_tasks`.`status`=2,`eh_quality_inspection_tasks`.`id`,NULL))AS "已办"
FROM
`eh_quality_inspection_tasks`
WHERE
DATE_FORMAT(`eh_quality_inspection_tasks`.`executive_start_time`,'%Y')=DATE_FORMAT(NOW(),'%Y')
AND `eh_quality_inspection_tasks`.`namespace_id`={}
    '''.format(ns)
    qualitytotal=dbsql(quality_sql,account)
    try:
     tasktypedict["quality"]=qualitytotal[0][0]
    except Exception:
       tasktypedict["quality"]=0
    try :
      tasktotal=qualitytotal[0][0]+equipmenttotal[0][0]
    except Exception:
        tasktotal=0
    try :
      taskcompleted=qualitytotal[0][1]+equipmenttotal[0][1]
    except Exception:
        taskcompleted=0
    try :
        tasktypedict["complerate"]=round((taskcompleted/tasktotal),2)
    except Exception:
        tasktypedict["complerate"]="--"
    tasktypelist.append(tasktypedict)

    return tasktypelist

def activityenrollment(ns):#活动报名人数

    select_sql='''
SELECT COUNT(IF (`eh_activity_roster`.`confirm_flag`=1 AND `eh_activity_roster`.`status` NOT IN (0, 1) ,`eh_activity_roster`.`id` , NULL ))AS "报名人数",COUNT(DISTINCT `eh_activities`.id) AS "发布总数"FROM eh_activity_roster
LEFT JOIN
`eh_activities`
ON `eh_activities`.id=`eh_activity_roster`.`activity_id`
WHERE `eh_activities`.`status`=2
AND `eh_activities`.`namespace_id`={}
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    activityenroll=dbsql(select_sql,account)#
    activityenrolldict={}
    if activityenroll==[]:
        activityenrolldict["enroll"]=0
        activityenrolldict["acttotal"]=0
        activityenrolldict["aveper"]=0
    else:
        activityenrolldict["enroll"]=activityenroll[0][0]
        activityenrolldict["acttotal"]=activityenroll[0][1]
        activityenrolldict["aveper"]=int(round(activityenroll[0][0]/activityenroll[0][1],0))
    return activityenrolldict

def forumthreads (ns):#帖子情况

    select_sql='''


SELECT COUNT(IF(eh_forum_posts.parent_post_id = 0,eh_forum_posts.`id`,NULL)) ,SUM(IF(eh_forum_posts.parent_post_id = 0,eh_forum_posts.view_count,0)),
COUNT(IF(eh_forum_posts.parent_post_id <>0,eh_forum_posts.`id`,NULL)),SUM(`eh_forum_posts`.`like_count`)
 FROM eh_forum_posts
 LEFT JOIN `eh_forums`
 ON `eh_forums`.`id`=eh_forum_posts.`forum_id`
 WHERE   eh_forum_posts.`status` = 2 AND `eh_forums`.`namespace_id`={} ;

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    forumthreads=dbsql(select_sql,account)#
    forumthreadsdict={}
    forumthreadsdict["post"]=str(forumthreads[0][0])
    forumthreadsdict["viewcount"]=str(forumthreads[0][1])
    forumthreadsdict["reply"]=str(forumthreads[0][2])
    forumthreadsdict["likecount"]=str(forumthreads[0][3])
    return forumthreadsdict

def activitytype(ns):#帖子标签分布数
    select_sql='''
SELECT tag, COUNT(*) FROM eh_activities WHERE STATUS = 2 AND eh_activities.`namespace_id` ={} GROUP BY tag  ORDER BY COUNT(*) DESC;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    activitytype=dbsql(select_sql,account)#入住率
    activitytypedict={}
    activitytypelist=[]
    dicti=1
    if activitytype==[]:
        activitytypedict["name"]=0
        activitytypedict["value"]=0
        activitytypelist.append(activitytypedict)
    else:
        for value in activitytype:
            activitytypedict[dicti]={}

            activitytypedict[dicti]["name"]=str(value[0])
            activitytypedict[dicti]["value"]=str((value[1]))
            activitytypelist.append(activitytypedict[dicti])
            dicti=dicti+1
    return activitytypelist

def activityattention(ns):#帖子标签分布数
    select_sql='''
SELECT ac.tag, SUM(view_count) FROM eh_forum_posts po, eh_activities ac WHERE po.id = ac.post_id AND ac.`status` = 2 AND ac.`namespace_id` ={} GROUP BY tag ORDER BY COUNT(*) DESC;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    activityattention=dbsql(select_sql,account)
    activityattentiondict={}
    activityattentionlist=[]
    dicti=1
    if activityattention==[]:
        activityattentiondict["name"]=0
        activityattentiondict["value"]=0
        activityattentionlist.append(activityattentiondict)
    else:
        for value in activityattention:
            activityattentiondict[dicti]={}

            activityattentiondict[dicti]["name"]=str(value[0])
            activityattentiondict[dicti]["value"]=str((value[1]))
            activityattentionlist.append(activityattentiondict[dicti])
            dicti=dicti+1
    return activityattentionlist

def trendingtopics(ns):#话题前五
    select_sql='''

SELECT `eh_forum_posts`.`category_path`, `eh_forum_posts`.subject, `eh_forum_posts`.view_count
FROM eh_forum_posts
LEFT JOIN
`eh_forums` ON `eh_forums`.id=`eh_forum_posts`.`forum_id`
WHERE `eh_forum_posts`.parent_post_id = 0
AND `eh_forum_posts`.`status` = 2 AND `eh_forums`.`namespace_id`={}
 ORDER BY `eh_forum_posts`.view_count DESC LIMIT 5;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    trendingtopics=dbsql(select_sql,account)
    trendingtopicsdict={}
    trendingtopicslist=[]
    dicti=1
    if trendingtopics==[]:
        trendingtopicsdict["type"]=0
        trendingtopicsdict["name"]=0
        trendingtopicsdict["value"]=0
        trendingtopicslist.append(trendingtopicsdict)
    else:
        for value in trendingtopics:
            trendingtopicsdict[dicti]={}
            if '/' in value[0]:
              trendingtopicsdict[dicti]["type"]=substr((value[0]),'/','"')
            else:
                trendingtopicsdict[dicti]["type"]=str(value[0])
            trendingtopicsdict[dicti]["name"]=str(value[1])
            trendingtopicsdict[dicti]["value"]=str((value[2]))
            trendingtopicslist.append(trendingtopicsdict[dicti])
            dicti=dicti+1
    return trendingtopicslist
def newactivity(ns):#话题前五
    select_sql='''
 SELECT `eh_activities`.id ,`eh_activities`.`subject`,`eh_activities`.`tag`,`eh_activities`.`create_time`,
  COUNT(IF (`eh_activity_roster`.`confirm_flag`=1 AND `eh_activity_roster`.`status` NOT IN (0, 1) ,`eh_activity_roster`.`id` , NULL ))AS "报名人数"
 FROM eh_activities
 LEFT JOIN `eh_activity_roster`
 ON `eh_activity_roster`.`activity_id`=`eh_activities`.`id`
 WHERE `eh_activities`.STATUS = 2
 AND `eh_activities`.`namespace_id`={}
 GROUP BY `eh_activities`.id
 ORDER BY `eh_activities`.create_time DESC
 LIMIT 10;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    newactivity=dbsql(select_sql,account)
    newactivitydict={}
    newactivitylist=[]
    dicti=1
    if newactivity==[]:
        newactivitydict["type"]=0
        newactivitydict["name"]=0
        newactivitydict["value"]=0
        newactivitydict["time"]=0
        newactivitylist.append(newactivitydict)
    else:
        for value in newactivity:
            newactivitydict[dicti]={}
            newactivitydict[dicti]["type"]=str(value[2])
            newactivitydict[dicti]["name"]=str(value[1])
            newactivitydict[dicti]["value"]=str(value[4])
            newactivitydict[dicti]["time"]=str(value[3])
            newactivitylist.append(newactivitydict[dicti])
            dicti=dicti+1
    return newactivitylist
def newforum(ns):#话题前五
    select_sql='''
 SELECT
 eh_forum_posts.`category_path`,eh_forum_posts.`subject`, eh_forum_posts.`create_time`,
 SUM(eh_forum_posts.`view_count`)AS "报名人数"
  FROM
 eh_forum_posts
 LEFT JOIN
 `eh_forums`
 ON `eh_forums`.`id`=eh_forum_posts.`forum_id`
 WHERE eh_forum_posts.parent_post_id = 0
 AND eh_forum_posts.`status` = 2
 AND `eh_forums`.`namespace_id`="999992"
 GROUP BY eh_forum_posts.`category_path`
 ORDER BY eh_forum_posts.create_time DESC
 LIMIT 10;
    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    newforum=dbsql(select_sql,account)
    newforumdict={}
    newforumlist=[]
    dicti=1
    if newforum==[]:
        newforumdict["type"]=0
        newforumdict["name"]=0
        newforumdict["value"]=0
        newforumdict["time"]=0
        newforumlist.append(newforumdict)
    else:
        for value in newforum:
            newforumdict[dicti]={}
            if "活动"in str(value[0]):
                continue
            newforumdict[dicti]["type"]=str(value[0])
            newforumdict[dicti]["name"]=str(value[1])
            newforumdict[dicti]["value"]=str(value[3])
            newforumdict[dicti]["time"]=str(value[2])
            newforumlist.append(newforumdict[dicti])
            dicti=dicti+1
    return newforumlist

def communityuseract(ns):#用户统计
    select_sql='''
SELECT
`cumulative_user_number`,`active_user_number`,`seven_active_user_number`,`thirty_active_user_number`
FROM
`eh_terminal_day_statistics`
WHERE
DATE_FORMAT(`create_time`,"%Y-%m-%d")=DATE_FORMAT(NOW(),'%Y-%m-%d')
AND `namespace_id`={}
    '''.format(ns)
    select__newuser_sql='''

SELECT
SUM(IF(DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= DATE(`create_time`),`new_user_number`,0))AS"7天",SUM(IF(DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(`create_time`),`new_user_number`,0))AS"30天"
FROM
`eh_terminal_day_statistics`
WHERE
 `namespace_id`=1000000
    '''
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    useract=dbsql(select_sql,account)
    newuser=dbsql(select__newuser_sql,account)
    useractdict={}

    if useract==[]:
        useractdict["totaluser"]=0
        useractdict["dayactiveuser"]=0
        useractdict["sevenactiveuser"]=0
        useractdict["thirtyactiveuser"]=0
        useractdict["thirtynewuser"]=0
        useractdict["sevenneweuser"]=0
    else:

        useractdict["totaluser"]=useract[0][0]
        useractdict["activeuser"]=useract[0][1]
        useractdict["sevenactiveuser"]=useract[0][2]
        useractdict["thirtyactiveuser"]=useract[0][3]
        useractdict["thirtynewuser"]=str(newuser[0][0])
        useractdict["sevenneweuser"]=str(newuser[0][1])
    return useractdict
def daynewusertrend(ns):#每日新增
    select_sql='''
 SELECT
 `date`,`new_user_number`
 FROM
 `eh_terminal_day_statistics`
 WHERE
 DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(`create_time`)
 AND  `namespace_id`={}
ORDER BY `create_time`

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    usertrend=dbsql(select_sql,account)
    usertrenddict={}
    usertrendlist=[]
    dicti=1
    if usertrend==[]:
        usertrenddict["value"]=0
        usertrenddict["name"]=0
        usertrendlist.append(usertrenddict)
    else:
        for value in usertrend:
            usertrenddict[dicti]={}
            date=time.strptime(str(value[0]), "%Y%m%d")
            usertrenddict[dicti]["name"]=time.strftime("%Y/%m/%d", date)
            usertrenddict[dicti]["value"]=str(value[1])
            usertrendlist.append(usertrenddict[dicti])
            dicti=dicti+1
    return usertrendlist

def dayactusertrend(ns):#每日活跃
    select_sql='''
 SELECT
 `date`,`active_user_number`
 FROM
 `eh_terminal_day_statistics`
 WHERE
 DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(`create_time`)
 AND  `namespace_id`={}
ORDER BY `create_time`

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    usertrend=dbsql(select_sql,account)
    usertrenddict={}
    usertrendlist=[]
    dicti=1
    if usertrend==[]:
        usertrenddict["value"]=0
        usertrenddict["name"]=0
        usertrendlist.append(usertrenddict)
    else:
        for value in usertrend:
            usertrenddict[dicti]={}
            date=time.strptime(str(value[0]), "%Y%m%d")
            usertrenddict[dicti]["name"]=time.strftime("%Y/%m/%d", date)
            usertrenddict[dicti]["value"]=str(value[1])
            usertrendlist.append(usertrenddict[dicti])
            dicti=dicti+1
    return usertrendlist

def daytotalusertrend(ns):#每日累计
    select_sql='''
 SELECT
 `date`,`cumulative_change_rate`
 FROM
 `eh_terminal_day_statistics`
 WHERE
 DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(`create_time`)
 AND  `namespace_id`={}
ORDER BY `create_time`

    '''.format(ns)
    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    usertrend=dbsql(select_sql,account)
    usertrenddict={}
    usertrendlist=[]
    dicti=1
    if usertrend==[]:
        usertrenddict["value"]=0
        usertrenddict["name"]=0
        usertrendlist.append(usertrenddict)
    else:
        for value in usertrend:
            usertrenddict[dicti]={}
            date=time.strptime(str(value[0]), "%Y%m%d")
            usertrenddict[dicti]["name"]=time.strftime("%Y/%m/%d", date)
            usertrenddict[dicti]["value"]=str(value[1])
            usertrendlist.append(usertrenddict[dicti])
            dicti=dicti+1
    return usertrendlist
def usergender(ns):#用户统计
    select_sql='''

SELECT
COUNT(IF(`gender`=1,`id`,NULL))AS"男",COUNT(IF(`gender`=2,`id`,NULL))AS"女"
FROM
`eh_users`
WHERE
`namespace_id`={}
    '''.format(ns)

    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    useract=dbsql(select_sql,account)
    useractdict={}

    if useract==[]:
        useractdict["male"]=0
        useractdict["female"]=0
    else:

        useractdict["male"]=useract[0][0]
        useractdict["female"]=useract[0][1]
    return useractdict
def ostype(ns):#用户统计
    select_sql='''

SELECT
COUNT(IF(`gender`=1,`id`,NULL))AS"男",COUNT(IF(`gender`=2,`id`,NULL))AS"女"
FROM
`eh_users`
WHERE
`namespace_id`={}
    '''.format(ns)

    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    useract=dbsql(select_sql,account)
    useractdict={}

    if useract==[]:
        useractdict["ios"]=0
        useractdict["Android"]=0
    else:

        useractdict["iOS"]=useract[0][0]
        useractdict["Android"]=useract[0][1]
    return useractdict

def ostype(ns):#用户统计
    select_sql='''

SELECT
COUNT(IF(`gender`=1,`id`,NULL))AS"男",COUNT(IF(`gender`=2,`id`,NULL))AS"女"
FROM
`eh_users`
WHERE
`namespace_id`={}
    '''.format(ns)

    account={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":"ehcore","port":"3306",}
    useract=dbsql(select_sql,account)
    useractdict={}

    if useract==[]:
        useractdict["ios"]=0
        useractdict["Android"]=0
    else:

        useractdict["iOS"]=useract[0][0]
        useractdict["Android"]=useract[0][1]
    return useractdict



if __name__ == '__main__':
    #list1,list2,list3,list4,list5,list6=incomedata()
    #print(list1,'\n',list2,'\n',list3,'\n',list4,'\n',list5,'\n',list6)
    list1=usergender(2)
    print(list1)