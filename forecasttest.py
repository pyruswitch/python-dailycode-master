__author__ = 'vincent'
import pandas as pd
#参数初始化
discfile = 'H:/upupup/电商后台/自动化统计/订餐计划/test.xlsx'
forecastnum = 5

#读取数据，指定日期列为指标，Pandas自动将“日期”列识别为Datetime格式
data = pd.read_excel(discfile, index_col = u'日期')

#时序图
import matplotlib.pyplot as plt

#用来正常显示中文标签

plt.rcParams['font.sans-serif'] = ['SimHei']


#用来正常显示负号

plt.rcParams['axes.unicode_minus'] = False
data.plot()
plt.show()

#自相关图
#from statsmodels.graphics.tsaplots import plot_acf
#plot_acf(data).show()