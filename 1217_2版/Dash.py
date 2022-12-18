from dash import Dash, html, dcc
import csv
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
import json

#function Defination
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

app = Dash(__name__)

colors = {
    'background': '#434648',
    'text': '#FFFFFF'
}



#資料處理以便後續畫圖的處理
path = './test.csv'
df = pd.read_csv(path, encoding='utf-8')
LenOfdf= len(df)

#Bubble Map 資料處理
date_list = []
RoadName_list = []
PositionLon_list = []
PositionLat_list = []
for i in range(LenOfdf):
    str1 = str(df["InfoData"][i])
    date = int(str1[8:])    
    if date not in date_list:
        date_list.append(date)
    if df["RoadName"][i] not in RoadName_list:
        RoadName_list.append(df["RoadName"][i])
        PositionLon_list.append(df["PositionLon"][i])
        PositionLat_list.append(df["PositionLat"][i])

date_list = sorted(date_list)
legth_date = len(date_list)
lenOfRoad = len(RoadName_list)
Road_Data = np.zeros((lenOfRoad, legth_date))

for i in range(LenOfdf):
    str1 = str(df["InfoData"][i])
    date = int(str1[8:])    
    row = date_list.index(date)
    col = RoadName_list.index(df["RoadName"][i])
    Road_Data[col][row] += (df["BIGVOLUME"][i]+df["CARVOLUME"][i]+df["MOTORVOLUME"][i])

Total = [0] * lenOfRoad
for i in range(lenOfRoad):
    Total[i] = sum(Road_Data[i])

Color_list = ["BLUE"] * lenOfRoad
range_str = [""] * 5
interval = max(Total)/4
# interval_list = [interval, interval*2, interval*3, interval*4]
interval_list = [100000, 200000, 300000, 400000]
range_str[0] = "< {}".format(interval_list[0])
range_str[1] = "{} to {}".format(interval_list[0]+1,interval_list[1])
range_str[2] = '{} to {}'.format(interval_list[1]+1,interval_list[2])
range_str[3] = '{} to {}'.format(interval_list[2]+1,interval_list[3])
range_str[4] = '> {}'.format(interval_list[3]+1)

Label_list = [range_str[0]] * lenOfRoad
for i in range(lenOfRoad):
    if Total[i] > interval_list[3]:
        Color_list[i] = "RED"
        Label_list[i] = range_str[4]
    elif Total[i] > interval_list[2] :
        Color_list[i] = "ORANGE"
        Label_list[i] = range_str[3]
    elif Total[i] > interval_list[1]:
        Color_list[i] = "YELLOW"
        Label_list[i] = range_str[2]
    elif Total[i]  > interval_list[0]:
        Color_list[i] = "GREEN"
        Label_list[i] = range_str[1]


DataOfBM = pd.DataFrame({
                            'PositionLon': PositionLon_list, 
                            'PositionLat':PositionLat_list, 
                            'RoadName': RoadName_list, 
                            'Total_Vol': Total, 
                            'Color': Color_list, 
                            'Range': Label_list
                        })
DataOfBM2 = pd.DataFrame(Road_Data, columns= date_list)
TotalVolume = pd.concat([DataOfBM, DataOfBM2], axis=1)

#Bubble Map
map_fig = px.scatter_mapbox(
                                TotalVolume, 
                                labels= dict(color="Total Volume"),
                                lat=TotalVolume["PositionLat"], 
                                lon=TotalVolume["PositionLon"],
                                color= TotalVolume["Range"],
                                hover_name=TotalVolume["RoadName"],
                                size= TotalVolume["Total_Vol"],
                                zoom=10,
                                color_discrete_map={
                                    range_str[0]: "blue",
                                    range_str[1]: "green",
                                    range_str[2]: "yellow",
                                    range_str[3]: "orange",
                                    range_str[4]: "red"
                                }
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
              ),
    title= 'Taiwan Map',
    hovermode= 'closest'
)

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H1("DashBoard",style={'textAlign': 'center','color': '#111111'}),
            # dcc.Dropdown([
            #                 'Page1 動畫',
            #                 'Page2 互動圖表'
            #             ],'Page2 互動圖表'),
        ]
    ),
    html.Div(dcc.Graph(id='Bubble Map', figure=map_fig),style={'width': '45%' ,'display': 'inline-block', 'height': '100%'}),
    html.Div(dcc.Graph(id='Bar Chart'),style={'width': '30%' ,'display': 'inline-block'}),
    html.Div(dcc.Graph(id="Heap Map"),style={'width': '25%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='Line Chart'),style={'width': '70%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='Pie Chart'),style={'width': '30%', 'display': 'inline-block'})
])

