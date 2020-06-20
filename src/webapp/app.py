# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=['./app-styles.css'])

app.layout = html.Div(children=[
    #html.H1(children='Hello Dash'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Img(src='/assets/logo-zann.png', className='logo'),
            ], className="logo-container"),
            html.Button('Exploration', id='btnExpl', className='btn-zan-big'),
            html.Button('Network', id='btnNet', className='btn-zan-big'),
            html.Button('Sentiment', id='btnSent', className='btn-zan-big'),
        ]     
        , className='sidebar-content'),
    ], className='sidebar zan-box-shadow'),
    html.Div(children='''
        content
    ''', className='content'),

    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # )
], className='main')

if __name__ == '__main__':
    app.run_server(debug=True)