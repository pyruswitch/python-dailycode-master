import http.client as hc
import http.cookiejar
import urllib
from DAO import Dao

from pyquery import PyQuery as Pq
#
# for i in range(1, 300):
# url = "www.dianping.com"
#     client = hc.HTTPConnection(url)
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
#     client.request("GET", "/search/map/category/{}/0".format(i), headers=headers)
#     cookieStr = client.getresponse().getheader("Set-Cookie")
#     cityenname = cookieStr[cookieStr.index("cye=") + 4:-1]
#     cityId = cookieStr[cookieStr.index("cy=") + 3:-1]
#     cityId = cityId[0:cityId.index(";")]
#     cityenname = cityenname[0:cityenname.index(";")]
#     if cityenname is not None:
#         insert_sql = "INSERT INTO dianping_cities (cityId,cityenname) VALUES ({},'{}')".format(cityId,cityenname)
#         dao = Dao()
#         dao.execute_dmls( insert_sql )
#
# test_html= '''
# <table width="100%" cellspacing="0" border="1" cellpadding="0" align="center" bordercolorlight="#2E5AB6" bordercolordark="#FFFFff" bgcolor="#F4F6FB">
#   <tbody><tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center"><font color="000000">售房单位</font></div></td>
#     <td width="35%">南京浙商投资有限公司</td>
#     <td width="20%" bgcolor="B9C8E8"><div align="center">编号</div></td>
#     <td width="20%">2015200016</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">房屋坐落地点</div></td>
#     <td colspan="3">江宁区秣陵街道天元东路388号</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">项目名称</div></td>
#     <td colspan="3"><a href="http://newhouse.njhouse.com.cn/detail.php?prjid=107090" target="_blank"><font color="red">南京义乌小商品城</font></a></td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">开盘时间</div></td>
#     <td colspan="3">2015-02-13</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">房屋用途性质</div></td>
#     <td colspan="3">商业</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">土地使用证号</div></td>
#     <td colspan="3">宁江国用2010第06163号</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">工程规划许可证号</div></td>
#     <td colspan="3"></td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">土地使用年限</div></td>
#     <td colspan="3">自2003-11-04起,至2043-11-03止&nbsp;&nbsp;&nbsp;&nbsp;共40年</td>
#   </tr>
#   <tr>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">区属</div></td>
#     <td width="25%">江宁区</td>
#     <td width="25%" bgcolor="B9C8E8"><div align="center">预售类别</div></td>
#     <td width="25%"></td>
#   </tr>
# </tbody></table>
# '''
# doc = Pq(test_html)
# print(Pq(doc("tr:eq(0)"))("td:eq(1)").text())
# _community_detail={}
# _community_detail['location']  = Pq(doc("tr:eq(1)"))("td:eq(1)").text()
# _community_detail['name']  =  Pq(doc("tr:eq(2)"))("a").text()
# _community_detail['url']  =   Pq(doc("tr:eq(2)"))("a").attr("href")
# _community_detail['area_name']  =  Pq(doc("tr:eq(8)"))("td:eq(1)").text()
# print(_community_detail)

test_str = "http://www.njhouse.com.cn/spf/inf/index3.php?prjid=108510&buildid=20092546&dm=3%B4%B1&Program=LDFcputRVrdJSySqfAcckJHGrGUTHu"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
request = urllib.request.Request(url=test_str, headers=headers)
m_fp = urllib.request.urlopen(request, timeout=1500)
html_str_uncode = m_fp.read()
m_fp.close()
doc = Pq(html_str_uncode)
a_list = doc("tr.text>td>a")
for a in a_list:
    print(doc(a).text())


    # request = urllib.request.Request("http://www.dianping.com/search/map/category/1/0")
    # m_fp = urllib.request.urlopen(request, timeout=500)
    # print(m_fp)