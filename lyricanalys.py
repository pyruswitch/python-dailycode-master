__author__ = 'vincent'

# -*- coding:utf-8 -*-
import urllib
from pyquery import PyQuery as Pq
import StrUtil
import time
import os



def get_page_content_str( url):
    time.sleep(1)

    try:
            print("现在开始抓取" + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            #伪装浏览器
            request = urllib.request.Request(url=url, headers=headers)
            #构造请求
            m_fp = urllib.request.urlopen(request, timeout=500)
            #访问网站获取源码
            html_str = m_fp.read().decode('utf-8')
            #读取源码，该网站使用的编码方式是utf-8

            return html_str
    except Exception:
            print(Exception)
            try:
                 request = urllib.request.Request(url=url, headers=headers)
                 m_fp = urllib.request.urlopen(request, timeout=500)
                 html_str= m_fp.read().decode('gbk')
                 return html_str
            except Exception:
             print(Exception)
             try:
                 request = urllib.request.Request(url=url, headers=headers)
                 m_fp = urllib.request.urlopen(request, timeout=500)
                 html_str= m_fp.read().decode('gb2312')
                 return html_str
             except Exception:
                      print(Exception)
            m_fp.close()
#定义抓取网页源码函数

baseurl="http://www.xiami.com/search/song/page/{}?spm=a1z1s.3521869.0.0.tdwCN4&key=%E6%9E%97%E5%A4%95&category=-1"
count=0
namelist=[]
for i in range(1,136):
    url=baseurl.format(i)
    print("现在开始抓取第{}页".format(i))
    print(url)

    html_str=get_page_content_str(url)
    doc=Pq(html_str)

    names=doc("#wrapper > div.grey_left.clearfix > div.grey_left_main > div > div.search_result > div.search_result_box > div.result_main > table > tbody > tr")
    for name in names:

        songname=Pq(name)("td.song_name > a").attr("title")
        songname=StrUtil.substr(songname,"'"," (")
        if songname not in namelist:
            if songname=="该艺人演唱的其他版本":
                lyricurl=Pq(name)("td.song_name > a:nth-child(2)").attr("href")
            else:
                lyricurl=Pq(name)("td.song_name > a").attr("href")
                lyricpage=get_page_content_str(lyricurl)
                lyric_page=Pq(lyricpage)
                lyric_str=lyric_page("#lrc > div.lrc_main").text()
                lyric_str=lyric_str.replace(" ","\n")
                if  lyric_str=="":
                    pass
                count=count+1

                path="H:/upupup/电商后台/主题挖掘/文本挖掘/测试/"+songname+".txt"
                try :
                   f=open(path,'w+')
                   f.write(str(lyric_str))
                   f.close()
                   namelist.append(songname)
                   print("完成"+songname+".txt的抓取")

                except Exception:
                          print(Exception)
                          f.close()
                          try :   os.remove(path)
                          except Exception:
                              print(Exception)