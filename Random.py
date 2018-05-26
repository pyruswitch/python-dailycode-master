__author__ = 'Administrator'

import string

count=0
list1=["A","B"]
list2=["A","B","C","D"]
list3=["A","B","C"]
list4=["A","B","C"]
list5=["A","B","C"]
for i in list1:
   for j in list2:
       for k in list3:
           for l in list4:
               for m in list5:
                   count=count+1
                   testresult=i+j+k+l+m
                   print(testresult)
print(count)