import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Glossary page layout
layout = html.Div([
    html.H5('Glossary'),

    dcc.Link('Navigate to main Page', href='/'),

    html.P(style={'paddingBottom': '0.5cm'}),  

    html.Details([
        html.Summary('Term to define'),
        html.P('caca prout.')
    ]),

    html.Details([
        html.Summary('Term to define'),
        html.P('caca prout.')
    ])

])