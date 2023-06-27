from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True,suppress_callback_exceptions = True)

# Define navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tabla", href="/tabla", style={"color": "white"})),
        dbc.NavItem(dbc.NavLink("Histograma", href="/histograma", style={"color": "white"})),
        dbc.NavItem(dbc.NavLink("Variable vs Variable", href="/1v1", style={"color": "white"})),
    ],
    brand=html.A("Menú principal", href="/", className="navbar-brand", style={"color": "white"}),
    sticky="top",
    color='green'
)



app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)

