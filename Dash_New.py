from dash import Dash, html, dcc
import csv
import pandas as pd
import numpy as np
import plotly.express as px

app = Dash(__name__)

colors = {
    'background': '#434648',
    'text': '#FFFFFF'
}

#資料處理以便後續畫圖的處理
path = ['../data_source/test.csv', '../data_source/heatmap.csv', '../data_source/linechart.csv']
df = pd.read_csv(path[0], encoding='utf-8')
length = len(df)
df2 = pd.read_csv(path[1])
df3 = pd.read_csv(path[2])

# RoadNameArr = [df["RoadName"][0]]
# index = 0
# SameName = 0
# for i in range(length):
#     for j in range(index):
#         if RoadNameArr[j] != df["RoadName"][i]:
#             SameName = 0
#         else:
#             SameName = 1
#     if SameName == 0 :
#         RoadNameArr.append(df["RoadName"][i])

# LenOfRoadName = len(RoadNameArr)
# TotalFlowArr = [0]*LenOfRoadName
# BigFlowArr = [0]*LenOfRoadName
# CarFlowArr = [0]*LenOfRoadName
# MotorFlowArr = [0]*LenOfRoadName

# for i in range(length):
#     for j in range(LenOfRoadName):
#         if df["RoadName"][i] == RoadNameArr[j]:
#             BigFlowArr[j] += df["BIGVOLUME"][i]
#             CarFlowArr[j] += df["CARVOLUME"][i]
#             MotorFlowArr[j] += df["MOTORVOLUME"][i]
#             break

# for i in range(LenOfRoadName):
#         TotalFlowArr[i] = df["BIGVOLUME"][i] + df["CARVOLUME"][i] + df["MOTORVOLUME"][i]


#Bubble Map
map_fig = px.scatter_mapbox(
                            df, 
                            lat=df["PositionLat"], 
                            lon=df["PositionLon"],
                            color=(df["BIGVOLUME"]+df["CARVOLUME"]+df["MOTORVOLUME"]), 
                            hover_name=df["RoadName"],
                            size=(df["BIGVOLUME"]+df["CARVOLUME"]+df["MOTORVOLUME"]), 
                            zoom=13
                        )
map_fig.update_layout(mapbox_style='open-street-map')
map_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    geo = dict(
            scope='asia',
            center = dict(lat = 25, lon = 121.53),
            projection_scale = 100,
            showland = True
        )
)

#Bar charts

FLOW_COUNT = [0,0,0,0]

len = df["BIGVOLUME"].size
for i in range(len):
    if (df["BIGVOLUME"][i]+df["CARVOLUME"][i]+df["MOTORVOLUME"][i]) > 45 :
        FLOW_COUNT[3] += 1
    elif (df["BIGVOLUME"][i]+df["CARVOLUME"][i]+df["MOTORVOLUME"][i]) > 30 :
        FLOW_COUNT[2] += 1
    elif (df["BIGVOLUME"][i]+df["CARVOLUME"][i]+df["MOTORVOLUME"][i]) >  15:
        FLOW_COUNT[1] += 1
    else :
        FLOW_COUNT[0] += 1

DataOfBar = {'CLASS':["0~15", "16~30", "31~45", "46以上"], 'FLOW':FLOW_COUNT}
Totalflow = pd.DataFrame(DataOfBar)

carflow_fig = px.bar(Totalflow, y=Totalflow["CLASS"], x=Totalflow["FLOW"], orientation='h')
carflow_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#Pie charts
EACHCAR = [0,0,0] #big,car,motor

for i in range(len):
    EACHCAR[0] += df["BIGVOLUME"][i]
    EACHCAR[1] += df["CARVOLUME"][i]
    EACHCAR[2] += df["MOTORVOLUME"][i]

DataOfPie = {'CLASS':["大車", "汽車", "機車"], 'FLOW':EACHCAR}
ThreeCar = pd.DataFrame(DataOfPie)

ThreeCar_fig = px.pie(ThreeCar, names=ThreeCar["CLASS"], values=ThreeCar["FLOW"])
ThreeCar_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#Line charts
AvgSpeed_fig = px.line(df, x=df["InfoData"], y=df["AVGSPEED"] )
AvgSpeed_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#Heatmap
heatmap = px.imshow(df2,
                labels=dict(x="Time of Day", y="Day of Week", color="Productivity"),
                y=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                x=['Morning', 'Afternoon', 'Evening'],
               )
heatmap.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#Line Chart
linechart = px.line(df3)
linechart.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div([
    html.Div(children=[
        html.H1(children='DashBoard',style={'textAlign': 'center','color': '#111111'}),
        # html.Label('跳轉頁面'),
        dcc.Dropdown([
                        'Page1 動畫',
                        'Page2 互動圖表'
                    ],'Page2 互動圖表')   
    ]),
    html.Div(children=[dcc.Graph(id='Bubble Map',figure=map_fig)],style={'width':'40%', 'display': 'inline-block', 'flaot': 'left', 'height': '100%'}),
    html.Div(children=[dcc.Graph(id='Bar Chart',figure=carflow_fig)],style={'width': '30%' ,'display': 'inline-block', 'height': '20%'}),
    html.Div(children=[dcc.Graph(id="Heatmap",figure=heatmap)],style={'width': '30%', 'display': 'inline-block', 'height': '40%'}),
    html.Div(children=[dcc.Graph(id='Line Chart',figure=linechart)],style={'width': '70%', 'display': 'inline-block', 'height': '40%'}),
    html.Div(children=[dcc.Graph(id='Pie Chart',figure=ThreeCar_fig)],style={'width': '30%', 'display': 'inline-block', 'height': '40%'})
])

#更新html
if __name__ == '__main__':
    app.run_server(debug=True)
