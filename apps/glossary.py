import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Glossary page layout
layout = html.Div([

    html.H5('Click on a term to display its definition.'),

    dcc.Link('Navigate to main page', href='/'),

    html.P(style={'paddingBottom': '0.5cm'}),  

    html.Details([
        html.Summary('Term to define', className = "tree-nav__item-title"),
        html.P('Definition', className = "tree-nav__item is-expandable")
    ]),


])