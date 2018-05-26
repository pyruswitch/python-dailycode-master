__author__ = 'vincent'
import jieba
from operator import itemgetter
from math import log
import os
import os.path
from snownlp import  SnowNLP as snlp
import jieba.posseg as pseg
import nltk



str=snlp('''
我今天很开心

''')
#print(str.words)
#print(str.tags)
print(str.sentiments)
