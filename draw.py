import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.font_manager
 
# a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
 
# for i in a:
#     print(i)

plt.rcParams['agg.path.chunksize'] = 10000
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
path = '../201801/vdtrafonetab_info_001.csv'
df = pd.read_csv(path, header= None, encoding='utf-8')
print(df[:3])
RoadID = df[4] #道路路名碼
RoadName = df[5] #道路名稱
BIGVOLUME = df[8] #大車的流量
BIGSPEED = df[9] #大車的速率
CARVOLUME = df[10] #汽車的流量
CARSPEED = df[11] #汽車的速率
MOTORVOLUME = df[12] #機車的流量
MOTORSPEED = df[13] #機車的速率
FREESPD = df[22] #速限
fig = plt.figure(figsize=(50,9))
plt.plot(RoadName, CARVOLUME)
plt.tick_params(axis='x', labelsize=8)
plt.xticks(rotation=-20) 
plt.xlabel("道路名稱")
plt.ylabel("流量") 
plt.title("2018年1月汽車流量")
# plt.grid(True)
plt.show()