#Bar Chart callback function
@app.callback( Output('Bar Chart', 'figure'),
               Input('Bubble Map', 'selectedData') )
def draw_BarChart(selectedData):
    FLOW_COUNT = [0] * 5
    if selectedData is None: #Default
        FLOW_COUNT[0] = Color_list.count("BLUE")
        FLOW_COUNT[1] = Color_list.count("GREEN")
        FLOW_COUNT[2] = Color_list.count("YELLOW")
        FLOW_COUNT[3] = Color_list.count("ORANGE")
        FLOW_COUNT[4] = Color_list.count("RED")
    else: 
        length_SD = len(selectedData["points"])
        for i in range(length_SD):
            if selectedData["points"][i]["marker.size"] > interval_list[3]:
                FLOW_COUNT[4] += 1
            elif selectedData["points"][i]["marker.size"] > interval_list[2] :
                FLOW_COUNT[3] += 1
            elif selectedData["points"][i]["marker.size"] > interval_list[1]:
                FLOW_COUNT[2] += 1
            elif selectedData["points"][i]["marker.size"]  > interval_list[0]:
                FLOW_COUNT[1] += 1
            else:
                FLOW_COUNT[0] += 1
    DataOfBar = {'COLOR':["BLUE", "GREEN", "YELLOW", "ORANGE", "RED"], 'QUANTITY':FLOW_COUNT}
    Totalflow = pd.DataFrame(DataOfBar)
    barchart = px.bar(
                            Totalflow,
                            labels= dict(x="Traffic Volume", y="COLOR LABEL"),
                            y=Totalflow["COLOR"],
                            x=Totalflow["QUANTITY"],
                            color = Totalflow["COLOR"],
                            color_discrete_map={
                                "BLUE": "blue",
                                "GREEN": "green",
                                "YELLOW": "yellow",
                                "ORANGE": "orange",
                                "RED": "red"
                            }
                        )
    barchart.update_layout(
                                plot_bgcolor=colors['background'],
                                paper_bgcolor=colors['background'],
                                font_color=colors['text'],
                                title= 'The Quantity Of Each Color Bubble',
                                hovermode= 'closest'
                            )
    return barchart

#function： 取得RoadName的list
def get_roadname(lon, lat):
    for i in range(len(TotalVolume)):
        if (TotalVolume["PositionLon"][i] == lon and TotalVolume["PositionLat"][i] == lat):
            Road = TotalVolume["RoadName"][i]
            return Road
    return None

#Heap Map callback function
@app.callback( Output('Heap Map', 'figure'),
               Input('Bubble Map', 'selectedData') )
def draw_HeapMap(selectedData):
    DataOfHM = np.zeros((7, 3))
    TargetRoadName = []
    if selectedData is None:
        for i in range(LenOfdf):
            str1 = str(df["InfoTime"][i])
            list1 = str1.split(' ')
            hr = int(list1[1][:2])      #只取小時，其他忽略
            date = int(list1[0][8:])    #只取日期，年月忽略
            DataOfHM[week_def(date)][time_def(hr)] += ( df["BIGVOLUME"][i] + df["CARVOLUME"][i] + df["MOTORVOLUME"][i] )
    else: 
        length_SD = len(selectedData["points"])
        for i in range(length_SD):
                TargetRoadName.append(get_roadname(selectedData["points"][i]["lon"], selectedData["points"][i]["lat"]))
        for i in range(LenOfdf):
            if df["RoadName"][i] in TargetRoadName:
                str1 = str(df["InfoTime"][i])
                list1 = str1.split(' ')
                hr = int(list1[1][:2])      #只取小時，其他忽略
                date = int(list1[0][8:])    #只取日期，年月忽略
                DataOfHM[week_def(date)][time_def(hr)] += ( df["BIGVOLUME"][i] + df["CARVOLUME"][i] + df["MOTORVOLUME"][i] )
    heatmap = px.imshow(
                        DataOfHM,
                        labels=dict(x="Time of Day", y="Day of Week", color="Total Volume"),
                        y=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                        x=['Morning', 'Afternoon', 'Evening'],
                        color_continuous_scale=["blue", "green", "yellow", "orange", "red"]
                    )
    heatmap.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title= 'The Total Volume Of Each Week(3 Time Period)',
        hovermode= 'closest'
    )
    return heatmap

#Pie Chart callback function
@app.callback( Output('Pie Chart', 'figure'),
               Input('Bubble Map', 'selectedData') )
