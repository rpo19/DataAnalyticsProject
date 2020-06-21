# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from pages.exploration import exploration_layout, products_layout, pieCategories
from pages.network import network_layout
from pages.sentiment import sentiment_layout
from pages.about import about_layout
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    external_stylesheets=[
        './app-styles.css',
        'https://fonts.googleapis.com/icon?family=Material+Icons+Outlined|Material+Icons+Round',
        'https://fonts.googleapis.com/css2?family=Open+Sans&display=swap'
    ],
    suppress_callback_exceptions=True
)

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
        return html.Div([
            html.H3('Tab content 2')
        ])

@app.callback(
    dash.dependencies.Output('hidden-div', 'children'),
    [dash.dependencies.Input('btn-cat', 'n_clicks')])
def update_output(btnCat):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-cat' in changed_id:
        return dcc.Graph(
                    id='example-graph-2',
                    figure=pieCategories
                )
    else:
        print('none')

if __name__ == '__main__':
    app.run_server(debug=True)