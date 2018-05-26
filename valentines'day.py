__author__ = 'deer'
#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
plt.figure(figsize=(6,6))

X = np.arange(-5.0, 5.0, 0.1)
Y = np.arange(-5.0, 5.0, 0.1)

x, y = np.meshgrid(X, Y)
f = 17 * x ** 2 - 16 * np.abs(x) * y + 17 * y ** 2 - 225

fig = plt.figure()
cs = plt.contour(x, y, f,0, colors = 'r')
plt.text(-2.2,1.9,u'尖尖儿：', fontproperties=font)
plt.text(-1.4,1.2,u'我秘秘密密地告诉你', fontproperties=font)
plt.text(-1.4,0.7,u'你不要告诉人家', fontproperties=font)
plt.text(-1.4,0.2,u'我是很爱很爱你的', fontproperties=font)
plt.text(0.8,-0.7,u'---爱你的俊美', fontproperties=font)
plt.show()
