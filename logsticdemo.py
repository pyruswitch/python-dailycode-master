__author__ = 'vincent'
import  pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
import copy

df=pd.read_excel(r"H:\upupup\电商后台\主题挖掘\商品\饮品\binary.xlsx")
print (df.head())

df.columns =["admit","gre","gpa","prestige"]
print (df.columns)
print (df.describe())
print(df.std())
print(pd.crosstab(df['admit'],df['prestige'],rownames=['admit']))
df.hist()
#pl.show()
dummy_ranks=pd.get_dummies(df['prestige'],prefix='prestige')
print(dummy_ranks.head())
cols_to_keep=['admit','gre','gpa']
data=df[cols_to_keep].join(dummy_ranks.ix[:,'prestige_2':])
print (data.head())
data['intercept']=1.0
train_cols=data.columns[1:]

logit=sm.Logit(data['admit'],data[train_cols])
result=logit.fit()

combos=copy.deepcopy(data)
predict_cols=combos.columns[1:]
combos['intercept']=1.0
combos['predict']=result.predict(combos[predict_cols])

total =0
hit=0
for value in combos.values:
    predict=value[-1]
    admit =int(value[0])
    if predict>0.5:
        total +=1
        if admit ==1:
            hit+=1
print("total:"+str(total) +",hit:"+str(hit) +",precision:"+"%.2f%%"%((hit/total)*100))

print (result.summary())