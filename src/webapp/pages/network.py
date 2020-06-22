import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import pandas as pd
import networkx as nx
import json

def readGraph():
    with open ('../networkData/prova2.cyjs') as prova:
        json_prova = json.load(prova)
        return json_prova['elements']['nodes'] + json_prova['elements']['edges']

graphData = readGraph()


network_layout = [html.Div(children=[
    html.Button(id='btn-net', n_clicks=0, children=['crea']),
    html.Div(id='network-output')
    # cyto.Cytoscape(
    #     id='cytoscape',
    #     layout={'name': 'preset'},
    #     style={'width': '100%', 'height': '400px'},
    #     elements=graphData
    # )
])]

# B06XYPK9M6