# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from pages.exploration import exploration_layout, products_layout, sample_products_list, reviews_layout, histCategories, histRating, histPrice
from pages.network import network_layout, readGraph
from pages.sentiment import sentiment_layout
from pages.about import about_layout
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import json

app = dash.Dash(
    __name__,
    external_stylesheets=[
        './app-styles.css',
        'https://fonts.googleapis.com/icon?family=Material+Icons+Outlined|Material+Icons+Round',
        'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'
    ],
    suppress_callback_exceptions=True
)

default_stylesheet = [
    {
        'selector': 'node:selected',
        'style': {
            'background-color': 'red',
            'width': '100px',
            'height': '100px'
        }
    },
]


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Img(src='/assets/logo.png', className='logo'),
            ], className="logo-container"),
            dcc.Link(children=[
                'Exploration',
                html.I(children='call_made', className='material-icons-round icon-button')],
                href='/exploration',className='btn-zan-big'),
            dcc.Link(children=[
                'Network',
                html.I(children='call_made', className='material-icons-round icon-button')],
                href='/network',className='btn-zan-big'),
            dcc.Link(children=[
                'Sentiment',
                html.I(children='call_made', className='material-icons-round icon-button')],
                href='/sentiment',className='btn-zan-big'),
            dcc.Link(children=[
                'About',
                html.I(children='call_made', className='material-icons-round icon-button')],
                href='/',className='btn-zan-big', style={'marginTop':'auto', 'marginBottom': '40px'}),
        ]     
        , className='sidebar-content'),
    ], className='sidebar zan-box-shadow'),
    html.Div(id='page-content', className='content')
], className='main')

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/exploration':
        return exploration_layout
    elif pathname == '/network':
        return network_layout
    elif pathname == '/sentiment':
        return sentiment_layout
    else:
        return about_layout

@app.callback(Output('tab-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'products':
        return products_layout
    elif tab == 'reviews':
        return reviews_layout

@app.callback(
    [dash.dependencies.Output('hidden-div-1', 'children'),
    dash.dependencies.Output('title-section', 'children')],
    [dash.dependencies.Input('btn-cat', 'n_clicks'),
    dash.dependencies.Input('btn-rat', 'n_clicks'),
    dash.dependencies.Input('btn-price', 'n_clicks'),
    dash.dependencies.Input('btn-prod', 'n_clicks') ])
def update_output(btnCat, btnRat, btnPrice, btnProd):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-cat' in changed_id:
        return dcc.Graph(
                    id='example-graph-2',
                    figure=histCategories
                ), 'Categories Distribution'
    elif 'btn-rat' in changed_id:
        return dcc.Graph(
                    id='example-graph-3',
                    figure=histRating
                ), 'Rating Distribution'
    elif 'btn-price' in changed_id:
        return dcc.Graph(
                    id='example-graph-4',
                    figure=histPrice
                ), 'Price Distribution'
    elif 'btn-prod' in changed_id:
        return sample_products_list, 'Products Samples'
    else:
        return sample_products_list, 'Products Samples'

@app.callback(Output('confirm', 'displayed'),
              [Input('btn-giant', 'n_clicks')])
def display_confirm(btnGiant):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-giant' in changed_id:
        return True
    return False

@app.callback(
    dash.dependencies.Output('network-output', 'children'),
    [Input('confirm', 'submit_n_clicks'),
    dash.dependencies.Input('dropComm', 'value')])
def update_output(submit_n_clicks, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'dropComm' in changed_id:
        if value is not None:
            graphData = readGraph(value)
            return  cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'preset'},
                    stylesheet=default_stylesheet,
                    autolock=True,
                    style={'width': '100%', 'height': '100%'},
                    elements=graphData)
        else:
            return html.Div(children=[
                html.Div('Choose a network to display', className='mb-10'),
                html.I(children='get_app', className='material-icons-round', style={'fontSize': '60px'}),
            ], className='flex-column flex-center justify-center subtitle network-title-placeholder')
    else:
        if submit_n_clicks:
            graphData = readGraph('giantComponent.cyjs')
            return  cyto.Cytoscape(
                id='cytoscape',
                layout={'name': 'preset'},
                stylesheet=default_stylesheet,
                autolock=True,
                style={'width': '100%', 'height': '100%'},
                elements=graphData)
        else:
            return html.Div(children=[
                html.Div('Choose a network to display', className='mb-10'),
                html.I(children='get_app', className='material-icons-round', style={'fontSize': '60px'}),
            ], className='flex-column flex-center justify-center subtitle network-title-placeholder')

@app.callback(dash.dependencies.Output('cytoscape', 'stylesheet'),
    [dash.dependencies.Input('radioColor', 'value'),
    dash.dependencies.Input('dropSize', 'value')])
def update_stylesheet(value, size):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    nodeSize = ''
    if size == 'default':
        nodeSize = ''
    else:
        nodeSize = 'data(nodeSize)'
    if value is None:
        value = ''
    
    additional_styles = [
            {
                'selector': 'node',
                'style': {
                    'background-color': value,
                    'width': nodeSize,
                    'height': nodeSize
                }
            }
    ]    
    return default_stylesheet + additional_styles


@app.callback(Output('node-output', 'children'),
              [Input('cytoscape', 'tapNodeData')])
def displayTapNodeData(data):
    if data is not None:
        return html.Div(children=[
                html.Div(children=[
                    html.Div(data['title'], className='subtitle'),
                    html.Div('Category: ' + data['category']),
                    html.Div('Degree: ' + str(data['Degree'])),
                    html.Div('Community: ' + str(data['community'])),
                    
                ], className=' flex-column')
            ], className='node-info-content flex-column zan-box-shadow'),

if __name__ == '__main__':
    app.run_server(debug=True)