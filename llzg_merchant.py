# coding=utf-8
# -*- coding: utf-8 -*-
__author__ = 'wuhan'
import urllib.request
import json
from DAO import Dao


def getmerchants(lat, long, COMMUNITY_ID):
    dao = Dao()
    param = {
        'long': long,
        'lat': lat,
        'cat': '',
        'page': '1',
        'order': '1',
        'ondoor': '0',
        'type': 'nine'


    }
    cats = ['街道办', "居委会", '入学']
    for cat in cats:
        param['cat'] = cat
        url = "http://llzg.com/llzgmri/m/p/business/list?" + urllib.parse.urlencode(param)

        r = urllib.request.urlopen(url)
        rlt = json.loads(r.read().decode('UTF-8'))
        try:
            for merchant in rlt['business']:
                insertSql = '''INSERT INTO ehdc.merchant_llzg
                            (city_id,
                             NAME,
                             phone,
                             area_name,
                             location,
                             description,
                             url,
                             LONGITUDE,
                             LATITUDE,
                             source_id,
                             service,
                             display_name,logo,COMMUNITY_ID)
                VALUES ('',
                        '{}',
                        '{}',
                        '',
                        '{}',
                        '',
                        '{}',
                        '{}',
                        '{}',
                        '',
                        '{}',
                        '{}',
                        '{}',
                        '{}');'''.format(merchant['business_name'],
                                         merchant['phone_number'],
                                         merchant['address'],
                                         '', merchant['lat'],
                                         merchant['long'], merchant['sub_title'], param['cat'], merchant['logo'],
                                         COMMUNITY_ID)
                dao.execute_dmls(insertSql)
        except:
            pass


if __name__ == '__main__':
    querySql = 'SELECT a.name ,a.COMMUNITY_ID ,b.LATITUDE,b.LONGITUDE FROM  shengchan_20140815.communities a ,shengchan_20140815.community_poses b WHERE a.COMMUNITY_ID =b.COMMUNITY_ID AND a.AREA_ID <11 AND a.AREA_ID > 0 '
    dao = Dao()
    result = dao.execute_query(querySql)
    for name, COMMUNITY_ID, LATITUDE, LONGITUDE in result:
        getmerchants(LATITUDE, LONGITUDE, COMMUNITY_ID)