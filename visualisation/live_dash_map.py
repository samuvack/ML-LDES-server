import pandas as pd
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

import plotly.express as px
import datetime
from random import random
import random
import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('IOW LDES (Linked Data Event Stream) Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

print(type(us_cities))

us_cities['color'] = [ random.randint(1,6)  for k in us_cities.index]
us_cities['lat'] = [ random.randint(50,52)  for k in us_cities.index]
us_cities['lon'] = [ random.randint(2,3) for k in us_cities.index]

print(us_cities)
property
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    


    fig2 = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            color_continuous_scale=px.colors.cyclical.IceFire, color="color", zoom=3, height=300)
    fig2.update_layout(mapbox_style="open-street-map")
    fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})





    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)