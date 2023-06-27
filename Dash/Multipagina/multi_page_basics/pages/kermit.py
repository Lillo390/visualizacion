# example of matching a path that starts with "shapshot-"

import dash
from dash import html

dash.register_page(
    __name__,
    path_template="/kermit",
)

layout = html.Div(["Home Page", html.Img(src="/assets/kermit.jpeg", height="50px")])


