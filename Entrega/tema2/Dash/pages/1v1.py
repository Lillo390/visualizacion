import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, callback
import pandas as pd
import plotly.express as px
import base64
import io

dash.register_page(__name__)

# Layout de la aplicación
layout = html.Div([
    html.H1("Representación de variable frente a variable"),
    dcc.Upload(
        id="upload-data-2",
        children=html.Div(["Arrastra o selecciona un archivo CSV"]),
        style={
            "width": "50%",
            "height": "50px",
            "lineHeight": "50px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px"
        }
    ),
    html.Div([
        dcc.RadioItems(
            id="x-axis",
            options=[],
            value=None,
            labelStyle={"display": "inline-block", "marginRight": "10px"}
        ),
        dcc.RadioItems(
            id="y-axis",
            options=[],
            value=None,
            labelStyle={"display": "inline-block", "marginRight": "10px"}
        ),
        html.Button(id="submit-button-1", children="Visualizar")
    ], style={"margin": "10px"}),
    dcc.Graph(id="scatter")
])

# Callback para cargar los datos del archivo CSV
@callback(
    [Output("x-axis", "options"), Output("y-axis", "options")],
    [Input("upload-data-2", "contents")],
    [State("upload-data-2", "filename")]
)
def load_csv(contents, filename):
    if contents is not None:
        # Convertir los datos del archivo CSV en un DataFrame de Pandas
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            else:
                return [], []
        except Exception as e:
            print(e)
            return [], []

        # Crear las opciones para los RadioItems
        options = [{"label": col, "value": col} for col in df.columns]
        
        return options, options

    return [], []


# Callback para generar el gráfico
@callback(
    Output("scatter", "figure"),
    [Input("submit-button-1", "n_clicks")],
    [State("x-axis", "value"), State("y-axis", "value"), State("upload-data-2", "contents"), State("upload-data-2", "filename")]
)
def generate_scatter(n_clicks, x_col, y_col, contents, filename):

    if n_clicks is not None and x_col is not None and y_col is not None and contents is not None:
        # Convertir los datos del archivo CSV en un DataFrame de Pandas
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            else:
                return px.scatter()
        except Exception as e:
            print(e)
            return px.scatter()
        
        type_x = df[x_col].dtype
        type_y = df[y_col].dtype

        fig = px.scatter()

        if (type_x == 'float' or type_x == 'int' or type_x == 'int64') and (type_y == 'float' or type_y == 'int' or type_y == 'int64'):
            fig = px.scatter(df, x=x_col, y=y_col,color_discrete_sequence=['green'])

        if type_x == 'object' and (type_y == 'float' or type_y == 'int' or type_y == 'int64') :
            fig = px.box(df, x=x_col, y=y_col)

        if type_y == 'object' and (type_x == 'float' or type_x == 'int' or type_x == 'int64') :
            fig = px.box(df, x=y_col, y=x_col)

        if type_y == 'object' and type_x == 'object' :
            fig = px.histogram(df, x=x_col, color=y_col, barmode='group')

        
        return fig

    return px.scatter() 