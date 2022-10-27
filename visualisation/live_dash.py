import datetime
from random import random
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


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    temp= 8 + random()*4
    con= 28 + random()*4
    pH =  random()*14
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Temperature: {0:.2f}'.format(temp), style=style),
        html.Span('Conductivity: {0:.2f}'.format(con), style=style),
        html.Span('pH: {0:0.2f}'.format(pH), style=style)
    ]

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    
    print('clean')
    print(n)
    if n ==0:
        global data
        data = {'time': [],
            'Conductivity': [],
            'Temperature': [],
            'pH': []}
        

        # Collect some data
        for i in range(180, 0, -1):
            time = datetime.datetime.now() - datetime.timedelta(seconds=i*1)
            temp= 8 + random()*4
            con= 28 + random()*4
            pH =  random()*14
            print(time)
            data['Temperature'].append(temp)
            data['Conductivity'].append(con)
            data['pH'].append(pH)
            data['time'].append(time)


    time = datetime.datetime.now()
    temp= 8 + random()*4
    con= 28 + random()*4
    pH =  random()*14
    data['Temperature'].append(temp)
    data['Conductivity'].append(con)
    data['pH'].append(pH)
    data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=3, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['pH'],
        'name': 'pH',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['Temperature'],
        'name': 'Temperature',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)
    fig.append_trace({
        'x': data['Conductivity'],
        'y': data['Temperature'],
        'text': data['time'],
        'name': 'Temperature vs Conductivity',
        'mode': 'markers',
        'type': 'scatter'
    }, 3, 1)

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)