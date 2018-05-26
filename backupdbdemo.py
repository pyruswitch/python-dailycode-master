__author__ = 'vincent'
# -*- coding: utf-8 -*-
import mysql.connector
import os
import time
import sys



def dbsql(selectsql,account):
    user=account["user"]
    pwd=account["pwd"]
    host=account["host"]
    db=account["db"]
    port=account["port"]

    cnx=mysql.connector.connect(user=user,password=pwd,database=db,host=host,port=port)
    cursor=cnx.cursor()
    select_sql=selectsql

    cursor.execute(select_sql)
    cnx.commit()
    cursor.close()
    cnx.close()
def import_sqlfile(account,filepath):
    #定义一系列参数
    mysqlcomm='mysqldump'
    dbserver=account["host"]
    dbuser=account["user"]
    dbpasswd=account["pwd"]
    dbname=account["db"]
    #dbtable=account["dbtable"]
    import_sqlformat='mysql -u{} -p{} -h{} {}  < {}'.format(dbuser,dbpasswd,dbserver,dbname,filepath)
    result=os.popen(import_sqlformat)
    if result:
        print(import_sqlformat)
        print(" backup completed!")
    else:
        print(" I'm sorry!!!,backup failed!")

def re_exe(account,inc,fieldname):

    #定义一系列参数
    mysqlcomm='mysqldump'
    dbserver=account["host"]
    dbuser=account["user"]
    dbpasswd=account["pwd"]
    dbname=account["db"]
    dbtable=account["dbtable"]
    last_backup_time= time.strftime('%Y%m%d%H%M%S')
    timeArray = time.strptime(last_backup_time, "%Y%m%d%H%M%S")
    querycrtime=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    fullquerycr="{} <=\'{}\'".format(fieldname,str(querycrtime))

    #定义sql的格式
    fullbackup_sqlfromat='{} --host={}  -u{} -p{}  {}  {} --single-transaction --where "{}" |mysql --host=localhost -uroot -pvc123456 basedbtest'

    fullbackup_sql=(fullbackup_sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,fullquerycr))

    print(fullbackup_sql)
    #执行sql并获取语句

    result=os.popen(fullbackup_sql)
    if result:
        print("fullbackup completed!")

        increbackup_sqlfromat='{} --host={} -t -u{} -p{}  {}  {} --replace --single-transaction --where "{}" |mysql --host=localhost -uroot -pvc123456 basedbtest'
        while True:

            now_time = time.strftime('%Y%m%d%H%M%S')

            timeArray = time.strptime(now_time, "%Y%m%d%H%M%S")
            this_backup_time=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            increquerycr="{} between '{}' and '{}'".format(fieldname,last_backup_time,this_backup_time)

            increbackup_sql=(increbackup_sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,increquerycr))
            result=os.popen(increbackup_sql)
            last_backup_time=this_backup_time
            #print(result)
            #对sql执行进行判断
            if result:
                print(this_backup_time+" backup completed!")
            else:
                print(this_backup_time+" I'm sorry!!!,backup failed!")
            time.sleep(inc)
    else:
        print("I'm sorry!!!,fullbackup failed!")




if __name__ == '__main__':
    #account_payorder={"user":"root","pwd":"vc123456","host":"localhost","db":'basedbtest',"port":"3306",'dbtable':'pay_orders','queryc':"create_time>'2017-11-22'"}
    #account_ehbiz={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":'ehcore',"port":"18306",'dbtable':'eh_customer_events','queryc':""}
    #account_ehcore={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":'ehcore',"port":"18306",'dbtable':'eh_customer_events'}

    #re_exe(account_ehcore,300,"create_time")
    #execute_sql(r'H:\upupup\电商后台\sql\sql文件\incre_backup')
    account={"user":"root","pwd":"vc123456","host":"localhost","db":'basedbtest',"port":"3306"}
    path=r'H:\upupup\电商后台\sql\sql文件\pay_orders20180104.sql'
    import_sqlfile(account,path)