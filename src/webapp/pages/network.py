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

communities_stats = pd.read_pickle("../dataApp/communities_stats.pickle")


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
                {'label': 'Community 1', 'value': '1'},
                {'label': 'Community 2', 'value': '2'},
                {'label': 'Community 3', 'value': '3'},
                {'label': 'Community 4', 'value': '4'},
                {'label': 'Community 5', 'value': '5'},
                {'label': 'Community 6', 'value': '6'},
                {'label': 'Community 7', 'value': '7'},
                {'label': 'Community 8', 'value': '8'},
                {'label': 'Community 9', 'value': '9'},
                {'label': 'Community 10', 'value': '10'}
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
        html.Button(id='show-central', n_clicks=0, children=[
                        html.I('my_location', className='material-icons-round'),
                        html.Div('Show central node', className='popup-center zan-box-shadow')
                    ], className='central-node-button zan-box-shadow disp-flex flex-center justify-center'),
        html.Div(children=[
            html.Div(children=[
                html.Div('Graph stats', className='subtitle'),
                html.Div(id='wordcloud-output', className='disp-flex flex-center', style={'position': 'relative', 'marginLeft': 'auto'})
            ], className='flex-row subtitle mb-10'),
            html.Div(id='stats-output', className='flex-column')
        ], className="net-stats-content zan-box-shadow flex-column"),
    ], className='network-stats-container flex-column'),

    html.Div(children=[
        html.Div(children=[
            html.I('help_outline', className='material-icons-round', style={'zIndex': '20'}),
            html.Div(children=[
                'The network links represent the relationships between two products often bought in combination (not necessarly at the same time)'
            ], className='info-text zan-box-shadow')
        ],className='info-wrapper flex-column flex-center justify-center')
    ], className="info-container zan-box-shadow", style={'fontSize': '30px', 'color': '#DBDBDB'}),
    html.Div(id='network-output', className="network-container flex-column flex-grow flex-center justify-center"),
    html.Div(id='node-output', className='node-info-container'),
    html.Div(id='placeholder-output', style={'display': 'none'})
]
