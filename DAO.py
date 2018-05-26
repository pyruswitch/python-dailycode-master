__author__ = 'wuhan'
import mysql.connector
import copy
from configparser import ConfigParser
import  StrUtil



class Dao(object):
    def __init__(self):
        config = ConfigParser()
        config.read("etc/config.cnf")
        self.__user = config.get("dbconfig", "user")
        self.__pwd = config.get("dbconfig", "pwd")
        self.__db_host = config.get("dbconfig", "db_host")
        self.__db = config.get("dbconfig", "db")

    def execute_dmls(self, sqls):
        """
        execute sql update and insert
        :param sql:
        :return:
        """

        cnx = mysql.connector.connect(user=self.__user, password=self.__pwd, host=self.__db_host, database=self.__db)
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

        cnx = mysql.connector.connect(user=self.__user, password=self.__pwd, host=self.__db_host, database=self.__db)
        print(sql)
        cursor = cnx.cursor()
        try:
            cursor.execute(sql)
            # result = copy.deepcopy(cursor.fetchone())
            # if result is None:
            #     return None
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
    Dao = Dao()
    sql = "select description from merchant_tmp where phone ='' "
    result = Dao.execute_query(sql)
    for re in result:
        phone =   StrUtil.find_Phone_Num(re[0])
        name = StrUtil.find_name(re[0])
        update_sql = "update merchant_tmp set phone = '{}',name = '{}' where description ='{}' ".format(phone,name,re[0])
        Dao.execute_dmls(update_sql)
