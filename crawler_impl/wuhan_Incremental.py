# coding=utf-8
# -*- coding: utf-8 -*-
__author__ = 'wuhan'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("E://chromedriver.exe")
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

