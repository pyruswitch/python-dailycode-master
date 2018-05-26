__author__ = 'Administrator'

import mysql.connector
from configparser import ConfigParser
from baidumap import xBaiduMap


class Dao(object):
    def __init__(self):
        config = ConfigParser()
        config.read("etc/config.cnf")
        self.__user = config.get("dbconfig", "user")
        self.__pwd = config.get("dbconfig", "pwd")
        self.__db_host = config.get("dbconfig", "db_host")
        self.__db_port=config.get("dbconfig", "db_port")
        self.__db = 'shengchan_20140815'

    def execute_dmls(self, sqls):
        """
        execute sql update and insert
        :param sql:
        :return:
        """

        cnx = mysql.connector.connect(user=self.__user, password=self.__pwd, host=self.__db_host,port=self.__db_port, database=self.__db)
        cursor = cnx.cursor()
        try:
            # print("insert begin")

            print("DML sql begin " + sqls)
            cursor.execute(sqls)
            # map(cursor.execute, sqls)
            cnx.commit()
            # print("insert end")
        except mysql.connector.Error as sql_err:
            print("Error: {}".format(sql_err.msg))
            log_sql = open('etc/test.log', 'a', encoding='utf-8')
            log_sql.write("Error: {} \n in the insert/update sql :{}".format(sql_err.msg, sqls))
            log_sql.close()
            cnx.rollback()
        finally:
            cursor.close()
            cnx.close

    def execute_query(self, sql):
        """
        execute sql query
        :param sql:
        :return: result_list
        """

        cnx = mysql.connector.connect(user=self.__user, password=self.__pwd, host=self.__db_host,port=self.__db_port, database=self.__db)
        print(sql)
        cursor = cnx.cursor()
        try:
            cursor.execute(sql)
            # result = copy.deepcopy(cursor.fetchone())
            # if result is None:
            # return None
            results = cursor.fetchall()
            if len(results) == 0:
                return None
            return results
        except mysql.connector.Error as sql_err:
            print("Error: {}".format(sql_err.msg))
            log_sql = open('etc/test.log', 'a')
            log_sql.write("Error: {} \n in the qury sql :{}".format(sql_err.msg, sql))
            log_sql.close()
            # cursor.close()des

        finally:
            cursor.close()
            cnx.close()

    def _get_url_by_id(self, sourceid):
        sql = "select url from fetch_list where source_id = {} and times = 0".format(sourceid)
        return self.execute_query(sql)


if __name__ == '__main__':
    dao = Dao()
    dao.execute_dmls("delete from  community_weining ; ")  # delete everytime
    sql = "SELECT id ,c.`NAME` cityName ,a.`NAME` comName  FROM community_applicants a ,cities  c WHERE a.status = 1 AND a.`CITY_ID` = c.`CITY_ID`  "
    # sql = "SELECT id ,c.`NAME` cityName ,a.`NAME` comName  FROM community_applicants a ,cities  c WHERE a.status = 1 AND a.`CITY_ID` = c.`CITY_ID` AND A.ID =31212    "
    bm = xBaiduMap()
    fileHandle = open('E:/test.txt', 'w')
    for id, cityName, comName in dao.execute_query(sql):
        location = bm.getSuggestion(comName, cityName)
        if location == None or len(location) < 1:
            if bm.getLocation(comName, cityName) == None:
                fileHandle.write(
                    "UPDATE community_applicants SET STATUS = 0 WHERE id ={}  AND NAME = '{}' ; \n".format(id, comName))
                print("UPDATE community_applicants SET STATUS = 0 WHERE id ={}  AND NAME = '{}' ;".format(id, comName))
        else:
            try:
                baidu = location[0]
                baiduaddress = bm.getAddress(baidu["location"]["lat"], baidu["location"]["lng"])
                updateSql = " INSERT INTO community_weining(id,cityName,NAME,baiduName,lat,lng,district,baiduaddress) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}') ; ".format(
                    id, cityName, comName, baidu["name"], baidu["location"]["lat"], baidu["location"]["lng"],
                    baidu["district"], baiduaddress)
                dao.execute_dmls(updateSql)
            except Exception as e:
                print(e)
    fileHandle.close()
