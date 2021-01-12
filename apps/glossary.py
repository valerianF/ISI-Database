import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def make_details(dataframe):
    return

# Glossary page layout
layout = html.Div([

    html.H5('Click on a term to display its definition.'),

    dcc.Link('Navigate to main page', href='/'),

    html.P(style={'paddingBottom': '0.5cm'}),  

    html.Details([
        html.Summary('Artistic Intention', style={'fontSize': 35, 'fontFamily': 'FontBold'}),
        html.Details([
            html.Summary('Context', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Information about the overall type of space in which the installation is built. 
                      Induced from the various contexts surrounding the corpus’ installations."""),
            html.Details([
                html.Summary('Outdoor Public Space'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('Indoor Public Space'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('Exhibition'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('School'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('Prototype'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('Care Center'),
                html.P('Definition')
            ]),
            html.Details([
                html.Summary('Transportation'),
                html.P('Definition')
            ])
            
        ])
    ]),

])