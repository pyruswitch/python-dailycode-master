__author__ = 'Administrator'
# -*- coding:utf-8 -*-
from openpyxl import Workbook
import urllib
import StrUtil
from pyquery import PyQuery as Pq
from selenium import webdriver
import time
import StrUtil
import string


'''url="http://news.163.com/16/0615/12/BPJOV7HL00014AED.html"
word="永佳天成"
word=word.encode("utf-8")
word=str(word)
word=StrUtil.substr(word,"b'","'")
word=word.replace(r"","%")
baseurl="http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs="
sufurl="&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word="
#url=baseurl+str(word)+sufurl+str(word)
print(url)
print("现在开始抓取" + url)
try:
 headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
 #伪装浏览器
 request = urllib.request.Request(url=url, headers=headers)
            #构造请求
 m_fp = urllib.request.urlopen(request, timeout=500)
 #访问网站获取源码
 html_str = m_fp.read().decode('utf-8')
 #读取源码，该网站使用的编码方式是utf-8
except Exception:
            print(Exception)
            try:
                  request = urllib.request.Request(url=url, headers=headers)
                  #构造请求
                  m_fp = urllib.request.urlopen(request, timeout=500)
                  html_str= m_fp.read().decode('gb2312')
            except Exception:
                  print(Exception)
                  try:
                        request = urllib.request.Request(url=url, headers=headers)
                        #构造请求
                        m_fp = urllib.request.urlopen(request, timeout=500)
                        html_str= m_fp.read().decode('gbk')
                  except Exception:
                      print(Exception)
            m_fp.close()
print(html_str)'''

