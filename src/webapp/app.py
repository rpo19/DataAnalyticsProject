# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from pages.exploration import exploration_layout, products_layout, sample_products_list, reviews_layout, histCategories, histRating, histPrice
from pages.network import network_layout, graphData
from pages.sentiment import sentiment_layout
from pages.about import about_layout
from dash.dependencies import Input, Output
import dash_cytoscape as cyto

app = dash.Dash(
    __name__,
    external_stylesheets=[
        './app-styles.css',
        'https://fonts.googleapis.com/icon?family=Material+Icons+Outlined|Material+Icons+Round',
        'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'
    ],
    suppress_callback_exceptions=True
)

stylesheet=[
        # Class selectors
        {
            'selector': '.red',
            'style': {
                'background-color': 'red',
                'line-color': 'red',
                'width': '300px',
                'height': '300px'
            }
        }
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

@app.callback(
    dash.dependencies.Output('network-output', 'children'),
    [dash.dependencies.Input('btn-reset', 'n_clicks') ])
def update_output(btnReset):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-reset' in changed_id:
        for row in graphData:
            if row['data']['shared_name'] == 'B07NVMYB7K':
                row['classes'] = 'red'
        return  cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'preset'},
            stylesheet=stylesheet,
            style={'width': '100%', 'height': '100%'},
            elements=graphData
        )
    else:
        for row in graphData:
            if row['data']['shared_name'] == 'B07NVMYB7K':
                row['classes'] = 'red'
        return  cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'preset'},
            stylesheet=stylesheet,
            style={'width': '100%', 'height': '100%'},
            elements=graphData
        )

if __name__ == '__main__':
    app.run_server(debug=True)