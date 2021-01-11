import dash

""" Import external CSS style sheet. 
Note than CSS files in /asset subfolder are automaticaly imported.
"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

""" Initiate the dash application """
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server