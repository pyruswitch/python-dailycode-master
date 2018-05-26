__author__ = 'vincent'
import jieba
from operator import itemgetter
from math import log
import os
import os.path
import jieba.posseg as pseg


rootdir=r"H:\upupup\电商后台\主题挖掘\文本挖掘\林夕"
TF={}
IDF={}
count=0.0
i=0
countwords=0
for root,dirs, filenames in os.walk(rootdir):
    for filename in filenames:
        i=i+1
        filepath=r"H:/upupup/电商后台/主题挖掘/文本挖掘/林夕/{}".format(filename)
        nowdic={}
        sumwords=0

        try :
            with open(filepath) as fr:
                for line in fr.readlines():
                    line =line.strip()
                    lis =list(pseg.cut(line))
                    sumwords+=float(len(lis))
                    countwords+=float(len(lis))
                    for li in lis:
                        a=li.flag

                        if len(li.word)<=1:
                            continue
                        li=str(li)
                        if li not in IDF.keys():
                                IDF[li]=[i]
                        else:
                                IDF[li].append(i)
                        if li not in nowdic.keys():
                                nowdic[li]=1.0
                        else:
                                nowdic[li]+=1.0
                count +=1.0
                if sumwords >0.0:
                    for key in nowdic.keys():
                        nowdic[key]=float(nowdic[key]/sumwords)
                        if key not in TF.keys():
                            TF[key]=nowdic[key]
                        else:
                            TF[key ]+=nowdic[key]
        except IOError as err:
            pass
    wordnum={}
    worddocnum={}
    for key in IDF.keys():
        numDoc=float(len(set(IDF[key])))
        num=int(len(IDF[key]))
        wordnum[key]=num
        worddocnum[key]=numDoc
        IDF[key]=[log(count/(numDoc+1.0))]
    TF_IDF=TF
    for key in TF_IDF.keys():
        TF_IDF[key]=float(TF_IDF[key]*TF[key])
    print(len(TF))
    print(sumwords)
    print(countwords)
    sortedDic =sorted(TF_IDF.items(),key=itemgetter(1),reverse=True)
    i=0
    fw=open("H:/upupup/电商后台/主题挖掘/文本挖掘/林夕TFIDF.txt","w+")
    for key in sortedDic:

        fw.write(str(key[0])+' '+str(wordnum[key[0]])+' '+str(worddocnum[key[0]])+' '+str(key[1])+'\r\n')
        i +=1
        if i>=40:
            continue
        print(key[0],key[1])
    fw.close()



