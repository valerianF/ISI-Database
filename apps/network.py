import os
import re
import pandas as pd
import numpy as np
import dash_cytoscape as cyto
from dash import dcc, html, Input, Output, callback

from apps.lists import doi_to_url
from apps.sunburst import appObj

""" Importing the datasheet into a pandas dataframe """
data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

""" Defining the sunburst objects and label arrays."""
AI = appObj(data, 'Artistic Intention')
SD = appObj(data, 'System Design')
IN = appObj(data, 'Interaction')
FI = appObj(data, 'Field')

""" Initiate arrays"""
AI.initiate_arrays()
SD.initiate_arrays()
IN.initiate_arrays()
FI.initiate_arrays()

""" Define categories for composite links """
multi_cats = ["TS_", "LS_", "SD_"]

""" Setting lists. Hard to automatize..."""
labellist = AI.labels[12:] + IN.labels[9:] + SD.labels[18:] + FI.labels[13:]
IDlist = AI.df['ids'][12:].tolist() + IN.df['ids'][9:].tolist() + SD.df['ids'][18:].tolist() + FI.labels[13:]
parentlist = AI.parentslabels[12:] + IN.parentslabels[9:] + SD.parentslabels[18:] + FI.parents[13:]

linkIDlist0 = AI.df['ids'][1:12].tolist() + IN.df['ids'][1:7].tolist() + SD.df['ids'][1:18].tolist()
linkparentlist = AI.labels[1:12] + IN.labels[1:7] + SD.labels[1:18]

linkIDlist = [x for x in linkIDlist0 if (x not in ['IT', 'SP', 'IDof', 'ODof'] and not x.startswith(tuple(multi_cats)))]
linkparentlist = [x for x in linkparentlist if linkparentlist.index(x) in [linkIDlist0.index(n) for n in linkIDlist]]

compIDlist = ['TS_Ima', 'TS_Con', 'TS_Det', 'TS_Ide', 'TS_Ser', 'TS_Mic', 'TS_Mec', 'TS_Env', 'TS_Bio', 'TS_Ele']
complabellist = ['Image Sensors', 'Controllers', 'Detectors', 'Identification', 'Server-Client', 'Microphones',
    'Force and Pressure Sensors', 'Environment Sensors', 'Bio-Signals Sensors', 'Electric, Magnetic Sensors']

