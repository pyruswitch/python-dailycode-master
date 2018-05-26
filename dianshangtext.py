
from openpyxl import Workbook
import urllib
from pyquery import PyQuery as Pq
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time
import StrUtil

driver=webdriver.Chrome("D:/chromedriver")
driver.get("http://www.yiguo.com/products/01_channelhome.html ")
top = driver.find_element_by_css_selector("#body > div.w > div.header.clearfix")
#定位元素要移动到的目标位置
#down =  driver.find_element_by_xpath('''//*[@id="body"]/div[1]/div[5]/div[5]/ul/li[53]/div[2]/div[2]/span/strong''')
js="var q=document.documentElement.scrollTop="
driver.execute_script(js)
time.sleep(3)
#执行元素的移动操作
#ActionChains(driver).drag_and_drop(,top, down).perform()
for i in range(1,50):
 target=("#body > div.w > div.wrap > div.goods_list.clearfix > ul > li:nth-child({}) > div.p_info.clearfix > div.p_name > a").format(i)
 fruitname=driver.find_element_by_css_selector(target).text
 print(fruitname)

