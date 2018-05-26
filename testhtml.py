__author__ = 'Administrator'
__author__ = 'Naxer'
# -*- coding:utf-8 -*-
from openpyxl import Workbook
import urllib
from pyquery import PyQuery as Pq
from selenium import webdriver
import time
import StrUtil


'''baseurl="http://www.egu365.com/search/list.jsp?page_type=2&egu=ci-0201000000&s_input=&pageno=1"
#目标网站URL
driver=webdriver.Chrome("D://chromedriver.exe")
driver.get(baseurl)'''


def a(list):
    str_list = ""
    for i in list:
       try:
           i + 1
       except TypeError:
            str_list =str_list+","+ "'"+ str(i)+ "'"
       else:
           str_list = str_list+str(i)+ ","
    str_list = "[" + str_list + "]"
    return str_list
def b():
    list1= ["周一", "周二", "周三", "周四", "周五", "周六"]

    list2=[5, 20, 36, 10, 10, 20]
    strtest="测试字符串拼接"+a(list1)
    print(strtest)

if __name__ == '__main__':
    b()