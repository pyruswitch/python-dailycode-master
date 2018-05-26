__author__ = 'Administrator'
# -*- coding:utf-8 -*-
import urllib
import json
import time
import  http.cookiejar

loginUrl = 'http://as-vip.missfresh.cn/v3/product/category/jsd-hn-snack?platform=ios&version=3.0.5'
headers = {
'Content-Type': 'application/json ',
'User-Agent': 'NewMissFresh/3.0.5 (iPhone; iOS 9.2; Scale/2.00)',
'Host': 'as-vip.missfresh.cn',
'Connection': 'Keep-Alive',
'Accept-Encoding': 'gzip, deflate',
'Content-Length': '207',
}
#loginData = 'http://api.1mxian.com/v5/category_list?category_id=15&coord_system=BD-09&latitude=22.53713817157729&longitude=113.9510510252698&poi_id=bd-a8d713c272264d95a8f729bb&refer_from=APP_IOS_2.1.0'
cookieJar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
req = urllib.request.Request(url=loginUrl, headers=headers)
loginResult = opener.open(req).read()
print( str(loginResult))