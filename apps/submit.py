import os, re
import pandas as pd
import subprocess
from sqlalchemy import create_engine
from dash import html, dcc, dash_table, callback, Input, Output

# raw_engine = engine.raw_connection()
# my_df = pd.read_sql_query("SELECT * FROM submitted_isi_list;", raw_engine)

# Lists page layout
layout = html.Div([

    html.P(style={'paddingBottom': '1cm'}),

    html.H5('Submit your installation to the database'),
    
    html.P(style={'paddingBottom': '1cm'}),

    html.H2('Artistic Intention'),

    html.Div([
        dcc.Dropdown(
            id='dropdown_context',
            options = [
                {'label': 'Exhibition','value': 'CO_Exhibition'},
                {'label': 'Prototype','value': 'CO_Prototype'},
                {'label': 'Outdoor', 'value': 'CO_Outdoor'},
                {'label': 'Indoor','value': 'CO_Indoor'},
                {'label': 'School','value': 'CO_School'},
                {'label': 'Care-center','value': 'CO_Care'},
                {'label': 'Transportation','value': 'CO_Trans'}
                ],
            multi=True,
            placeholder="Context",
            style={
                    'height': '200%',
                    'width' : '200px'
                    }
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='dropdown_lifespan',
            options = [
                {'label': 'Ephemeral','value': 'LP_Ephemeral'},
                {'label': 'Semi-Permanent','value': 'LP_Temp'},
                {'label': 'Permanent', 'value': 'LP_Semi'}
                ],
            multi=False,
            placeholder="Lifespan",
            style={
                    'height': '200%',
                    'width' : '200px'
                    }
        ),
    ], style={'display': 'inline-block', 'paddingLeft': '0.5cm'}),

    html.Div([
        dcc.Dropdown(
            id='dropdown_audience',
            options = [
                {'label': 'All audiences','value': 'AU_Both'},
                {'label': 'Adults','value': 'AU_Adults'},
                {'label': 'Children', 'value': 'AU_Child'}
                ],
            multi=False,
            placeholder="Audience",
            style={
                    'height': '200%',
                    'width' : '200px'
                    }
        ),
    ], style={'display': 'inline-block', 'paddingLeft': '0.5cm'}),

    html.Div([
        dcc.Dropdown(
            id='dropdown_role',
            options = [
                {'label': 'Expressive','value': 'RS_Expr'},
                {'label': 'Informational','value': 'RS_Info'},
                {'label': 'Didactic', 'value': 'RS_Didactic'},
                {'label': 'Therapeutic', 'value': 'RS_Therapeutic'}
                ],
            multi=True,
            placeholder="Role of Sound",
            style={
                    'height': '200%',
                    'width' : '200px'
                    }
        ),
    ], style={'display': 'inline-block', 'paddingLeft': '0.5cm'}),

    html.P(style={'paddingBottom': '1cm'}),

    html.Button('Submit', id='submit-button', n_clicks=0),

    html.Div(id='output'),

    html.P(style={'paddingBottom': '2cm'})
])

@callback(Output('output', 'children'),
    [Input('dropdown_context', 'value'),
    Input('dropdown_lifespan', 'value'),
    Input('dropdown_audience', 'value'),
    Input('dropdown_role', 'value'),
    Input('submit-button', 'n_clicks')])
def submit_installation(co, lp, au, ro, n_clicks):
    ai = []

    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", "isi-database"], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip().replace("postgres", "postgresql")
    engine = create_engine(connuri)

    if n_clicks == 1:
        ai.append(
            {
                'co': co,
                'lp': lp,
                'au': au,
                'ro': ro
            })

        df = pd.DataFrame(data=ai)

        with engine.connect() as conn:
            df.to_sql("isi_list", con=engine, if_exists='append', index=False)

    return