import os, re
import pandas as pd
from dash import dcc, html

data = pd.read_csv(os.path.join(os.getcwd(), 'data', 'installationsList.csv'))

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

def make_list():
    sections = []
    rows = []

    for i in range(0, len(data)):
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

rows = make_list()

# Lists page layout
layout = html.Div([

    html.H5(str(len(data)) + ' installations are currently reviewed'),

    dcc.Link('Main page', href='/'),

    dcc.Link('Glossary', 
        href='/glossary',
        style={'paddingLeft': '0.5cm'}
    ),

    dcc.Link('Network visualization', 
        href='/network',
        style={'paddingLeft': '0.5cm'}
    ),

    html.P(style={'paddingBottom': '0.5cm'}),

    html.Table(
            [html.Th(col) for col in data.columns[[1, 2, 6, 5, 3]]]
            + rows
    ),

    html.P(style={'paddingBottom': '2cm'}),

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
