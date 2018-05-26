# -*- coding:utf-8 -*-
__author__ = 'wuhan'

from DAO import Dao
from baidumap import xBaiduMap

if __name__ == '__main__':
    Dao = Dao()
    # query_sql = "SELECT url,location FROM merchant  WHERE SOURCE_ID = 16      "
    # result = Dao.execute_query(query_sql)
    # for url , location  in result:
    #     bm=xBaiduMap()
    #     print(location ,url)
    #     if location is not None:
    #         zuobiao = bm.getLocation(location,"深圳")
    #         print(zuobiao)
    #         if zuobiao is None:
    #             continue
    #         LONGITUDE = zuobiao[1]
    #         LATITUDE = zuobiao [0]
    #         update_sql = "update merchant set LONGITUDE = '{}' ,LATITUDE = '{}' where url = '{}' and  SOURCE_ID = 16 ".format(LONGITUDE , LATITUDE , url)
    #         Dao.execute_dmls(update_sql)

    query_sql = " SELECT id, BAIDU_LATI , BAIDU_LONG FROM job_beijing  WHERE baidu_lati IS NOT NULL    "
    result = Dao.execute_query(query_sql)
    for COMMUNITY_ID, LATITUDE, LONGITUDE in result:
        bm = xBaiduMap( )
        if LATITUDE is not None:
            try:
                location = bm.getAddress(LONGITUDE,LATITUDE)
            except Exception as e :
                print(e)
                continue
            if location is None:
                continue
            update_sql = "update job_beijing set addr = '{}' where id = '{}'   ".format(
                location, COMMUNITY_ID)
            Dao.execute_dmls(update_sql)