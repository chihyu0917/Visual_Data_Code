from dash import Dash, html, dcc
import csv
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime
import json

# function Definition
def time_def(hr):
    result = -1
    result_str = ['Morning', 'Afternoon', 'Evening']
    i = 0
    if hr < 12: 
        result = 0
        # i = 0
    elif hr < 18:
        result = 1
        # i = 1
    else:
        result = 2
        # i = 2
    # return result
    return str(result) + ' ' + result_str[result]

def week_def(date):
    weekday = ['1 Monday', '2 Tuesday', '3 Wednesday', '4 Thursday', '5 Friday', '6 Saturday', '7 Sunday']
    return weekday[date%7]
    # return date%7

app = Dash(__name__)

colors = {
    'background': '#434648',
    'text': '#FFFFFF'
}

# 資料處理以便後續畫圖的處理
path = '../final/test.csv'
df = pd.read_csv(path, encoding='utf-8')

# 數據處理
df['InfoData'] = pd.to_datetime(df['InfoData'], format='%Y-%m-%d %H:%M:%S')
df['Date'] = df['InfoData'].dt.date
df['RoadTotal'] = df['BIGVOLUME'] + df['CARVOLUME'] + df['MOTORVOLUME']
# grouped = df.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
grouped = df.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
pivot_table = grouped.pivot_table(values='RoadTotal', index=['RoadName', 'PositionLon', 'PositionLat'], columns='Date', fill_value=0)

# 計算各個 RoadName 的 Total
Total = pivot_table.sum(axis=1)

# 計算各個 RoadName 的 Label 和 Color
# interval_list = [100000, 200000, 300000, 400000]
interval_list = [5000, 10000, 20000, 100000]
range_str = ["< {}".format(interval_list[0])]
range_str += ["{} to {}".format(interval_list[i]+1,interval_list[i+1]) for i in range(3)]
range_str += ["> {}".format(interval_list[3]+1)]
bins = [0] + interval_list + [np.inf]
Label_list = pd.cut(Total, bins=bins, labels=range_str).tolist()
Color_list = pd.cut(Total, bins=bins, labels=["BLUE","GREEN", "YELLOW", "ORANGE", "RED"]).tolist()


DataOfBM = pd.DataFrame({
                            'PositionLon': pivot_table.index.get_level_values('PositionLon'), 
                            'PositionLat': pivot_table.index.get_level_values('PositionLat'), 
                            'RoadName': pivot_table.index.get_level_values('RoadName'), 
                            'Total_Vol': Total, 
                            'Color': Color_list, 
                            'Range': Label_list
                        })
# DataOfBM2 = pd.DataFrame(Road_Data, columns= date_list)
# DataOfBM2 = pd.DataFrame(pivot_table, columns= 'Date')
# TotalVolume = pd.concat([DataOfBM, DataOfBM2], axis=1)
TotalVolume = pd.concat([DataOfBM], axis=1)

# #Bubble Map
# map_fig = px.scatter_mapbox(
#                                 TotalVolume, 
#                                 labels= dict(color="Total Volume"),
#                                 lat=TotalVolume["PositionLat"], 
#                                 lon=TotalVolume["PositionLon"],
#                                 color= TotalVolume["Range"],
#                                 hover_name=TotalVolume["RoadName"],
#                                 size= TotalVolume["Total_Vol"],
#                                 zoom=10,
#                                 color_discrete_map={
#                                     range_str[0]: "blue",
#                                     range_str[1]: "green",
#                                     range_str[2]: "yellow",
#                                     range_str[3]: "orange",
#                                     range_str[4]: "red"
#                                 }
#                         )
# map_fig.update_layout(mapbox_style='open-street-map')
# map_fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text'],
#     geo = dict(
#                 scope='asia',
#                 center = dict(lat = 25, lon = 121.53),
#                 projection_scale = 100,
#                 showland = True
#               ),
#     title= 'Taiwan Map',
#     hovermode= 'closest'
# )

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
    # html.Div(dcc.Graph(id='Bubble Map', figure=map_fig),style={'width': '45%' ,'display': 'inline-block', 'height': '100%'}),
    html.Div(dcc.Graph(id='Bubble Map'),style={'width': '45%' ,'display': 'inline-block', 'height': '100%'}),
    html.Div(dcc.Graph(id='Bar Chart'),style={'width': '30%' ,'display': 'inline-block'}),
    html.Div(dcc.Graph(id="Heap Map"),style={'width': '25%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='Line Chart'),style={'width': '70%', 'display': 'inline-block'}),
    html.Div(dcc.Graph(id='Pie Chart'),style={'width': '30%', 'display': 'inline-block'})
])

