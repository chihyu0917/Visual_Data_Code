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
    'fig_background': '#5F6366',
    # 'plot_background': '#ededed',
    'plot_background': '#5F6366',
    'text': '#FFFFFF',
    'red': '#C1395E',
    'orange': '#E07B42',
    'yellow': '#F0CA50',
    'green': '#AEC17B',
    'blue': '#89A7C2',
    'BIG': '#AFBC8f',
    'CAR': '#E7D292',
    'MOTOR': '#E5A952',
}

# 資料處理以便後續畫圖的處理
path = '/Users/siowanchoi/Desktop/專題/merged.csv'
df = pd.read_csv(path, encoding='utf-8')

#處理pivot_table，內容為路段資訊及每日總量
df['InfoData'] = pd.to_datetime(df['InfoData'], format='%Y-%m-%d %H:%M:%S')
df['Date'] = df['InfoData'].dt.date
df['RoadTotal'] = df['BIGVOLUME'] + df['CARVOLUME'] + df['MOTORVOLUME']
grouped = df.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
pivot_table = grouped.pivot_table(values='RoadTotal', index=['RoadName', 'PositionLon', 'PositionLat'], columns='Date', fill_value=0)

# 計算各個 RoadName 的 Total
Total = pivot_table.sum(axis=1)

# 計算各個 RoadName 的 Label 和 Color
# interval_list = [100000, 200000, 300000, 400000]
interval_list = [15000, 25000, 35000, 45000]
range_str = ["< {}".format(interval_list[0])]
range_str += ["{} to {}".format(interval_list[i]+1,interval_list[i+1]) for i in range(3)]
range_str += ["> {}".format(interval_list[3]+1)]
bins = [0] + interval_list + [np.inf]
Color_list = pd.cut(Total, bins=bins, labels=["BLUE","GREEN", "YELLOW", "ORANGE", "RED"]).tolist()

ColorLabel_list = pd.DataFrame({'RoadName': pivot_table.index.get_level_values('RoadName').tolist(),
                                'PositionLon':pivot_table.index.get_level_values('PositionLon').tolist(),
                                'PositionLat':pivot_table.index.get_level_values('PositionLat').tolist(),
                                'Total_Vol':Total.tolist(),
                                'Color':Color_list,
                                'Range':pd.cut(Total, bins=bins, labels=range_str).tolist()})

DataOfBM_df = pd.merge(pivot_table, ColorLabel_list, on=['PositionLon', 'PositionLat', 'RoadName'])
DataOfBM_df = DataOfBM_df.sort_values('Total_Vol')
#DataOfBM_pd ----> 'lon', 'lat', 'RoadName', 'Total_Vol', 'Color', 'Range'

#路段的資料
RoadInfo = pd.DataFrame({'RoadName': pivot_table.index.get_level_values('RoadName').tolist(),
                        'PositionLon':pivot_table.index.get_level_values('PositionLon').tolist(),
                        'PositionLat':pivot_table.index.get_level_values('PositionLat').tolist()})


#---------------------------------------------Mapbox callback function---------------------------------------------

@app.callback( Output('Bubble Map', 'figure'),
               Input('Line Chart', 'selectedData'),
               Input('Pie Chart', 'clickData'),
               Input('Bar Chart', 'clickData') )
