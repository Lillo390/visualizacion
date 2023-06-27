import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('./data/california_cities.csv')
Lslider = []
min=df['elevation_m'].min()
max=df['elevation_m'].max()
for e in range(int(min),int(max),200):
    Lslider.append(e)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='elevation-slider',
        min=df['elevation_m'].min(),
        max=df['elevation_m'].max(),
        value=(max+min)/2,
        marks={str(e): str(e) for e in Lslider}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('elevation-slider', 'value')])

def update_figure(selected_elev):
    filtered_df = df[df.elevation_m <= selected_elev]
    traces = []
    print(filtered_df['city'])
    traces.append(go.Scatter(
        x=filtered_df['longd'],
        y=filtered_df['latd'],
        marker_size=filtered_df['population_total']/10000,
        text=filtered_df['city'],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'black'}
        },
))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'longitud'},
            yaxis={'title': 'latitud'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
