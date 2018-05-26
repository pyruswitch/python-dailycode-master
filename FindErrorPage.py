# -*- coding: utf-8 -*-
__author__ = 'wuhan'

import http.client as hc
import http.cookiejar
import urllib
from DAO import Dao
from pyquery import PyQuery as Pq

dao = Dao()
querySql = "SELECT COMMUNITY_ID,ORIGINAL_URL ,(SELECT COUNT(DISTINCT BUILDING_NUM )FROM apartments WHERE apartments.`COMMUNITY_ID` = communities.`COMMUNITY_ID` ) FROM communities WHERE STATUS = -1 AND SOURCE_ID = 19"
result = dao.execute_query(querySql)
for communityId, url, count in result:
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    request = urllib.request.Request(url=url, headers=headers)
    m_fp = urllib.request.urlopen(request, timeout=500)
    try:
        html = m_fp.read().decode('gb2312')
    except Exception as e :
        print(e)
        print(url + "出错了")
        continue
    pq = Pq(html)
    li = pq("div.st_tree>ul>li")
    pagecount = len(li)
    # for i in li:
    #     pagecount = pagecount + 1
    if (pagecount != count):
        updateSql = "update communities set STATUS = -1 WHERE STATUS = 1 AND SOURCE_ID = 19 and COMMUNITY_ID = {}".format(
            communityId)
        dao.execute_dmls(updateSql)
    else :
        updateSql = "update communities set STATUS = 2 WHERE STATUS = 1 AND SOURCE_ID = 19 and COMMUNITY_ID = {}".format(
            communityId)
        dao.execute_dmls(updateSql)