def draw_BubbleMap(selectedData, clickData, clickData2):
    DataOfBM = DataOfBM_df.copy()
    if selectedData is None and clickData is None and clickData2 is None: #Default
        df_subset = df.copy()
        df_subset['RoadTotal'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    elif selectedData is not None:
        first = selectedData['range']['x'][0]
        last = selectedData['range']['x'][1]
        first = datetime.strptime(first, '%Y-%m-%d %H:%M:%S.%f')
        last = datetime.strptime(last, '%Y-%m-%d %H:%M:%S.%f')
        df_subset = df.copy()
        df_subset['Date'] = pd.to_datetime(df_subset['Date'])
        df_subset = df[(df_subset['Date'] >= first) & (df_subset['Date'] <= last)]
        df_subset['RoadTotal'] = df_subset['BIGVOLUME'] + df_subset['CARVOLUME'] + df_subset['MOTORVOLUME']
    elif clickData is not None:
        df_subset = df.copy()
        if clickData['points'][0]['label'] == 'BIG':
            df_subset['RoadTotal'] = df_subset['BIGVOLUME']
        elif clickData['points'][0]['label'] == 'CAR':
            df_subset['RoadTotal'] = df_subset['CARVOLUME'] 
        elif clickData['points'][0]['label'] == 'MOTOR':
            df_subset['RoadTotal'] = df_subset['MOTORVOLUME']
    elif clickData2 is not None:
        label = clickData2['points'][0]['label']
        DataOfBM = DataOfBM_df[DataOfBM_df['Color'] == label]
        
    if clickData is not None or selectedData is not None:
        grouped = df_subset.groupby(['RoadName', 'Date', 'PositionLon', 'PositionLat'])['RoadTotal'].sum().reset_index()
        pivot_table = grouped.pivot_table(values='RoadTotal', index=['RoadName', 'PositionLon', 'PositionLat'], columns='Date', fill_value=0)

        Total = pivot_table.sum(axis=1)

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

    map_fig = px.scatter_mapbox(
                                DataOfBM,
                                labels=dict(color='Total_Vol'),
                                lat=DataOfBM['PositionLat'],
                                lon=DataOfBM['PositionLon'],
                                color=DataOfBM['Range'],
                                hover_name=DataOfBM['RoadName'],
                                size=DataOfBM['Total_Vol'],
                                size_max=15,
                                zoom=10,
                                color_discrete_map={
                                    range_str[0]: colors['blue'],
                                    range_str[1]: colors['green'],
                                    range_str[2]: colors['yellow'],
                                    range_str[3]: colors['orange'],
                                    range_str[4]: colors['red']
                                }
    )
    map_fig.update_layout(
        # mapbox_style='stamen-terrain',
        mapbox_style='carto-positron',
        plot_bgcolor=colors['plot_background'],
        paper_bgcolor=colors['fig_background'],
        font_color=colors['text'],
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            font=dict(size=10)
        ),
        geo=dict(
            scope='asia',
            center=dict(lat=25, lon=121.53),
            projection_scale=100,
            showland=True
        ),
        margin=dict(l=30, r=30, t=60, b=30),
        title='Taiwan Map',
        hovermode='closest'
    )
    return map_fig


#---------------------------------------------Bar Chart callback function---------------------------------------------
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
            "BLUE": colors['blue'],
            "GREEN": colors['green'],
            "YELLOW": colors['yellow'],
            "ORANGE": colors['orange'],
            "RED": colors['red']
        }
    )
    barchart.update_layout(
        plot_bgcolor=colors['plot_background'],
        paper_bgcolor=colors['fig_background'],
        font_color=colors['text'],
        title= {
            'text': 'Quantity Of Each Color',
            'x': 0.5,
            'y': 0.95
        },
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode='closest',
        showlegend=False
    )
    return barchart

#function： 取得RoadName的list
def get_roadname(lon, lat):
    for i in range(len(RoadInfo)):
        if (RoadInfo["PositionLon"][i] == lon and RoadInfo["PositionLat"][i] == lat):
            Road = RoadInfo["RoadName"][i]
            return Road
    return None


#---------------------------------------------Pie Chart callback function---------------------------------------------
@app.callback( Output('Pie Chart', 'figure'),
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
                            "BIG": colors['BIG'],
                            "CAR": colors['CAR'],
                            "MOTOR": colors['MOTOR']
                        }
                    )
    piechart.update_layout(
        plot_bgcolor=colors['plot_background'],
        paper_bgcolor=colors['fig_background'],
        font_color=colors['text'],
        title= {
            'text': 'Proportion Of Cars',
            'x': 0.5,
            'y': 0.95
        },
        hovermode= 'closest'
    )
    return piechart


