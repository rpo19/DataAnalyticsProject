import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json

def readGraph():
    with open ('../networkData/giantComponent.cyjs', encoding='cp850') as prova:
        json_prova = json.load(prova)
        return json_prova['elements']['nodes'] + json_prova['elements']['edges']

graphData = readGraph()


network_layout = [
    html.Div(children=[
        html.Label('Color', className='mb-5'),
        dcc.RadioItems(
            options=[
                {'label': 'Communities', 'value': 'rgbComm'},
                {'label': 'Categories', 'value': 'rgbCat'},
            ],
            value='rgbCat'
        ),
        html.Div(className='mb-10'),  
        html.Label('Subgraph by category', className='mb-5'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Category1', 'value': '1'},
                {'label': 'Category2', 'value': '2'},
                {'label': 'Category3', 'value': '3'}
            ]
        ),
        html.Div(className='mb-10'),  
        html.Label('Subgraph by community', className='mb-5'),
        dcc.Dropdown(
            id='dropdown2',
            options=[
                {'label': 'Community1', 'value': 'comm1'},
                {'label': 'Community2', 'value': 'comm2'},
                {'label': 'Community3', 'value': 'comm3'}
            ]
        ),
        html.Button(id='btn-reset', n_clicks=0, children=[
            'Reset Graph'
        ], className='btn-small zan-box-shadow', style={'marginTop': 'auto'}),
    ], className="network-menu-container zan-box-shadow flex-column"),
    html.Div(children=[
        html.Div('Giant component', className='subtitle mb-10'),
        html.Div('N. of categories: numero'),
        html.Div('N. of communities: numero'),
    ], className="network-stats-container zan-box-shadow flex-column"),
    html.Div(id='network-output', className="network-container flex-grow")
]
