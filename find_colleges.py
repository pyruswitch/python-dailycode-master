__author__ = 'Administrator'
import urllib

from pyquery import PyQuery as Pq
from DAO import Dao


def get_page_content_str(url):
    try:
        print("现在开始抓取" + url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        request = urllib.request.Request(url=url, headers=headers)
        m_fp = urllib.request.urlopen(request, timeout=500)
        html_str = m_fp.read().decode('gb2312')
        m_fp.close()
        return html_str
    except urllib.error.URLError as err:
        print(err)
        return None
    except Exception  as err:
        print(err)
        return None


def craw(url):
    html = get_page_content_str(url)
    doc = Pq(html)
    td_list = doc("td.FONT")
    for td in td_list:
        school_list = td
        for school in school_list:
            print(school)


for i in range(1, 34):
    if i < 10:
        url = "http://www.huaue.com/gx0{}.htm".format(i)
    else:
        url = "http://www.huaue.com/gx{}.htm".format(i)
    craw(url)
