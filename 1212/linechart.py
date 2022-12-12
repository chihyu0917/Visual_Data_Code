# # import plotly.express as px

# # df = px.data.gapminder().query("continent=='Oceania'")
# # # df = [[1, 2], [3, 4]] #不能用
# # fig = px.line(df, x="year", y="lifeExp", color='country')
# # fig.show()

# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px
# import pandas as pd

# app = Dash(__name__)


# app.layout = html.Div([
#     html.H4('Line Chart'),
#     dcc.Graph(id="graph"),
#     dcc.Input(id='my-input', value='initial value', type='text')
#     # dcc.Checklist(
#     #     id="checklist",
#     #     # options=["Asia", "Europe", "Africa","Americas","Oceania"],
#     #     # value=["Americas", "Oceania"],
#     #     options=["BIGSPEED", "CARSPEED", "MOTORSPEED"],
#     #     value=["BIGSPEED", "CARSPEED", "MOTORSPEED"],
#     #     inline=True
#     # ),
# ])


# @app.callback(
#     Output("graph", "figure"), 
#     Input("my_input", "value"))
# # def update_line_chart(continents):
# #     df = px.data.gapminder() # replace with your own data source
# #     mask = df.continent.isin(continents)
#     # fig = px.line(df[mask], 
#         # x="year", y="lifeExp", color='country')
# def update_line_chart(speed):
#     # path = '../data_source/linechart.csv'
#     # df = pd.read_csv(path)
#     # mask = df.speed.isin(speed)
#     # fig = px.line(df[mask], x="year", y="lifeExp", color='country')
#     df = pd.DataFrame(dict(
#     x = [1, 3, 2, 4],
#     y = [1, 2, 3, 4]
#     ))
#     fig = px.line(df, x="x", y="y", title="Unsorted Input") 
#     return fig
# # df = pd.DataFrame(dict(
# # x = [1, 3, 2, 4],
# # y = [1, 2, 3, 4]
# # ))
# # fig = px.line(df, x="x", y="y", title="Unsorted Input") 
# # fig.show()


# app.run_server(debug=True)

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
path = '../data_source/201801/vdtrafonetab_info_001.csv'
df = pd.read_csv(path , header = None)
def useful_speed(big, car, mot):
    if big > 120: 
        big = 120
    if car > 150: 
        car = 150
    if mot > 90: 
        mot = 90
    # if big == 0 or car == 0 or mot == 0: 
    #     big = car = mot = -1
    if big < 10: 
        big = 40
    if car < 20: 
        car = 60
    if mot < 10: 
        mot = 40
    result = [big, car, mot]
    return result

date_list = []
for i in range(500000):
    str1 = str(df[23][i])
    list1 = str1.split(' ')
    date = int(list1[0][8:])
    if date not in date_list:
        date_list.append(date)
date_list = sorted(date_list)
print(date_list)
date_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
speed_big = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
speed_car = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
speed_mot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(500000):
# for i in range(20):
    str1 = str(df[23][i])
    list1 = str1.split(' ')
    date = int(list1[0][8:])
    speed_list = useful_speed(df[9][i], df[11][i], df[13][i])
    if speed_list[0] != -1:
        j = date_list.index(date)
        date_num[j] += 1
        speed_big[j] += speed_list[0]
        speed_car[j] += speed_list[1]
        speed_mot[j] += speed_list[2]
for i in range(10):
    if date_num[i] == 0:
        date_num[i] = 1
    speed_big[i] /= date_num[i]
    speed_car[i] /= date_num[i]
    speed_mot[i] /= date_num[i]
print(date_num)
print(speed_big, speed_car, speed_mot)
speed_merge = speed_big + speed_car + speed_mot
print(speed_merge)
df2 = pd.DataFrame({
    "Fruit": [5, 7, 8, 10, 15, 20, 22, 25, 28, 29, 5, 7, 8, 10, 15, 20, 22, 25, 28, 29, 5, 7, 8, 10, 15, 20, 22, 25, 28, 29],
    # "Amount": [4, 1, 2, 2, 4, 5],
    "Amount": speed_merge,
    # "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    "City": ['BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'BIGVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'CARVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME', 'MOTORVOLUME']
})

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig = px.line(df2, x="Fruit", y="Amount", color="City")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)