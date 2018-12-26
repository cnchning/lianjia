#coding=utf-8
#!/usr/bin/python

import os
import time
import datetime
import sys
from util.logutil import log
import numpy as np
import matplotlib.pyplot as pl
from pylab import mpl

#处理matplotlib 中文显示问题
mpl.rcParams['font.sans-serif'] = ['FangSong']   # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False       # 解决保存图像是负号'-'显示为方块的问题

x = []
y = []
z = []
for i in range(0, 21):
    x.append(i)
    y.append(i/2 if i % 2 == 0 else i+1)
    z.append(i/3+1 if i%3 == 0 else i+2)
print(y)

fig = pl.figure()
axes1 = fig.add_axes([0.1, 0.1, 0.85, 0.85]) #绘图区域范围，显示区域从0-1，0.1 0.1：左下角坐标，0.85 0.85 右上角坐标
axes1.set_title(u'测试', {}, loc='center')
line1 = axes1.plot(x, y, 'rs-', label=u'曲线1')
line2 = axes1.plot(x, z, 'bs-', label=u'曲线2')

axes1.set_ylabel(u'Y轴')
axes1.set_xlabel(u'X轴')
axes1.grid(True)

#设置和显示图例
legend = pl.legend(loc='center', shadow=True, fontsize='x-large')
# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#00FFCC')

pl.show()