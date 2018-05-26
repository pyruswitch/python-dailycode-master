__author__ = 'vincent'

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

    cursor.execute(select_sql, multi=True)
    cnx.commit()
    cursor.close()
    cnx.close()


def cre_db(dbname):
    select_sql='''
create database if not exists
        '''+dbname
    cnx=mysql.connector.connect(user='root',password='vc123456',database='',host='127.0.0.1',port='3306')
    cursor=cnx.cursor()
    cursor.execute(select_sql)
#    print(dbname+"已创建")
    cnx.close()

def backup_database(dbname,tablename):
    select_sql='''

        '''
    print(select_sql)
    account={"user":"root","pwd":"vc123456","host":"localhost","db":dbname,"port":"3306",}
    dbsql(select_sql,account)
    print()

def re_exe(path,account,inc,filename):
    os.chdir(path)
    if not os.path.exists('incre_backup'):
           os.mkdir('incre_backup')
    #切换到新建的文件夹中
    os.chdir('incre_backup')
    #def tuplesql(command,server,user,passwd,db,table,filename):
    #   return (mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,exportfile)
    #定义一系列参数
    mysqlcomm='mysqldump'
    dbserver=account["host"]
    dbuser=account["user"]
    dbpasswd=account["pwd"]
    dbname=account["db"]
    dbtable=account["dbtable"]
    last_backup_time=backup_db(path,account,filename)
    increbackup_sqlfromat='{} --host={} -t -u{} -p{}  {}  {} --replace --single-transaction --where "{}">{}'
    while True:
        os.chdir(path)
        os.chdir('incre_backup')
        now_time = time.strftime('%Y%m%d%H%M%S')
        exportfile=str(now_time)+'.sql'
        print(exportfile)
        timeArray = time.strptime(now_time, "%Y%m%d%H%M%S")
        this_backup_time=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        increquerycr="{} between '{}' and '{}'".format(filename,last_backup_time,this_backup_time)

        increbackup_sql=(increbackup_sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,increquerycr,exportfile))
        result=os.popen(increbackup_sql)
        last_backup_time=this_backup_time
        #print(result)
        #对sql执行进行判断
        if result:
            print("backup completed!")
            time.sleep(5)
            execute_sql(path,exportfile)
            time.sleep(inc)
        else:
            print("I'm sorry!!!,backup failed!")
            time.sleep(inc)


def execute_sql(path,exportfile):
    """ """
    os.chdir(path)

    account={"user":"root","pwd":"vc123456","host":"127.0.0.1","db":'basedbtest',"port":"3306",}
    #for each in os.listdir("."):
    count = 0   #读取行数
    sql = ""    #拼接的sql语句
    if os.path.exists(exportfile) == True:
            with open(exportfile, "r", encoding="utf-8") as f:
                for each_line in f.readlines():
                    # 过滤数据
                    if not each_line or each_line == "\n":
                        continue
                    # 读取2000行数据，拼接成sql
                    elif count <2000:
                        sql += each_line
                        count += 1
                    # 读取达到2000行数据，进行提交，同时，初始化sql，count值
                    else:

                        dbsql(sql,account)
                        print("每两千条写入一次")
                        sql = each_line
                        count = 1
                # 当读取完毕文件，不到2000行时，也需对拼接的sql 执行、提交
                if sql is not None:
                    cnx=mysql.connector.connect(user="root",password="vc123456",database='basedbtest',host="127.0.0.1",port='3306')
                    cursor=cnx.cursor()
                    for result in cursor.execute(sql, multi=True):
                      pass
                    print("import completed")

def  backup_db(path,account,filename):

    os.chdir(path)
    if not os.path.exists('incre_backup'):
           os.mkdir('incre_backup')
    #切换到新建的文件夹中
    os.chdir('incre_backup')
    #def tuplesql(command,server,user,passwd,db,table,filename):
    #   return (mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,exportfile)
    #定义一系列参数
    mysqlcomm='mysqldump'
    dbserver=account["host"]
    dbuser=account["user"]
    dbpasswd=account["pwd"]
    dbname=account["db"]
    dbtable=account["dbtable"]
    now_time = time.strftime('%Y%m%d%H%M%S')
    exportfile=str(now_time)+'.sql'
    #querycr=account['queryc']
    timeArray = time.strptime(now_time, "%Y%m%d%H%M%S")
    querycrtime=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    fullquerycr="{} <=\'{}\'".format(filename,str(querycrtime))

    #increquerycr="create_time>"+now_time.strftime('%Y-%m-%d %H:%M:%S')
    #定义sql的格式
    print(exportfile)
    path=os.getcwd()
    #exportfilepath=os.path.abspath(exportfile)
    #increbackup_sqlfromat='{} --host={} -t -u{} -p{}  {}  {} --replace --single-transaction --where "{}">{}'
    fullbackup_sqlfromat='{} --host={}  -u{} -p{}  {}  {} --single-transaction --where "{}">{}'
    #mysqldump -uroot -proot --databases db1 --tables a1 --where='id=1'  >/tmp/a1.sql
    #生成相应的sql语句
    #sql=(sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,querycr,exportfile))

    fullbackup_sql=(fullbackup_sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,fullquerycr,exportfile))

    #increbackup_sql=(increbackup_sqlfromat.format(mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,increquerycr,exportfile))
    print(fullbackup_sql)
    #执行sql并获取语句

    result=os.popen(fullbackup_sql)
    #print(result)
   #对sql执行进行判断
    if result:
        print("backup completed!")
        time.sleep(5)
        execute_sql(path,exportfile)
    else:
        print("I'm sorry!!!,backup failed!")






    return querycrtime


if __name__ == '__main__':
    #execute_sql(r"H:\upupup\电商后台\sql\sql文件 ")
    #account_payorder={"user":"root","pwd":"vc123456","host":"localhost","db":'basedbtest',"port":"3306",'dbtable':'pay_orders','queryc':"create_time>'2017-11-22'"}
    #account_ehbiz={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":'ehcore',"port":"18306",'dbtable':'eh_customer_events','queryc':""}
    #account_ehcore={"user":"ehcore","pwd":"ehcore","host":"10.1.10.45","db":'ehcore',"port":"18306",'dbtable':'eh_customer_events','queryc':"create_time>'2017-11-24'"}
    #incre_db(r"H:\upupup\电商后台\sql\sql文件 ",account_payorder)
    #backup_db(r"H:\upupup\电商后台\sql\sql文件 ",account_ehbiz)
    #re_exe(r"H:\upupup\电商后台\sql\sql文件 ",account_ehcore,120,"create_time")
    execute_sql(r'H:\upupup\电商后台\sql\sql文件',"pay_orders_20180418.sql")