@app.callback( Output('Bubble Map', 'figure'),
               Input('Line Chart', 'selectedData'),
               Input('Pie Chart', 'clickData') )
def draw_BubbleMap(selectedData, clickData):
    if selectedData is None and clickData is None:
        df_subset = df.copy()
        df_subset['RoadTotal'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    elif clickData is None:
        first = selectedData['range']['x'][0]
        last = selectedData['range']['x'][1]
        first = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        last = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
        df_subset = df.copy()
        df_subset['Date'] = pd.to_datetime(df_subset['Date'])
        df_subset = df[(df_subset['Date'] >= first) & (df_subset['Date'] <= last)]
        df_subset['RoadTotal'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    else:
        df_subset = df.copy()
        if clickData['points'][0]['label'] == 'BIG':
            # df_subset['Total Volume'] = df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
            df_subset['RoadTotal'] = df_subset['BIGVOLUME']
        elif clickData['points'][0]['label'] == 'CAR':
            df_subset['RoadTotal'] = df_subset['CARVOLUME'] 
        elif clickData['points'][0]['label'] == 'MOTOR':
            df_subset['RoadTotal'] = df_subset['MOTORVOLUME']
    # 數據處理
    grouped = df_subset.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
    pivot_table = grouped.pivot_table(values='RoadTotal', index=['RoadName', 'PositionLon', 'PositionLat'], columns='Date', fill_value=0)

    # 計算各個 RoadName 的 Total
    Total = pivot_table.sum(axis=1)

    # 計算各個 RoadName 的 Label 和 Color
    # interval_list = [5000, 10000, 20000, 100000]
    # range_str = ["< {}".format(interval_list[0])]
    # range_str += ["{} to {}".format(interval_list[i]+1,interval_list[i+1]) for i in range(3)]
    # range_str += ["> {}".format(interval_list[3]+1)]
    # bins = [0] + interval_list + [np.inf]
    Label_list = pd.cut(Total, bins=bins, labels=range_str).tolist()
    Color_list = pd.cut(Total, bins=bins, labels=["BLUE","GREEN", "YELLOW", "ORANGE", "RED"]).tolist()

    DataOfBM = pd.DataFrame({
                                'PositionLon': pivot_table.index.get_level_values('PositionLon'), 
                                'PositionLat': pivot_table.index.get_level_values('PositionLat'), 
                                'RoadName': pivot_table.index.get_level_values('RoadName'), 
                                'Total_Vol': Total, 
                                'Color': Color_list, 
                                'Range': Label_list
                            })
    # DataOfBM2 = pd.DataFrame(Road_Data, columns= date_list)
    # DataOfBM2 = pd.DataFrame(pivot_table, columns= 'Date')
    # TotalVolume = pd.concat([DataOfBM, DataOfBM2], axis=1)
    TotalVolume = pd.concat([DataOfBM], axis=1)

    #Bubble Map
    map_fig = px.scatter_mapbox(
                                    TotalVolume, 
                                    # labels= dict(color="Total Volume"),
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
    return map_fig

#Bar Chart callback function
@app.callback( Output('Bar Chart', 'figure'),
               Input('Bubble Map', 'selectedData'),
               Input('Line Chart', 'selectedData'),
               Input('Pie Chart', 'clickData') )
def draw_BarChart(selectedData, selectedData2, clickData):
    color_counts = {"BLUE": 0, "GREEN": 0, "YELLOW": 0, "ORANGE": 0, "RED": 0}
    if selectedData is None and selectedData2 is None and clickData is None: #Default
        for color in Color_list:
            color_counts[color] += 1
    elif selectedData2 is None and clickData is None: #Bubble Map
        marker_sizes = [p["marker.size"] for p in selectedData["points"]]
        for size in marker_sizes:
            if size > interval_list[3]:
                color_counts["RED"] += 1
            elif size > interval_list[2]:
                color_counts["ORANGE"] += 1
            elif size > interval_list[1]:
                color_counts["YELLOW"] += 1
            elif size > interval_list[0]:
                color_counts["GREEN"] += 1
            else:
                color_counts["BLUE"] += 1
    else:
        if selectedData2 is None: #Pie Chart    
            df_subset = df.copy()
            if clickData['points'][0]['label'] == 'BIG':
                df_subset['RoadTotal'] = df_subset['BIGVOLUME']
            elif clickData['points'][0]['label'] == 'CAR':
                df_subset['RoadTotal'] = df_subset['CARVOLUME'] 
            elif clickData['points'][0]['label'] == 'MOTOR':
                df_subset['RoadTotal'] = df_subset['MOTORVOLUME']
        else: #Line Chart
            first = selectedData2['range']['x'][0]
            last = selectedData2['range']['x'][1]
            first = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
            last = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
            df_subset = df.copy()
            df_subset['Date'] = pd.to_datetime(df_subset['Date'])
            df_subset = df[(df_subset['Date'] >= first) & (df_subset['Date'] <= last)]
            df_subset['RoadTotal'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    
        grouped = df_subset.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
        pivot_table = grouped.pivot_table(values='RoadTotal', index=['RoadName', 'PositionLon', 'PositionLat'], columns='Date', fill_value=0)

        Total = pivot_table.sum(axis=1)

        Color_list2 = pd.cut(Total, bins=bins, labels=["BLUE","GREEN", "YELLOW", "ORANGE", "RED"]).tolist()
        for color in Color_list2:
            if color == "BLUE" or color == "GREEN" or color == "YELLOW" or color == "ORANGE" or color == "RED":
                color_counts[color] += 1
        
    data = {'COLOR': list(color_counts.keys()), 'QUANTITY': list(color_counts.values())}
    total_flow = pd.DataFrame(data)
    barchart = px.bar(
        total_flow,
        labels=dict(x="Traffic Volume", y="COLOR LABEL"),
        y=total_flow["COLOR"],
        x=total_flow["QUANTITY"],
        color=total_flow["COLOR"],
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
        title='The Quantity Of Each Color Bubble',
        hovermode='closest'
    )
    return barchart

#function： 取得RoadName的list
def get_roadname(lon, lat):
    for i in range(len(TotalVolume)):
        if (TotalVolume["PositionLon"][i] == lon and TotalVolume["PositionLat"][i] == lat):
            Road = TotalVolume["RoadName"][i]
            return Road
    return None

#Pie Chart callback function
@app.callback( Output('Pie Chart', 'figure'),
            #    Input('Bubble Map', 'selectedData') )
               Input('Bubble Map', 'selectedData'),
               Input('Line Chart', 'selectedData') )

def draw_PieChart(selectedData, selectedData2):
    EACHVOLUME = {'BIG': 0, "CAR": 0, "MOTOR": 0}
    TargetRoadName = []
    if selectedData is None and selectedData2 is None:
        df_subset = df.copy()
    elif selectedData2 is None:
        TargetRoadName = [get_roadname(point['lon'], point['lat']) for point in selectedData['points']]
        df_subset = df[df['RoadName'].isin(TargetRoadName)]
    else:
        first = selectedData2['range']['x'][0]
        last = selectedData2['range']['x'][1]
        first = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        last = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
        df_subset = df.copy()
        df_subset['Date'] = pd.to_datetime(df_subset['Date'])
        df_subset = df[(df_subset['Date'] >= first) & (df_subset['Date'] <= last)]
    
    EACHVOLUME['BIG'] = df_subset["BIGVOLUME"].sum()
    EACHVOLUME['CAR'] = df_subset["CARVOLUME"].sum()
    EACHVOLUME['MOTOR'] = df_subset["MOTORVOLUME"].sum()
    
    DataOfPie = pd.DataFrame({'CLASS':list(EACHVOLUME.keys()), 'FLOW':list(EACHVOLUME.values())})
    piechart = px.pie(
                        DataOfPie, 
                        names= DataOfPie["CLASS"], 
                        values= DataOfPie["FLOW"],
                        color= DataOfPie["CLASS"],
                        color_discrete_map={
                            "BIG": "#afbc8f",
                            "CAR": "#e7d292",
                            "MOTOR": "#e5a952"
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

#Heap Map callback function
@app.callback( Output('Heap Map', 'figure'),
            #    Input('Bubble Map', 'selectedData') )
            Input('Bubble Map', 'selectedData'),
            Input('Line Chart', 'selectedData'),
            Input('Pie Chart', 'clickData') )
def draw_HeapMap(selectedData, selectedData2, clickData):
    DataOfHM = pd.DataFrame(index=[], columns=[])
    # DataOfHM = np.zeros((7, 3))
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # if selectedData is None:
    if selectedData is None and selectedData2 is None and clickData is None:
        df_subset = df.copy()
        df_subset['Total Volume'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    # else:
    elif clickData is None and selectedData2 is None:
        TargetRoadName = [get_roadname(point['lon'], point['lat']) for point in selectedData['points']]
        df_subset = df[df['RoadName'].isin(TargetRoadName)]
        df_subset['Total Volume'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    elif selectedData2 is None:
        df_subset = df.copy()
        if clickData['points'][0]['label'] == 'BIG':
            # df_subset['Total Volume'] = df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
            df_subset['Total Volume'] = df_subset['BIGVOLUME']
        elif clickData['points'][0]['label'] == 'CAR':
            df_subset['Total Volume'] = df_subset['CARVOLUME'] 
        elif clickData['points'][0]['label'] == 'MOTOR':
            df_subset['Total Volume'] = df_subset['MOTORVOLUME']
    else:
        first = selectedData2['range']['x'][0]
        last = selectedData2['range']['x'][1]
        first = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        last = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
        df_subset = df.copy()
        df_subset['Date'] = pd.to_datetime(df_subset['Date'])
        df_subset = df[(df_subset['Date'] >= first) & (df_subset['Date'] <= last)]
        df_subset['Total Volume'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    
    df_subset['InfoTime'] = pd.to_datetime(df_subset['InfoTime'], format='%Y-%m-%d %H:%M:%S')
    df_subset['Date'] = df_subset['InfoTime'].dt.date
    df_subset['Time'] = df_subset['InfoTime'].dt.hour.apply(time_def)
    df_subset['Weekday'] = df_subset['InfoTime'].dt.dayofweek.apply(week_def)
    # df_subset['Total Volume'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    DataOfHM = pd.pivot_table(df_subset, values='Total Volume', index=['Weekday'], columns=['Time'], aggfunc=np.sum, fill_value=0)
    
    heatmap = px.imshow(
                        DataOfHM,
                        labels=dict(y="Day of Week", x="Time of Day", color="Total Volume"),
                        x=list(DataOfHM.columns),
                        y=list(DataOfHM.index),
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


#Line Chart callback function
@app.callback( Output('Line Chart', 'figure'),
            #    Input('Bubble Map', 'selectedData') )
            Input('Bubble Map', 'selectedData'),
            Input('Pie Chart', 'clickData') )
def draw_LineChart(selectedData, clickData):
    legth_date = len(pivot_table.columns)
    
    TargetRoadName = []
    
    # if selectedData is None:
    if selectedData is None and clickData is None:
        df_subset = df.copy()

    elif clickData is None: 
        TargetRoadName = [get_roadname(point['lon'], point['lat']) for point in selectedData['points']]
        df_subset = df[df['RoadName'].isin(TargetRoadName)]
    else:
        df_subset = df.copy()
        

    # agg_dict = {"Speed": np.sum, "Volume": np.sum}
    df_subset['BIGSPEED'] = df_subset['BIGSPEED'] * df_subset['BIGVOLUME']
    df_subset['CARSPEED'] = df_subset['CARSPEED'] * df_subset['CARVOLUME']
    df_subset['MOTORSPEED'] = df_subset['MOTORSPEED'] * df_subset['MOTORVOLUME']
    pivoted_df = pd.pivot_table(df_subset, values=["BIGSPEED", "CARSPEED", "MOTORSPEED", "BIGVOLUME", "CARVOLUME", "MOTORVOLUME"],
                                 index=["Date"], aggfunc=np.sum, fill_value=0)
    pivoted_df["BIG_AVGSPEED"] = pivoted_df["BIGSPEED"] / pivoted_df["BIGVOLUME"]
    pivoted_df["CAR_AVGSPEED"] = pivoted_df["CARSPEED"] / pivoted_df["CARVOLUME"]
    pivoted_df["MOTOR_AVGSPEED"] = pivoted_df["MOTORSPEED"] / pivoted_df["MOTORVOLUME"]

    if clickData is None:
        linechart = px.line(pivoted_df, x=pivoted_df.index, y=["BIG_AVGSPEED", "CAR_AVGSPEED", "MOTOR_AVGSPEED"],
                        labels=dict(x="Date", y="Average Speed"),
                        markers=True,
                        color_discrete_map={
                            "BIG_AVGSPEED": "#afbc8f",
                            "CAR_AVGSPEED": "#e7d292",
                            "MOTOR_AVGSPEED": "#e5a952"
                        },
                       )
    else:
        if clickData['points'][0]['label'] == 'BIG':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["BIG_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "BIG_AVGSPEED": "#afbc8f"
                            },
                        )
        elif clickData['points'][0]['label'] == 'CAR':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["CAR_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "CAR_AVGSPEED": "#e7d292"
                            },
                        )
        elif clickData['points'][0]['label'] == 'MOTOR':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["MOTOR_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "MOTOR_AVGSPEED": "#e5a952"
                            },
                        )
    # linechart = px.line(pivoted_df, x=pivoted_df.index, y=["BIG_AVGSPEED", "CAR_AVGSPEED", "MOTOR_AVGSPEED"],
    #                     labels=dict(x="Date", y="Average Speed"),
    #                     markers=True,
    #                     color_discrete_map={
    #                         "BIG_AVGSPEED": "#afbc8f",
    #                         "CAR_AVGSPEED": "#e7d292",
    #                         "MOTOR_AVGSPEED": "#e5a952"
    #                     },
    #                    )

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