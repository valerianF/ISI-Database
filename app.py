import re
import dash
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from sunburst import appObj

"""
Run this file, then visit http://127.0.0.1:8050/ in your web browser.
For an offline check, run plot(fig).
Components required: python and the following librairies: dash, pandas and plotly
Next steps: 

- Improve tags (relate them to their parents)
- Visually organise tags according to their associated category
- Filter the graph in function of the filters or at least some filters
- Add a tab (or a radio element) that retrieve the associated tags for a given installation
- Display the total number of installations for the study
"""


root = 'D:/Files/OneDrive - McGill University/Classes/MUMT 609 - Project/ScriptAnimation/data/installationsList.csv'
data = pd.read_csv(root)



AI = appObj(data, 'Artistic Intention')
SD = appObj(data, 'System Design')
IN = appObj(data, 'Interaction')

AI.initiateArray()
SD.initiateArray()
IN.initiateArray()

data = SD.data
labellist = AI.labels[11:] + IN.labels[7:] + SD.labels[11:]
IDlist = AI.df['ids'][11:].tolist() + IN.df['ids'][7:].tolist() + SD.df['ids'][11:].tolist()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def doi_to_url(link):
    if re.match('10.', link):
        return 'https://doi.org/' + link
    elif re.match('DOI:', link):
        return re.sub('DOI:', 'https://doi.org/', link)
    elif re.match('doi:', link):
        return re.sub('doi:', 'https://doi.org/', link)
    else:
        return link

def make_list(values):
    sections = []
    rows = []
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
                    cell = html.Td(html.A(href=doi_to_url(value), children=doi_to_url(value)))                    
                else:
                    cell = html.Td(children=value)
                row.append(cell)
            rows.append(html.Tr(row))
    return rows


app.layout = html.Div(children=[

    html.H1(children='Interactive Sound Installations Database'),
            
    html.Div([
        dcc.RadioItems(
            id="select_plot",
            options=[
                {'label': 'Artistic Intention', 'value': 'AI'},
                {'label': 'Interaction', 'value': 'IN'},
                {'label': 'System Design', 'value': 'SD'}
                ],
            value='SD',
            labelStyle={'display': 'inline-block', 'cursor': 'pointer', 'margin-left':'1cm', 'font-size': '20px'}

            )
    ]),

    html.P(style={'padding-bottom': '0.5cm'}),  
            
    dcc.Graph(id='sunburst'),

    html.P(style={'padding-bottom': '1cm'}),     

    html.Div([
        dcc.Dropdown(
            id='dropdown_cat',
            options=[{'label': re.sub('<br>', ' ', i), 'value': i} for i in labellist],
            multi=True,
            placeholder="Select one or more categories",
            style={
                    'height': '200%',
                    'width' : '500px'
                    }
        )
    ]),

    html.P(style={'padding-bottom': '0.5cm'}),  

    html.Div(id='list_inst')
])
            
@app.callback(Output("sunburst", "figure"), 
              [Input("select_plot", "value")])
def update_figure(input_value):
    if input_value == 'AI':
        dframe = AI.df
        colorscale = 'Burg'
    elif input_value == 'SD':
       dframe = SD.df
       colorscale = 'Greens'
    elif input_value == 'IN':
       dframe = IN.df
       colorscale = 'Blues'
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
            insidetextorientation='radial',
            marker = dict(
                colors = np.log(dframe['values']),
                colorscale = colorscale
                )
        ))
    fig.update_layout(margin = dict(t=20, l=20, r=0, b=0))

    return fig


@app.callback(
    Output('list_inst', 'children'),
    [Input('sunburst', 'clickData'),
    Input('dropdown_cat', 'value')])
def display_list(clickData, values):
    rows = [] 
    if values is None or values == []:
        if clickData is None or len(clickData['points'][0]['id']) <= 6:
            return 'Click on a sub-category or choose it from the dropdown menu to get a list of the concerned installations.'
        elif len(clickData['points'][0]['id']) > 6:
            values = [clickData['points'][0]['label']]
            rows = make_list(values)

    elif values is not None and (clickData is None or len(clickData['points'][0]['id']) <= 6):
        rows = make_list(values)
        if rows == []:
            return 'No installation belong to those categories.'

    elif values is not None and clickData is not None:
        if len(clickData['points'][0]['id']) > 6:
            values.append(clickData['points'][0]['label'])
            rows = make_list(values)
        if rows == []:
            return 'No installation belong to those categories.'
    
    return  [
        html.H5('Chosen tags: '),
        html.H3([' | ' + re.sub('<br>', ' ', value) for value in values]),
        html.Table(
                [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                + rows
                )
            ]


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)  
    


            
            
            
        
            
            
            
        

