import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

df = pd.read_csv('./data/california_cities.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='elev-slider',
        min=df['elevation_m'].min(),
        max=df['elevation_m'].max(),
        value=df['elevation_m'].max(),
        marks={str(alt): str(int(alt)) for alt in np.linspace(df['elevation_m'].min(),df['elevation_m'].max(), 10)}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('elev-slider', 'value')])

def update_figure(selected_elev):
    filtered_df = df[df.elevation_m <= selected_elev]
    traces=[go.Scatter(
        x=filtered_df['longd'],
        y=filtered_df['latd'],
        marker_size=filtered_df['population_total']/10000,
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        }
        )]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Longitud'},
            yaxis={'title': 'Latitud'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
