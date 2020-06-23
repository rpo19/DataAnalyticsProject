import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json

def readGraph(network):
    with open ('../networkData/' + network, encoding='cp850') as prova:
        return json.load(prova)
        #return json_prova['elements']['nodes'] + json_prova['elements']['edges']


network_layout = [
    dcc.ConfirmDialog(
        id='confirm',
        message='This operation requires a lot of resources, are you sure to proceed?',
    ),
    html.Div(children=[
        html.Label('Subgraph by community', className='mb-5'),
        dcc.Dropdown(
            id='dropComm',
            options=[
                {'label': 'Community 1', 'value': 'community1.cyjs'},
                {'label': 'Community 2', 'value': 'community2.cyjs'},
                {'label': 'Community 3', 'value': 'community3.cyjs'},
                {'label': 'Community 4', 'value': 'community4.cyjs'},
                {'label': 'Community 5', 'value': 'community5.cyjs'},
                {'label': 'Community 6', 'value': 'community6.cyjs'},
                {'label': 'Community 7', 'value': 'community7.cyjs'},
                {'label': 'Community 8', 'value': 'community8.cyjs'},
                {'label': 'Community 9', 'value': 'community9.cyjs'},
                {'label': 'Community 10', 'value': 'community10.cyjs'}
            ]
        ),
        html.Div(className='mb-10'),
        html.Label('Node size', className='mb-5'),
        dcc.Dropdown(
            id='dropSize',
            options=[
                {'label': 'Default', 'value': 'default'},
                {'label': 'By degree centrality', 'value': 'degree'},
            ],
            value='default'
        ),
        html.Div(className='mb-10'),
        html.Label('Color', className='mb-5'),
        dcc.RadioItems(
            id='radioColor',
            options=[
                {'label': 'Communities', 'value': 'data(commColor)'},
                {'label': 'Categories', 'value': 'data(catColor)'},
            ],
            value='data(catColor)'
        ),
        html.Div(className='mb-10'),
        html.Button(id='btn-giant', n_clicks=0, children=[
            'Show Giant Component'
        ], className='btn-small zan-box-shadow', style={'marginTop': 'auto'}),
        
    ], className="network-menu-container zan-box-shadow flex-column"),
    html.Div(children=[
        html.Div('Graph stats', className='subtitle mb-10'),
        html.Div('Nodes: 17914'),
        html.Div('Edges: 26572', className='mb-10'),
        html.Div('N. of categories: 37'),
        html.Div('N. of communities: 1064'),
        html.Div('N. of conn. cmps: 962'),
    ], className="network-stats-container zan-box-shadow flex-column"),
    html.Div(id='network-output', className="network-container flex-column flex-grow flex-center justify-center"),
    html.Div(id='node-output', className='node-info-container'),
    html.Div(id='placeholder-output', style={'display': 'none'})
]