def draw_PieChart(selectedData):
    EACHCAR = [0,0,0] #big,car,motor
    TargetRoadName = []
    if selectedData is None:
        for i in range(LenOfdf):
            EACHCAR[0] += df["BIGVOLUME"][i]
            EACHCAR[1] += df["CARVOLUME"][i]
            EACHCAR[2] += df["MOTORVOLUME"][i]
    else: 
        length_SD = len(selectedData["points"])
        for i in range(length_SD):
                TargetRoadName.append(get_roadname(selectedData["points"][i]["lon"], selectedData["points"][i]["lat"]))
        for i in range(LenOfdf):
            if df["RoadName"][i] in TargetRoadName:
                EACHCAR[0] += df["BIGVOLUME"][i]
                EACHCAR[1] += df["CARVOLUME"][i]
                EACHCAR[2] += df["MOTORVOLUME"][i]
    DataOfPie = pd.DataFrame({'CLASS':["Big", "Car", "Motor"], 'FLOW':EACHCAR})
    piechart = px.pie(
                        DataOfPie, 
                        names= DataOfPie["CLASS"], 
                        values= DataOfPie["FLOW"],
                        color= DataOfPie["CLASS"],
                        color_discrete_map={
                            "Big": "#afbc8f",
                            "Car": "#e7d292",
                            "Motor": "#e5a952"
                        }
                    )
    piechart.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title= 'Proportion Of Cars In January',
        hovermode= 'closest'
    )
    return piechart

#Line Chart callback function
@app.callback( Output('Line Chart', 'figure'),
               Input('Bubble Map', 'selectedData') )
def draw_LineChart(selectedData):
    speed_big = [0] * legth_date   #Total Speed of Big Car
    speed_car = [0] * legth_date   #Total Speed of Car
    speed_mot = [0] * legth_date   #Total Speed of Motor
    volume_big = [0] * legth_date  #Total Volume of Big Car
    volume_car = [0] * legth_date  #Total Volume of Car
    volume_mot = [0] * legth_date  #Total Volume of Motor
    TargetRoadName = []
    if selectedData is None:
        for i in range(LenOfdf):
            str1 = str(df["InfoData"][i])
            date = int(str1[8:])    
            j = date_list.index(date)
            volume_big[j] += df["BIGVOLUME"][i]
            volume_car[j] += df["CARVOLUME"][i]
            volume_mot[j] += df["MOTORVOLUME"][i]
            speed_big[j] += df["BIGSPEED"][i] * df["BIGVOLUME"][i]
            speed_car[j] += df["CARSPEED"][i] * df["CARVOLUME"][i]
            speed_mot[j] += df["MOTORSPEED"][i] * df["MOTORVOLUME"][i]

    else: 
        length_SD = len(selectedData["points"])
        for i in range(length_SD):
                TargetRoadName.append(get_roadname(selectedData["points"][i]["lon"], selectedData["points"][i]["lat"]))
        for i in range(LenOfdf):
            if df["RoadName"][i] in TargetRoadName:
                str1 = str(df["InfoData"][i])
                date = int(str1[8:])    
                j = date_list.index(date)
                volume_big[j] += df["BIGVOLUME"][i]
                volume_car[j] += df["CARVOLUME"][i]
                volume_mot[j] += df["MOTORVOLUME"][i]
                speed_big[j] += df["BIGSPEED"][i] * df["BIGVOLUME"][i]
                speed_car[j] += df["CARSPEED"][i] * df["CARVOLUME"][i]
                speed_mot[j] += df["MOTORSPEED"][i] * df["MOTORVOLUME"][i]

    for i in range(legth_date):
        if volume_big[i] != 0:
            speed_big[i] /= volume_big[i]
        if volume_car[i] != 0:
            speed_car[i] /= volume_car[i]
        if volume_mot[i] != 0:
            speed_mot[i] /= volume_mot[i]

    Avgspeed = {'BIG_AVGSPEED':speed_big, 'CAR_AVGSPEED':speed_car, 'MOTOR_AVGSPEED':speed_mot}
    DataOfLC = pd.DataFrame(Avgspeed)
    DataOfLC.insert(0, 'Date', date_list)
    linechart = px.line(
                            DataOfLC,
                            x= "Date",
                            y= [DataOfLC["BIG_AVGSPEED"], DataOfLC["CAR_AVGSPEED"], DataOfLC["MOTOR_AVGSPEED"]],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "BIG_AVGSPEED": "#afbc8f",
                                "CAR_AVGSPEED": "#e7d292",
                                "MOTOR_AVGSPEED": "#e5a952"
                            },
                    )
    linechart.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title= 'Average Speed Of Cars In January',
        hovermode= 'closest'
    )

    return linechart

#更新html
if __name__ == '__main__':
    app.run_server(debug=True)
