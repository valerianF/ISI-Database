import os, re
import pandas as pd
from dash import html, dcc, dash_table

data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

# Lists page layout
layout = html.Div([

    html.H5('Submit your installation to the database'),

    html.Div([
        dash_table.DataTable(
            id='submit-table-AI',
            columns = [
                'Context', 'Sound Design', 'Intervention Visibility',
                'Lighting Design', 'Lifespan', 'Audience',
                'Visitor\'s Position', 'Role of Sound'
            ]
        )
    ]),

    html.P(style={'paddingBottom': '2cm'})
])
