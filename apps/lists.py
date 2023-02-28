import os, re
import pandas as pd
from dash import html, dcc

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
        for col2 in data.columns[[3, 2, 6, 5]]:
            value = data.iloc[i][col2]
            if col2 == 'Hyperlink':
                cell = html.Td(html.A(href=doi_to_url(value), children=data.iloc[i][1], target='_blank',
                className='link_list'))                    
            else:
                cell = html.Td(value)
            row.append(cell)
        rows.append(html.Tr(row))
    return rows

rows = make_list()

# Lists page layout
layout = html.Div([
    
    html.Div(className="banner",
        children=[

        html.H1(className='banner_header', children=["Interactive Sound Installations Database"]),

        dcc.Link('HOME', href='/', className='banner_link'),
        html.P(), 
        dcc.Link('GLOSSARY', href='/glossary', className='banner_link'),
        html.P(), 
        dcc.Link('LIST OF INSTALLATIONS', href='/lists', className='banner_link_fixed'),
    ]), 

    html.Div(className="page_lists",
    children =[
    html.P(style={'paddingBottom': '0.5cm'}),

    html.Table(
            [html.Th(col) for col in ['Name', 'Creator(s)', 'Year', 'Source']]
            + rows
    ),

    html.P(style={'paddingBottom': '2cm'}),

    html.P(className='credits', children = 
    ['✍ Created by ',
            html.A(href='https://www.mcgill.ca/music/valerian-fraisse',
                children='Valérian Fraisse', target='_blank', className='link_credits'),
            ' with the support of ',
            html.A(href='https://www.mcgill.ca/sis/people/faculty/guastavino',
                children='Catherine Guastavino', target='_blank', className='link_credits'),
            ' and ',
            html.A(href='https://www.mcgill.ca/music/marcelo-m-wanderley',
                children='Marcelo Wanderley', target='_blank', className='link_credits'),
            '. Designed by ',
            html.A(href='http://camillemagnan.com/',
                children='Camille Magnan', target='_blank', className='link_credits'),
            '.'
    ]),

        html.P(style={
            'color': '#AEAEAE',
            'paddingBottom': '1cm',
            'paddingLeft': '1cm',
            'fontWeight': '500',
            'fontSize': '10pt'
        }, 
        children = [
        'This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.'
    ]),

    ]),
])
