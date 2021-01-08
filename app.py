import re
import os
import dash
import pandas as pd
import numpy as np
import webbrowser
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sunburst import appObj

"""
After downloading this repository, run this file.
For an offline check, run plot(fig).
Components required: python and the following librairies: dash, pandas and plotly
Next steps: 

- Improve tags (relate them to their parents)
- Visually organise tags according to their associated category
- Filter the graph in function of the filters or at least some filters 
  (what the plot would look like for outdoor applications only?)
- Add a tab (or a radio element) that retrieve the associated tags for a given installation
- Add a tab with a Venn Diagram showing all potential relation between categories
- World map indicating the location of each installation
"""


""" Accessing the csv located in root, importing it to a pandas dataframe."""
root = os.path.join(os.getcwd(), 'data', 'installationsList.csv')
data = pd.read_csv(root)

""" Defining the sunburst objects."""
AI = appObj(data, 'Artistic Intention')
SD = appObj(data, 'System Design')
IN = appObj(data, 'Interaction')
FI = appObj(data, 'Field')

""" Initiate respective sunburst arrays."""
AI.initiate_arrays()
SD.initiate_arrays()
IN.initiate_arrays()
FI.initiate_arrays()

labellist = AI.labels[11:] + IN.labels[7:] + SD.labels[18:]
IDlist = AI.df['ids'][11:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][18:].tolist()
parentlist = AI.parentslabels[11:] + IN.parentslabels[7:] + SD.parentslabels[18:]

