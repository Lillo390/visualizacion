import dash
from dash import dcc
from dash import html
import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Table Example (CSV)'),
    dcc.Dropdown(
        id='X',
        options = [{'label':name, 'value':name} for name in df.columns],
        value = 'Index'
        ),
    generate_table(df),
    html.Div(id = 'selection'),
])


@app.callback(
    dash.dependencies.Output('selection', 'children'),
    [dash.dependencies.Input('X', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
