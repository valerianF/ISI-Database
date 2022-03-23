import os, re
import dash
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

from apps import glossary, lists, submit
from apps.lists import doi_to_url
from apps.sunburst import appObj

"""
After downloading this repository, run this file.
For an offline check, run plot(fig).
Components required: python and the following librairies: dash, pandas and plotly
Next steps: 

- Improve tags (relate them to their parents)
- Visually organise tags according to their associated category
- Filter the graph in function of the filters or at least some filters 
  (e.g. what the plot would look like for outdoor applications only?)
- Add a tab (or a radio element) that retrieve the associated tags for a given installation
- Add a tab with a Venn Diagram showing all potential relation between categories
- World map indicating the location of each installation
- Export local functions to external file (too many rows in the app)
"""

""" Accessing the csv located in repo, importing it to a pandas dataframe."""
data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

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

labellist = AI.labels[12:] + IN.labels[7:] + SD.labels[18:] + FI.labels[13:]
IDlist = AI.df['ids'][12:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][18:].tolist() + FI.labels[13:]
parentlist = AI.parentslabels[12:] + IN.parentslabels[7:] + SD.parentslabels[18:] + FI.parents[13:]

""" Import external CSS style sheet. 
Note than CSS files in /asset subfolder are automaticaly imported.

"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

""" Initiate the dash application """
app = dash.Dash(__name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    title='ISI Database',
    update_title='Loading...')
server = app.server

""" Local functions """
def make_list(values, plotType):
    """Creates a html list containing publications belonging
    to the input categories.

    Parameters
    ----------
    values : list
        Category or categories selected.
    plotType : str
        Type of Sunburst plot. 
    """

    sections = []
    rows = []
  
    for value in values:
        try:
            section = IDlist[labellist.index(value)]
            sections.append(section)
        except ValueError:
            sections.append(value)

    for i in range(0, len(data)):
        verif = np.zeros(len(sections))
        for s in range(0, len(sections)):
            field = str(data.iloc[i]['Field']).split('; ')
            for f in range(0, len(field)):
                if re.sub(' ', '<br>', field[f]) == sections[s]:
                    verif[s] = 1
                else:
                    continue 
            try:                           
                if data.iloc[i][sections[s]] == 1:
                    verif[s] = 1
                elif data.iloc[i][sections[s]] != 1:
                    continue
            except KeyError:
                continue

        if 0 not in verif:              
            row = []
            for col2 in data.columns[[1, 2, 6, 5, 3]]:
                value = data.iloc[i][col2]
                if col2 == 'Hyperlink':
                    cell = html.Td(html.A(href=doi_to_url(value), children='Click Here', target='_blank'))                    
                else:
                    cell = html.Td(value)
                row.append(cell)
            rows.append(html.Tr(row))
    return rows

""" Application layout."""
# Index layout
app.layout = html.Div(className="app_layout",
    children=[

    # represents the url bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.Div(className="banner", 
        children=[

        html.H1("Interactive"),
        html.Br(),
        html.H1("Sound"),
        html.Br(),
        html.H1("Installations"),
        html.Br(),
        html.H1("Database"),

        html.P(style={'paddingBottom': '1cm'}), 

        dcc.Link('HOME', href='/', className='banner_link'),
        html.P(style={'paddingBottom': '0.5cm'}),  
        dcc.Link('GLOSSARY', href='/glossary', className='banner_link'),
        html.P(style={'paddingBottom': '0.5cm'}),  
        dcc.Link('LIST OF INSTALLATIONS', href='/lists',className='banner_link'),
        # dcc.Link('Submit', 
        #     href='/submit',
        #     style={'paddingLeft': '0.5cm'}
        # ),
    ]),

    html.Div(id='page-content', className='page_content'),

    html.Div(className="footer", 
        children=[
        html.P(['Designed by ',
            html.A(href='https://www.mcgill.ca/music/valerian-fraisse',
                children='Valérian Fraisse', target='_blank'),
            ' with the support of ',
            html.A(href='https://www.mcgill.ca/sis/people/faculty/guastavino',
                children='Catherine Guastavino', target='_blank'),
            ' and ',
            html.A(href='https://www.mcgill.ca/music/marcelo-m-wanderley',
                children='Marcelo Wanderley', target='_blank'),
            '.',
            html.Br(),
            'The source code is available on ',
            html.A(href='https://github.com/valerianF/ISI-Database',
                children='GitHub', target='_blank'),
            '.'], style={'fontSize': '12px'}),

        html.P(['This work is licensed under a ',
            html.A(rel='license', href='http://creativecommons.org/licenses/by-nc-sa/4.0/',
                children='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License',
                target='_blank'),
            '.'], style={'fontSize': '12px'})
    ])
])

# Main page layout
layout_main = html.Div([

    # html.H5(str(len(data)) + ' installations are currently reviewed. All the terms below are explained in the glossary.'),

    # html.P(style={'paddingBottom': '0.5cm'}),  
            
    html.Div(className="page_left", 
    children=[

        dcc.Graph(id='sunburst'),

        html.P(style={'paddingBottom': '0.5cm'}),  
                
        html.Div(className='radio_buttons',
            children=[
                dcc.RadioItems(
                    id="select_plot",
                    options=[
                        {'label': 'Artistic Intention', 'value': 'AI'},
                        {'label': 'Interaction', 'value': 'IN'},
                        {'label': 'System Design', 'value': 'SD'}
                        # {'label': 'Subject Area', 'value': 'FI'}
                        ],
                    value='AI', # Initial Sunburst: Artistic Intention
                    className='radiobutton-group',
                    ),
                    html.Span(className='checkmark'),
        ]),

        html.P(style={'paddingBottom': '1cm'}), 

    ]),    

    html.Div(className='page_right',
    children=[

        html.Div([
            dcc.Dropdown(
                id='dropdown_cat',
                options=[
                    {
                    'label': re.sub('<br>', ' ', parentlist[i]) + ' | ' + re.sub('<br>', ' ', labellist[i]),
                    'value': labellist[i]
                    } for i in range(0, len(labellist))
                    ],
                multi=True, # Makes in sort that several categories can be selected
                placeholder="Select one or more categories",
                style={
                        'height': '400%',
                        'width' : '400px'
                        }
            ),
            # html.Button('Take a Snapshot', id='snap-button', n_clicks=0, style={'marginLeft': '30px'}),
        ], style={'display': 'flex'}),

        html.P(style={'paddingBottom': '0.5cm'}),  

        html.Div(id='list_inst', className='list_inst'),

        html.P(style={'paddingBottom': '2cm'}),
    ])
])

""" Callback functions."""  

# Index callbacks
@app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
def display_page(pathname):
    """ Updates page content in function of chosen url.

    Parameters
    ----------
    pathname : str 
        Page to redirect to. 
    """
    if pathname == '/':
        return layout_main
    if pathname == '/glossary':
        return glossary.layout
    if pathname == '/lists':
        return lists.layout
    if pathname == '/submit':
        return submit.layout
    else:
        return layout_main


# Main page callbacks
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
            # hovertemplate='<b>%{label} </b> <br>Elements concerned: %{value}<br>',
            hoverinfo = 'skip',
            maxdepth=3,
            name = '',
            marker = marker
        ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                    font=dict(family='Roboto'),
                    autosize=False,
                    width=500,
                    height=500)   

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

    if values is None or values == []:
        if clickData is None or (len(clickData['points'][0]['id']) <= 6 and plotType != 'FI') or clickData['points'][0]['id'] in parentlist:    
            return  [html.H6('Click on a sub-category or choose it from the dropdown menu to get a list of the corresponding installations.')] 
        else:
            values = [clickData['points'][0]['label']]
            parent = clickData['points'][0]['parent']
            parents.append(parent)
            rows = make_list(values, plotType)

    else:
        if clickData is None or (len(clickData['points'][0]['id']) <= 6 and plotType != 'FI') or clickData['points'][0]['id'] in parentlist:
            for value in values:
                parents.append(parentlist[labellist.index(value)])     
            rows = make_list(values, plotType)

        else:
            for value in values:
                parents.append(parentlist[labellist.index(value)])
            parent = clickData['points'][0]['parent']
            parents.append(parent)
            values.append(clickData['points'][0]['label'])
            rows = make_list(values, plotType)

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

   
""" Run the app. """
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) 