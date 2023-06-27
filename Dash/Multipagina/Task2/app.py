import dash
import dash_bootstrap_components as dbc
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import pandas as pd
import io 

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Más gráficas",
    ),
    brand="Exploración dataframe",
    color="primary",
    dark=True,
    className="mb-2",
)

upload = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra o selecciona un archivo CSV'
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    )

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(content, filename):
    if content is not None:
        content_string = content[0].decode("utf-8")
        df = pd.read_csv(io.StringIO(content_string))
        return html.Div([
            html.H5(filename),
            html.Table(
                # Header
                [html.Tr([html.Th(col) for col in df.columns])] +

                # Body
                [html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ]) for i in range(len(df))]
            )
        ])



app.layout = dbc.Container(
    [upload,navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
