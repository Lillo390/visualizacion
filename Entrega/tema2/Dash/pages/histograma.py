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
    html.H1("Representación por histograma"),
    dcc.Upload(
        id="upload-data-3",
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
            id="variable-2",
            options=[],
            value=None,
            labelStyle={"display": "inline-block", "marginRight": "10px"}
        ),
        html.Button(id="submit-button-2", children="Visualizar")
    ], style={"margin": "10px"}),
    dcc.Graph(id="histograma")
])

# Callback para cargar los datos del archivo CSV
@callback(
    Output("variable-2", "options"),
    [Input("upload-data-3", "contents")],
    [State("upload-data-3", "filename")]
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
                return []
        except Exception as e:
            print(e)
            return []

        # Crear las opciones para los RadioItems
        #options = [{"label": col, "value": col} for col in df.columns]
        options = df.columns
        #print(options)

        return options

    return []


# Callback para generar el gráfico
@callback(
    Output("histograma", "figure"),
    [Input("submit-button-2", "n_clicks")],
    [State("variable-2", "value"), State("upload-data-3", "contents"), State("upload-data-3", "filename")]
)
def generate_histo(n_clicks, x_col, contents, filename):
    
    if n_clicks is not None and x_col is not None and contents is not None:
        # Convertir los datos del archivo CSV en un DataFrame de Pandas
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            else:
                return px.histogram()
        except Exception as e:
            print(e)
            return px.histogram()

        # Generar el gráfico
        fig = px.histogram(df, x=x_col,color_discrete_sequence=['green'])

        return fig

    return px.histogram()