""" Network object """
class netObj:
    def __init__(self, data):
        self.data = data
        self.len = len(self.data)
        self.elements = []
        self.stylesheet = []
        self.colors = []
        self.parents = []
        self.cat_check = True

    def create_network(self, keys=None, parent=None):
        """ Create network parents and children nodes and edges. 

        Parameters
        ----------
        keys : list
            Specific taxa from which corresponding nodes are retrieved
        parent : str
            If assigned, groups nodes together in function of the taxon.

        """

        self.parents = []
        parents_f = []
        self.colors = ['red', 'blue', 'green','magenta', 'cyan', 'indigo', 'saddlebrown', 'darkorange',
            'darkolivegreen', 'dimgray', 'black']
        self.elements = []
        self.stylesheet = []
        shared_parents = []
        # compound_parents = []
        nodes_ind = []
        self.multi_cats = ["TS"] #Categories for which we only want to assess sub-category


        # Return empty elements and stylesheet if no filters
        if (keys == None or keys == []) and (parent == None or parent == []):
            return

        # Special parent lists
        if parent == "SP_N":
            parent = ['SP_Num', 'SP_Hea', 'SP_Cnt']
        elif parent == "SP_D":
            parent = ['SP_Pnt', 'SP_Dir']
        elif parent == "IODof":
            parent = ['IDof', 'ODof']

        # Initialize parents list
        if type(parent) == str:
            self.init_parents(parent, keys)
        elif type(parent) == list:
            for p in parent:
                self.init_parents(p, keys)

        self.parents = list(set(self.parents))

        # If too much links are chosen
        if len(self.parents) > len(self.colors):
            self.cat_check = False
            return

        # Determine filtered installations' position in list
        if keys == [] or keys is None:
            nodes_ind = np.linspace(0, self.len-1, self.len)
        else:
            for n in range(self.len):
                values = [self.data.loc[n, key] for key in keys]
                if all(v == 1 for v in values):
                    nodes_ind.append(n)
        
        # Prior evaluation of shared parents
        array = np.array(nodes_ind)
        for i in nodes_ind:
            array = np.delete(array, np.where(array == i))
            node_parent_i = self.evaluate_parents(i)
            if node_parent_i != []:
                for j in array:
                    node_parent_j = self.evaluate_parents(j)
                    if node_parent_j != []:               
                        for p_i in node_parent_i:
                            for p_j in node_parent_j:
                                if p_i == p_j:
                                    shared_parents.append(p_i)

        # Determine which category to set as a compound
        # for parent in self.parents:
        #     if shared_parents.count(parent) > 5:
        #         compound_parents.append(parent)
  
        # Add nodes
        for i in nodes_ind:
            node_parent_i = self.evaluate_parents(i)
            self.elements.append(dict(
                data=dict(
                    id=self.data.loc[i, 'ID'],
                    label=self.data.loc[i, 'Name'],
                    parent=node_parent_i
                # grabbable=False
                )
            ))


        # Return only nodes if no parents
        if parent == None or parent == []:
            return
        
        # Edge elements
        array = np.array(nodes_ind)
        for i in nodes_ind:
            array = np.delete(array, np.where(array == i))
            node_parent_i = self.evaluate_parents(i)

            # Continue if node doesn't have any parents 
            if node_parent_i == []:
                continue
            
            # Evaluate remaining installations for siblings
            for j in array:
                node_parent_j = self.evaluate_parents(j)                  

                n_p = 0
                for p_i in node_parent_i:
                    for p_j in node_parent_j:
                        if p_i == p_j:
                            n_p += 1
                            # Add Edges for Nodes with same parent
                            if n_p == 1:
                                self.add_edge(i, j, p_j)
                            if n_p == 2:
                                self.add_edge(i, j, p_j, " bezier")
                            if n_p == 3:
                                self.add_edge(i, j, p_j, " bezier1")
                            if n_p == 4:
                                self.add_edge(i, j, p_j, " bezier2")

        # Generate Compound Elements and Stylesheets
        # if compound_parents != []:
        #     for parent in compound_parents:
        #         self.elements.append(dict(
        #                             data=dict(
        #                                 id=parent
        #                             ), 
        #                         classes= self.colors[self.parents.index(parent)]
        #                         ))
        #         self.stylesheet.append(dict(
        #             selector = '$node > node' + self.colors[self.parents.index(parent)],
        #             style = {
        #                 'background-color': self.colors[self.parents.index(parent)],
        #                 'background-opacity': '0.2',
        #                 'shape': 'roundrectangle',
        #                 'text-background-color': self.colors[self.parents.index(parent)],
        #                 'text-background-opacity': '0.2',
        #                 'border-width': 0.2,
        #             }
        #         ))

        # Stylesheets
        self.stylesheet.append(dict(
            selector = 'node',
            style = {
                'label': 'data(label)',
                'border-width': '3',
                'border-style': 'solid',
                'border-color': 'black',
                'color': 'black',
                'text-background-color': 'white',
                'text-background-opacity': '0.8',
                'text-backgroun-shape': 'round-rectangle',
                'text-margin-y': '-5px',
                'font-family': 'FontBold, sans-serif'
            }
        ))

        self.stylesheet.append(dict(
            selector = ':selected',
            style = {
                "border-width": 10,
                'background-color': 'white'
                }
        ))

        self.stylesheet.append(dict(
            selector = ':unselected',
            style = {
                "border-width": 3,
            }
        ))

        for i in range(len(self.elements)):
            try:
                for j in range(len(self.elements[i]['data']['parent'])):
                    if self.elements[i]['data']['parent'][j] is not [] and self.elements[i]['data']['parent'][j] not in shared_parents:
                        self.elements[i]['classes'] = "no_siblings_" + self.colors[self.parents.index(self.elements[i]['data']['parent'][j])]
                        self.stylesheet.append(dict(
                            selector = "node.no_siblings_" + self.colors[self.parents.index(self.elements[i]['data']['parent'][j])],
                            style = {
                                'background-color': self.colors[self.parents.index(self.elements[i]['data']['parent'][j])]
                            }
                        ))
            except KeyError:
                continue
                            
        for parent in self.parents:
            self.stylesheet.append(dict(
                selector = 'edge.' + self.colors[self.parents.index(parent)],
                style = {
                    'line-color': self.colors[self.parents.index(parent)]
                }
            ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": 8,
                "control-point-weights": 0.5              
            }
        ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier1',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": -8,
                "control-point-weights": 0.5             
            }
        ))

        self.stylesheet.append(dict(
            selector = 'edge.bezier2',
            style = {
                "curve-style": "unbundled-bezier",
                "control-point-distances": -16,
                "control-point-weights": 0.5             
            }
        ))

    # Local functions
    def evaluate_parents(self, n):
        node_parent = []
        for col in self.parents:
            for column in self.data.columns:
                if col in column:
                    if self.data.loc[n, column] == 1:
                        node_parent.append(col)
        return list(set(node_parent))

    def add_edge(self, i, j, node_parent, classes = ""):
        self.elements.append(dict(
        data=dict(
            source=self.data.loc[i, 'ID'],
            target=self.data.loc[j, 'ID'],
            label=node_parent
        ),
        classes= self.colors[self.parents.index(node_parent)] + classes
        ))

    def init_parents(self, p, keys):
        for col in self.data:
            if p in col:
                for i in range(self.len):
                    values_i = [self.data.loc[i, key] for key in keys]
                    if all(v == 1 for v in values_i):
                        if self.data.loc[i, col] == 1:
                            if col not in self.parents:
                                if p not in self.multi_cats[0]:
                                    self.parents.append(col)
                                elif p in self.multi_cats[0]:
                                    self.parents.append(col[0:6])



