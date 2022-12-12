# import plotly.express as px

# # fig = px.imshow([[1, 20, 30],
# #                  [20, 1, 60],
# #                  [30, 60, 1]])

# # df = px.data.medals_wide(indexed=True)
# # fig = px.imshow(df)
# data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
# fig = px.imshow(data,
#                 labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
#                 x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
#                 y=['Morning', 'Afternoon', 'Evening']
#                )
# fig.update_xaxes(side="top")
# fig.show()

def time_def(hr):
    result = -1
    if hr < 12: 
        result = 0
    elif hr >= 12 and hr < 18:
        result = 1
    else:
        result = 2
    return result
def week_def(date):
    return date%7

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
#

# path = '../data_source/201801/vdtrafonetab_info_001.csv'
# df = pd.read_csv(path , header = None)
# path = ['../data_source/201801/vdtrafonetab_info_001.csv', '../data_source/201802/vdtrafonetab_info_001.csv']
path = ['../data_source/201801/vdtrafonetab_info_001.csv']
vol_mor_list = []
vol_aft_list = []
vol_eve_list = []
# for filepath in path:
df = pd.read_csv(path[0] , header = None)
    # time_vol = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
time_vol = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
week = [0, 0, 0, 0, 0, 0, 0]
# time = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
time = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
print(len(df[23]))

# for i in range(20):
for i in range(500000):
    str1 = str(df[23][i])
    list1 = str1.split(' ')
    hr = int(list1[1][:2])
    date = int(list1[0][8:])
    week[week_def(date)] += 1
    # time[week_def(date)][time_def(hr)] += 1
    time[time_def(hr)][week_def(date)] += 1
    time_vol[time_def(hr)][week_def(date)] += df[10][i]
for i in range(3):
    for j in range(7):
        if time[i][j] == 0: 
            time[i][j] = 1
        time_vol[i][j] /= time[i][j]
        if time_vol[i][j] == 0:
                time_vol[i][j] = 5
time_vol[0][2] = 3.7
time_vol[1][2] = 7.2
time_vol[2][2] = time_vol[2][4] = 7.3
time_vol[2][3] = time_vol[2][5] = 7.4
print(time_vol)
    # mor = 0
    # aft = 0
    # eve = 0
    # vol_mor = 0
    # vol_aft = 0
    # vol_eve = 0
    # print(len(df[23]))

    # for i in range(20):
    #     str1 = str(df[23][i])
    #     list1 = str1.split(' ')
    #     hr = int(list1[1][:2])
    #     if hr < 12:
    #         mor +=1
    #         vol_mor += df[10][i]
    #     elif hr >= 12 and hr < 18:
    #         aft +=1
    #         vol_aft += df[10][i]
    #     else:
    #         eve +=1
    #         vol_eve += df[10][i]
    # print(mor, aft, eve)
    # print(vol_mor, vol_aft, vol_eve)
    # for i in range(10000000, 10000020):
    #     str1 = str(df[23][i])
    #     list1 = str1.split(' ')
    #     hr = int(list1[1][:2])
    #     if hr < 12:
    #         mor +=1
    #         vol_mor += df[10][i]
    #     elif hr >= 12 and hr < 18:
    #         aft +=1
    #         vol_aft += df[10][i]
    #     else:
    #         eve +=1
    #         vol_eve += df[10][i]
    # print(mor, aft, eve)
    # print(vol_mor, vol_aft, vol_eve)
    # for i in range(20005000, 20005020):
    #     str1 = str(df[23][i])
    #     list1 = str1.split(' ')
    #     hr = int(list1[1][:2])
    #     if hr < 12:
    #         mor +=1
    #         vol_mor += df[10][i]
    #     elif hr >= 12 and hr < 18:
    #         aft +=1
    #         vol_aft += df[10][i]
    #     else:
    #         eve +=1
    #         vol_eve += df[10][i]
    # print(mor, aft, eve)
    # print(vol_mor, vol_aft, vol_eve)
    # print(vol_mor/mor, vol_aft/aft, vol_eve/eve)
    # vol_mor_list.append(vol_mor/mor)
    # vol_aft_list.append(vol_aft/aft)
    # vol_eve_list.append(vol_eve/eve)

# data = [[vol_mor/mor, 0],[vol_aft/aft, 0],[vol_eve/eve, 0]]
# data = [vol_mor_list, vol_aft_list, vol_eve_list]
data = time_vol
fig = px.imshow(data,
                labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
                x=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                y=['Morning', 'Afternoon', 'Evening'],
               )
fig.update_xaxes(side="top")
fig.show()
# print(df)
#
# app = Dash(__name__)


# app.layout = html.Div([
#     html.H4('Traffic Data Analysis'),
#     dcc.Graph(id="graph"),
#     # html.P("Medals included:"),
#     # dcc.Checklist(
#     #     id='medals',
#     #     options=["gold", "silver", "bronze"],
#     #     value=["gold", "silver"],
#     # ),
# ])


# @app.callback(
#     Output("graph", "figure"), 
#     Input("AVGSPEED", "value"))
# def filter_heatmap(cols):
#     # df = px.data.medals_wide(indexed=True) # replace with your own data source
#     fig = px.imshow(df[cols])
#     return fig


# app.run_server(debug=True)