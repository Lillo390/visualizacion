import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='Visualizador de archivos csv'),
    html.Div(children='''
         Para visualizar el archivo, primero selecciona el tipo de representación y después carga el archivo.
    '''),
    html.Br(),
    html.Img(src='./assets/csv_image.png',style={'height':'20%', 'width':'20%'})

])