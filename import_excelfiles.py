# coding=utf-8
# -*- coding: utf-8 -*-
__author__ = 'wuhan'

import os
import csv
import StrUtil
from DAO import Dao


filepath = "D:\\用户目录\\我的文档\\Tencent Files\\71913596\\FileRecv\\小区行政区街道A"
file_list = os.listdir(filepath)
for file in file_list:
    file = filepath + "\\" + file
    with open(file) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        body = next(f_csv)
        community_name=''
        community_area=''
        community_street=''
        community_sc=''
        for i in range(0,len(headers)):
            if headers[i] =="区":
                community_area=body[i]
            if headers[i] =="街道":
                community_street=body[i]
            if headers[i] =="社区":
                community_sc=body[i]
            if headers[i] =="小区":
                community_name=body[i]
        try:
            insertSQL = "INSERT INTO ehdc.shenzhen_community_to_street    (community_name, community_area, community_street, community_sc) VALUES ('{}', '{}', '{}', '{}');".format(community_name, community_area, community_street, community_sc)
            dao = Dao()
            dao.execute_dmls(insertSQL)
        except:
            pass


