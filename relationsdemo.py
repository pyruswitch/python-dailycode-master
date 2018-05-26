#-*- coding: utf-8 -*-
__author__ = 'vincent'
import pandas as pd



path=r"H:\upupup\功课\Python\binary.xlsx"
data=pd.read_excel(path)
data.columns = ["admit", "gre", "gpa", "prestige"]
result=data.corr(u'admit')
print(result)