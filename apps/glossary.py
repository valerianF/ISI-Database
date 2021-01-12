import os
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc


# Glossary page layout
layout = html.Div([

    html.H5('Click on a term to display its definition.'),

    dcc.Link('Navigate to main page', href='/'),

    dcc.Link('List of installations', 
        href='/lists',
        style={'paddingLeft': '0.5cm'}
    ),


    html.P(style={'paddingBottom': '0.5cm'}),  

    html.Details([
        html.Summary('Artistic Intention', style={'fontSize': 35, 'fontFamily': 'FontBold'}),
        html.P("""Pictures the overall context informing the design process. Most of its 
        elements are often thought by the designer or the artist prior to the implementation 
        of an Interactive Sound Installation. """),
        html.Details([
            html.Summary('Context', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Information about the overall type of space in which the installation is built. 
                      Induced from the various contexts surrounding the corpus’ installations."""),
            html.Details([
                html.Summary('Outdoor Public Space'),
                html.P('Outdoor spaces accessible to all peoples such as plazas, squares or parks.')
            ]),
            html.Details([
                html.Summary('Indoor Public Space'),
                html.P('Indoor spaces accessible to all peoples such as libraries.')
            ]),
            html.Details([
                html.Summary('Exhibition'),
                html.P('The installation is/was exhibited, for instance at a gallery or in a conference.')
            ]),
            html.Details([
                html.Summary('School'),
                html.P('School from kindergarten to secondary school.')
            ]),
            html.Details([
                html.Summary('Prototype'),
                html.P('The installation has a temporary design that is subject to improvements.')
            ]),
            html.Details([
                html.Summary('Care Center'),
                html.P('Place dedicated to health care such as hospitals or nursing homes.')
            ]),
            html.Details([
                html.Summary('Transportation'),
                html.P('The installation is situated in a transportation means such as a car or a boat.')
            ]),
        ]),
        html.Details([
            html.Summary('Audience', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Type of audience targeted by the installation. Induced from the corpus."""),
            html.Details([
                html.Summary('Adults'),
                html.P("""Though children may or may not be able to access it, they are not 
                the primary target of the concerned installation.""")
            ]),
            html.Details([
                html.Summary('Children'),
                html.P('The concerned installation is specifically made for a young audience.')
            ]),
            html.Details([
                html.Summary('Both'),
                html.P('The concerned installation can be equally approched by all audiences.')
            ]),
        ]),
        html.Details([
            html.Summary('Lifespan', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Duration in which the installation was or is planned to remain
            active. It is a common approach to categorize sounding artwork, since it is determinant for
            the design process. 
            
            (Bandt, R. 2005. “Designing Sound in Public Space in Australia: A Comparative Study Based on
            the Australian Sound Design Project’s Online Gallery and Database.” Organised Sound
            10 (2): 129–40.)"""), 
            html.Details([
                html.Summary('Ephemeral')
            ]),
            html.Details([
                html.Summary('Temporary')
            ]),
            html.Details([
                html.Summary('Semi-permanent')
            ])      
        ])
    ], style={'maxWidth' : '800px'})
])