""" Application Layout """
layout = html.Div([

    html.H2('Interactive Sound Installations Database | Network Visualization'),

    dcc.Link('Main page', href='/'),

    dcc.Link('Glossary', 
        href='/glossary',
        style={'paddingLeft': '0.5cm'}
    ),

    dcc.Link('List of installations', 
        href='/lists',
        style={'paddingLeft': '0.5cm'}
    ),

    html.Div([
        cyto.Cytoscape(
            id='main_network',
            layout={
                'name':'cose',
                'nodeDimensionsIncludeLabels': 'true'
                },
            style={'font-family': 'FontBold, sans-serif'},
            elements = [],
            stylesheet = [],
            minZoom=0.3,
            maxZoom=1
        )
    ]),

    html.Div(
        id='network_legend',
        className = 'legend'
    ),

    html.P(style={'paddingBottom': '0cm'}), 

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown_link',
                options = [
                    {
                    'label': re.sub('<br>', ' ', linkparentlist[i]),
                    'value': linkparentlist[i]
                    } for i in range(0, len(linkparentlist))
                    ],
                multi=True, # A single category to filter installations
                placeholder="Select one or more categories to link installations",
                style={
                        'height': '200%'
                        }
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='dropdown_filter',
                options = [
                    {
                    'label': re.sub('<br>', ' ', parentlist[i]) + ' | ' + re.sub('<br>', ' ', labellist[i]),
                    'value': labellist[i]
                    } for i in range(0, len(labellist))
                    ],
                multi=True, # Makes in sort that several categories can be selected
                placeholder="Select one or more categories to filter installations",
                style={
                        'height': '200%'
                        }
            ),
        ], style={'width': '49%', 'display': 'inline-block', 'margin-left': '2%'}),
    ]),
    
    html.P(style={'paddingBottom': '0cm'}),

    html.Div(id='tap_node')

])

# Network callbacks
@callback([
    Output('main_network', 'elements'),
    Output('main_network', 'stylesheet'),
    Output('network_legend', 'children'),
    Output('main_network', 'style')
    ], [Input('dropdown_filter', 'value'),
    Input('dropdown_link', 'value')])
def update_elements(input_cat, input_link):

    output_values = []
    output_link = []
    legend = ""
    content = []

    if (input_cat is not None and input_cat != []) and (input_link is not None and input_link != []):
        
        for input_value in input_cat:
            output_values.append(IDlist[labellist.index(input_value)]) 

        for link in input_link:
            output_link.append(linkIDlist[linkparentlist.index(link)])    
        
        net = netObj(data)
        net.create_network(output_values, parent=output_link)

        if not net.cat_check:
            return [], [], [html.H4("""You have chosen too many categories to link installations. Try to remove one or more categories.""")], {'width': '100%', 'height': '0vh'}

        elements = net.elements
        stylesheet = net.stylesheet

        for link in output_link:
            if output_link == 'TS':
                legend += ' | Type of Input Device'
            else:
                legend += ' | ' + re.sub('<br>', ' ', linkparentlist[linkIDlist.index(link)])

        legend = legend[2:]

        children = [
            html.Legend(html.H4(html.B(legend)))
        ]

        for parent in net.parents:
            if 'TS' in parent:
                children.extend([
                    html.Span(className=net.colors[net.parents.index(parent)]),
                    html.Li(re.sub('<br>', ' ', complabellist[compIDlist.index(parent)]))
                ])
            else:
                children.extend([
                    html.Span(className=net.colors[net.parents.index(parent)]),
                    html.Li(re.sub('<br>', ' ', labellist[IDlist.index(parent)]))
                ])

        return elements, stylesheet, [html.Fieldset(children)], {'width': '100%', 'height': '70vh'}
    else:
        return [], [], [html.H4("""Please select at least a category on each the dropdown lists below.""")], {'width': '100%', 'height': '0vh'}

@callback(
    Output('tap_node', 'children'),
    [Input('main_network', 'tapNodeData')])
def tap_node_data(tapdata):

    if tapdata is not None and tapdata != []:
        for i in range(0, len(data)):
            if data.iloc[i]['Name'] == tapdata['label']:
                break

        row = []
        for col in data.columns[[1, 2, 6, 5, 3]]:
            value = data.iloc[i][col]
            if col == 'Hyperlink':
                cell = html.Td(html.A(href=doi_to_url(value), children='Click Here', target='_blank'))                    
            else:
                cell = html.Td(value)
            row.append(cell)
        return [
            html.H5("You recently tapped this installation:"),
            html.Table(
                [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
                + [html.Tr(row)]
            )
        ] 




