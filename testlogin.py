__author__ = 'vincent'

import urllib
import http.cookiejar
from urllib import request
from pyquery import PyQuery as Pq


class Login:
 def redlogin(loginurl):


   cj = http.cookiejar.LWPCookieJar()
   cookie_support = urllib.request.HTTPCookieProcessor(cj)
   opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
   urllib.request.install_opener(opener)
   h=urllib.request.urlopen(loginurl)
   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
   #伪装浏览器
   req = urllib.request.Request(url=loginurl, headers=headers)
   #构造请求
   urllib.request.install_opener(opener)
   m_fp = urllib.request.urlopen(req, timeout=500)
   #访问网站获取源码
   html_str = m_fp.read().decode('utf-8')
   #读取源码，该网站使用的编码方式是utf-8
   doc=Pq(html_str)
   authenticity_token=doc("head > meta:nth-child(8)").attr("content")
   print("authenticity_token=: "+authenticity_token)




   headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                   'Referer': "http://devops.lab.everhomes.com/login",
          }
   values = {"authenticity_token":authenticity_token,
           "username":"vincent",
          "password":"12345678"
   }
   data = urllib.parse.urlencode(values).encode('utf-8')

   req = urllib.request.Request(url=loginurl,
                                       headers=headers,data=data  )
   urllib.request.install_opener(opener)
   m_fp = urllib.request.urlopen(req)

 def get_req(get_url):
     get_req=urllib.request.Request(get_url)
     m_fp = urllib.request.urlopen(get_req)
     html_str = m_fp.read().decode("utf-8")
     return html_str
if __name__ == '__main__':
    ck=Login.redlogin("http://devops.lab.everhomes.com/login")
    #get_req=urllib.request.Request("http://devops.lab.everhomes.com/projects/devops/issues?query_id=54" )
    #m_fp = urllib.request.urlopen(get_req)

    #html_str = m_fp.read().decode("utf-8")
    html_str=Login.get_req("http://devops.lab.everhomes.com/projects/devops/issues?query_id=59")