""" Import external CSS style sheet. 
Note than CSS files in /asset subfolder are automaticaly imported.
"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

""" Initiate the dash application """
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

""" Local functions """
def doi_to_url(link):
    """ Converts the doi into a proper url.
    If the input is a link, returns it unchanged.

    Parameters
    ----------
    link : str
        Doi number.
    """
    if re.match('10.', link):
        return 'https://doi.org/' + link
    elif re.match('DOI:', link):
        return re.sub('DOI:', 'https://doi.org/', link)
    elif re.match('doi:', link):
        return re.sub('doi:', 'https://doi.org/', link)
    else:
        return link

def make_list(values):
    """Creates a html list containing publications belonging
    to the input categories.

    Parameters
    ----------
    values : list
        Category or categories selected.
    """

    sections = []
    rows = []

    if values is None or values == []:
        for i in range(0, len(data)):
            row = []
            for col2 in data.columns[[1, 2, 6, 5, 3]]:
                value = data.iloc[i][col2]
                if col2 == 'Hyperlink':
                    cell = html.Td(html.A(href=doi_to_url(value), children='Click Here'))                    
                else:
                    cell = html.Td(children=value)
                row.append(cell)
            rows.append(html.Tr(row))

    else:        
        for value in values:
            section = IDlist[labellist.index(value)]
            sections.append(section)
        for i in range(0, len(data)):
            verif = np.zeros(len(sections))
            for s in range(0, len(sections)):              
                if data.iloc[i][sections[s]] == 1:
                    verif[s] = 1
                elif data.iloc[i][sections[s]] != 1:
                    continue
            if 0 not in verif:              
                row = []
                for col2 in data.columns[[1, 2, 6, 5, 3]]:
                    value = data.iloc[i][col2]
                    if col2 == 'Hyperlink':
                        cell = html.Td(html.A(href=doi_to_url(value), children='Click Here'))                    
                    else:
                        cell = html.Td(children=value)
                    row.append(cell)
                rows.append(html.Tr(row))
    return rows

""" Creation of the html app layout."""
app.layout = html.Div(children=[

    html.H1(children='Interactive Sound Installations Database'),

    html.H5(children=str(len(AI.data)) + ' installations are currently reviewed'),

    html.P(style={'padding-bottom': '0.5cm'}),  
            
    html.Div([
        dcc.RadioItems(
            id="select_plot",
            options=[
                {'label': 'Artistic Intention', 'value': 'AI'},
                {'label': 'Interaction', 'value': 'IN'},
                {'label': 'System Design', 'value': 'SD'},
                {'label': 'Subject Area', 'value': 'FI'}
                ],
            value='AI', # Initial Sunburst: Artistic Intention
            labelStyle={'display': 'inline-block', 'cursor': 'pointer', 'margin-left':'1cm', 'font-size': '20px'}

            )
    ]),

    html.P(style={'padding-bottom': '0.5cm'}),  
            
    dcc.Graph(id='sunburst'),

    html.P(style={'padding-bottom': '1cm'}),     

    html.Div([
        dcc.Dropdown(
            id='dropdown_cat',
            options = [
                {
                'label': re.sub('<br>', ' ', parentlist[i]) + ' | ' + re.sub('<br>', ' ', labellist[i]),
                'value': labellist[i]
                } for i in range(0, len(labellist))
                ],
            multi=True, # Makes in sort that several categories can be selected
            placeholder="Select one or more categories",
            style={
                    'height': '200%',
                    'width' : '500px'
                    }
        ),
        # html.Button('Take a Snapshot', id='snap-button', n_clicks=0, style={'margin-left': '30px'}),
    ], style={'display': 'flex'}),

    html.P(style={'padding-bottom': '0.5cm'}),  

    html.Div(id='list_inst')
])

""" Callback functions."""          
@app.callback(Output("sunburst", "figure"), 
              [Input("select_plot", "value")])
            #   Input('snap-button', 'n_clicks')])
def update_figure(input_value):
    """ Updates the sunburst chart in function of the radio button selected.
    If the snapshot html button is triggered (currently deactivated), saves a svg plot of the corresponding dimension.

    Parameters
    ----------
    input_value : str
        Type of radio button selected.
    n_clicks : int
        Number of clicks for the snapshot html button.
    """
    if input_value == 'AI':
        dframe = AI.df
        colorscale = 'Burg'
    elif input_value == 'SD':
        dframe = SD.df
        colorscale = 'Greens'
    elif input_value == 'IN':
        dframe = IN.df
        colorscale = 'Blues'
    elif input_value == 'FI':
        dframe = FI.df
        colorscale = 'GnBu_r'
        marker = None
    if input_value != 'FI':
        marker = dict(
        colors = np.log(dframe['values']),
        colorscale = colorscale
        )
    fig = go.Figure()
    fig.add_trace(go.Sunburst(
            ids = dframe['ids'], 
            labels=dframe['labels'],
            parents=dframe['parents'],
            branchvalues='total',
            values=dframe['values'],
            hovertemplate='<b>%{label} </b> <br>Elements concerned: %{value}<br>',
            maxdepth=3,
            name = '',
            # insidetextorientation='radial',
            marker = marker
        ))
    fig.update_layout(margin = dict(t=20, l=20, r=0, b=0))

    # changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # if 'snap-button' in changed_id:
    #     im_name = 'snapshot_' + input_value + '.svg'
    #     if not os.path.exists("snapshots"):
    #         os.mkdir("snapshots")
    #     fig.write_image(os.path.join('snapshots', im_name))

    return fig

@app.callback(
    Output('list_inst', 'children'),
    [Input('sunburst', 'clickData'),
    Input('dropdown_cat', 'value'),
    Input('select_plot', 'value')])
def display_list(clickData, values, plotType):
    """ Displays the html list in fuction of the callback inputs.
    No list is (yet) displayed for the Field sunburst.

    Parameters
    ----------

    clickData : list
        Data about the sunburt's clicked section.
    values : list
        Selected data from the dropdown list.
    plotType : str
        Type of sunburst selected on the radio buttons.
    """
    rows = []
    parents = []
    str_values = []

    if plotType != 'FI':
        if values is None or values == []:
            if clickData is None or len(clickData['points'][0]['id']) <= 6:
                rows = make_list(values)
                return  [
                    html.H6('Click on a sub-category or choose it from the dropdown menu to filter the list below.'),
                    html.Table(
                            [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                            + rows
                            )
                        ]  
            else:
                values = [clickData['points'][0]['label']]
                parent = clickData['points'][0]['parent']
                parents.append(parent)
                rows = make_list(values)

        else:
            if clickData is None or len(clickData['points'][0]['id']) <= 6:
                for value in values:
                    parents.append(parentlist[labellist.index(value)])     
                try:
                    rows = make_list(values)
                except ValueError:
                    return

            else:
                for value in values:
                    parents.append(parentlist[labellist.index(value)])
                parent = clickData['points'][0]['parent']
                parents.append(parent)
                values.append(clickData['points'][0]['label'])
                try:
                    rows = make_list(values)
                except ValueError:
                    return

        if rows == []:
            return 'No installation belongs to all those categories.'
        

        for i in range(0, len(parents)):
            str_values.append([re.sub('<br>', ' ', parents[i]) + ' | ' 
                + re.sub('<br>', ' ', values[i])])
        
        if len(values) > 1:
            return  [
                html.H5('Chosen tags: '),
                html.H3([str_values[i][0] + ' ― ' for i in range(0, len(str_values)-1)] + [str_values[-1][0]]),
                html.H5(str(len(rows)) + ' results'),
                html.Table(
                        [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                        + rows
                        )
                    ]
        elif len(values) == 1:
            return  [
                html.H5('Chosen tag: '),
                html.H3([value[0] for value in str_values]),
                html.H6(str(len(rows)) + ' results'),
                html.Table(
                        [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                        + rows
                        )
                    ]   
   
""" Run the app. Launch the web page."""
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) 