#---------------------------------------------Heat Map callback function---------------------------------------------
@app.callback( Output('Heap Map', 'figure'),
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
    DataOfHM = pd.pivot_table(df_subset, values='Total Volume', index=['Weekday'], columns=['Time'], aggfunc=np.sum, fill_value=0)
    
    heatmap = px.imshow(
                        DataOfHM,
                        labels=dict(y="Day of Week", x="Time of Day", color="Total Volume"),
                        x=list(DataOfHM.columns),
                        y=list(DataOfHM.index),
                        color_continuous_scale='Pinkyl'
                        # color_continuous_scale=[colors['blue'], colors['green'], colors['yellow'], colors['orange'], colors['red']]
                    )
    
    heatmap.update_layout(
        plot_bgcolor=colors['plot_background'],
        paper_bgcolor=colors['fig_background'],
        font_color=colors['text'],
        title= {
            'text': 'Total Volume Of Each Week',
            'x': 0.5,
            'y': 0.95
        },
        hovermode= 'closest'
    )
    
    return heatmap



#---------------------------------------------Line Chart callback function---------------------------------------------
@app.callback( Output('Line Chart', 'figure'),
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
                            "BIG_AVGSPEED": colors['BIG'],
                            "CAR_AVGSPEED": colors['CAR'],
                            "MOTOR_AVGSPEED": colors['MOTOR']
                        },
                       )
    else:
        if clickData['points'][0]['label'] == 'BIG':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["BIG_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "BIG_AVGSPEED": colors['BIG']
                            },
                        )
        elif clickData['points'][0]['label'] == 'CAR':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["CAR_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "CAR_AVGSPEED": colors['CAR']
                            },
                        )
        elif clickData['points'][0]['label'] == 'MOTOR':
            linechart = px.line(pivoted_df, x=pivoted_df.index, y=["MOTOR_AVGSPEED"],
                            labels=dict(x="Date", y="Average Speed"),
                            markers=True,
                            color_discrete_map={
                                "MOTOR_AVGSPEED": colors['MOTOR']
                            },
                        )

    linechart.update_layout(
        plot_bgcolor= colors['plot_background'],
        paper_bgcolor= colors['fig_background'],
        font_color=colors['text'],
        title= {
            'text': 'Average Speed Of Cars',
            'x': 0.5,
            'y': 0.95
        },
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode= 'closest'
    )
    return linechart


#---------------------------------------------Dash Board 版面---------------------------------------------
app.layout = html.Div(
    style={'height': '100%', 'width': '100%', 'backgroundColor': colors['background'], 'fontFamily': 'Times New Roman, sans-serif', 'padding': '2%'},
    children=[        
        html.H1("DashBoard", style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '2%', 'fontSize': '40px'}),
        html.Div(
            style={'height': '100vh', 'width': '100%', 'display': 'flex', 'flexWrap': 'wrap'},
            children=[
                html.Div( #左邊
                    style={'height': '100vh', 'width': '34%', 'float': 'left', 'marginRight': '1%'},
                    children=[dcc.Graph(id='Bubble Map', style={'height': '100vh'})]
                ),
                html.Div( #右邊
                    style={'height': '100vh', 'width': '65%', 'float': 'right', 'display': 'flex', 'flexWrap': 'wrap'},
                    children=[
                        html.Div(
                            style={'width': '100%', 'height': '49%', 'marginBottom': '1%'},
                            children=[dcc.Graph(id='Line Chart', style={'height': '100%'})]
                        ),
                        html.Div(
                            style={'width': '29%', 'height': '50%', 'marginRight': '1%'},
                            children=[dcc.Graph(id='Bar Chart', style={'height': '100%'})]
                        ),
                        html.Div(
                            style={'width': '34%', 'height': '50%', 'marginRight': '1%'},
                            children=[dcc.Graph(id='Heap Map', style={'height': '100%'})]
                        ),
                        html.Div(
                            style={'width': '35%', 'height': '50%'},
                            children=[dcc.Graph(id='Pie Chart', style={'height': '100%'})]
                        )
                    ]
                ),
            ]
        )
    ]
)




#---------------------------------------------html update---------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)