import dash
from dash import html, dcc, callback, Input, Output, dash_table

import pandas as pd
import base64
import io

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Representación tabular'),

    html.Div(children='''
        Carga un archivo CSV y visualiza su contenido.
    '''),

    dcc.Upload(
        id='upload-data-1',
        children=html.Div([
            'Arrastra o ',
            html.A('selecciona un archivo')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Permitimos subir solo archivos CSV
        accept='.csv'
    ),
    
    dcc.Dropdown(
        id='select-columns',
        options=[],
        multi=True,
        placeholder="Selecciona las columnas que deseas visualizar"
    ),
    
    html.Div(id='output-data-upload')


])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Leemos el archivo CSV
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # Creamos la tabla con los datos del DataFrame
        table = dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'scroll'},
        )
        # Actualizamos las opciones del dropdown
        dropdown_options = [{'label': col, 'value': col} for col in df.columns]
        # Devolvemos la tabla y las opciones del dropdown
        return table, dropdown_options
    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error procesando este archivo.'
        ])

# Callback que se ejecuta al subir un archivo
@callback([Output('output-data-upload', 'children'),
           Output('select-columns', 'options')],
          [Input('upload-data-1', 'contents'),
           Input('upload-data-1', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        children, options = parse_contents(contents, filename)
        return children, options
    return dash.no_update

# Callback que se ejecuta al seleccionar las columnas del dropdown
@callback(Output('table', 'columns'),
          Input('select-columns', 'value'))
def update_columns(value):
    if value is not None:
        columns = [{'name': col, 'id': col} for col in value]
        return columns
    return dash.no_update

# Callback que se ejecuta al subir un archivo o seleccionar las columnas del dropdown
@callback(Output('table', 'data'),
          Input('upload-data-1', 'contents'),
          Input('select-columns', 'value'))
def update_data(contents, value):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        if value is not None:
            df = df[value]
        return df.to_dict('records')

