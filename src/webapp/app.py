# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from pages.exploration import exploration_layout, products_layout, sample_products_list, reviews_layout, histCategories, histRating, histPrice, dfSampleProducts
from pages.network import network_layout, readGraph, communities_stats
from pages.sentiment import sentiment_layout, clean_sentence, bow, model, dfTimeSeries
from pages.about import about_layout
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import json
import ast
import plotly.express as px

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
            'border-width': '5',
            'border-color': 'yellow'
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

@app.callback(Output('confirm', 'displayed'),
              [Input('btn-giant', 'n_clicks')])
def display_confirm(btnGiant):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-giant' in changed_id:
        return True
    return False

@app.callback(
    [dash.dependencies.Output('network-output', 'children'),
    dash.dependencies.Output('stats-output', 'children'),
    dash.dependencies.Output('wordcloud-output', 'children'),
    dash.dependencies.Output('show-central', 'style')],
    [Input('confirm', 'submit_n_clicks'),
    dash.dependencies.Input('dropComm', 'value')])
def update_output(submit_n_clicks, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'dropComm' in changed_id:
        if value is not None:
            graphData = readGraph('community' + value + '.cyjs')
            communityStats = communities_stats.loc[communities_stats['id'] == int(value)]
            topWords = list(communities_stats["top_words"][int(value)-1].keys())[0:3]
            topEnts = list(communities_stats["top_ents"][int(value)-1].keys())[0:3]
            b64_image = communityStats["wordclouds"].values[0]
            return  [cyto.Cytoscape(
                    id='cytoscape',
                    layout={'name': 'preset'},
                    stylesheet=default_stylesheet,
                    autolock=True,
                    style={'width': '100%', 'height': '100%'},
                    elements=graphData), 
                    html.Div(children=[
                        html.Div('Nodes: ' + str(communityStats['cardinality'].values[0])),
                        html.Div('Max Degree: ' + str(communityStats['max_degree'].values[0])),
                        html.Div('Avg Clust. Coeff: ' + str(round(communityStats['avg_clust'].values[0], 2)), className='mb-10'),
                        html.Div('Dominant Category: ' + communityStats['dominant_category'].values[0], className='mb-10'),
                        html.Div('Top Words: ' + str(topWords), className='mb-10'),
                        html.Div('Top Entities: ' + str(topEnts))
                    ]),
                    html.Div(children=[
                        html.I('cloud_queue', className='material-icons-round', style={'marginLeft': 'auto'}),
                        html.Div(children=[
                            html.Img(src='data:image/png;base64,{0}'.format(b64_image))
                        ], className='wordcloud-container zan-box-shadow'),
                    ], className='disp-flex flex-center justify-center icon-wordcloud-wrapper'),
                    {'visibility': 'visible'}
                    ]
        else:
            return [html.Div(children=[
                html.Div('Choose a network to display', className='mb-10'),
                html.I(children='get_app', className='material-icons-round', style={'fontSize': '60px'}),
            ], className='flex-column flex-center justify-center subtitle network-title-placeholder'), 
            html.Div(children=[
                html.Div('Nodes: 17914'),
                html.Div('Edges: 26572', className='mb-10'),
                html.Div('N. of categories: 37'),
                html.Div('N. of communities: 1064'),
                html.Div('N. of conn. cmps: 962'),
            ], className='flex-column'), '', {'visibility': 'hidden'}]
    else:
        if submit_n_clicks:
            graphData = readGraph('giantComponent.cyjs')
            return  [cyto.Cytoscape(
                id='cytoscape',
                layout={'name': 'preset'},
                stylesheet=default_stylesheet,
                autolock=True,
                style={'width': '100%', 'height': '100%'},
                elements=graphData), 
                html.Div(children=[
                html.Div('Nodes: 17914'),
                html.Div('Edges: 26572', className='mb-10'),
                html.Div('N. of categories: 37'),
                html.Div('N. of communities: 1064'),
                html.Div('N. of conn. cmps: 962'),
            ], className='flex-column'), '', {'visibility': 'hidden'}]
        else:
            return [html.Div(children=[
                html.Div('Choose a network to display', className='mb-10'),
                html.I(children='get_app', className='material-icons-round', style={'fontSize': '60px'}),
            ], className='flex-column flex-center justify-center subtitle network-title-placeholder'),
            html.Div(children=[
                html.Div('Nodes: 17914'),
                html.Div('Edges: 26572', className='mb-10'),
                html.Div('N. of categories: 37'),
                html.Div('N. of communities: 1064'),
                html.Div('N. of conn. cmps: 962'),
            ], className='flex-column'), '', {'visibility': 'hidden'}]
            

@app.callback(dash.dependencies.Output('cytoscape', 'stylesheet'),
    [dash.dependencies.Input('radioColor', 'value'),
    dash.dependencies.Input('dropSize', 'value'),
    dash.dependencies.Input('show-central', 'n_clicks'),
    dash.dependencies.Input('dropComm', 'value'),
    dash.dependencies.Input('confirm', 'submit_n_clicks')])
def update_stylesheet(value, size, n_clicks, dropComm, submit_n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n_clicks is not None:
        if 'show-central' in changed_id and n_clicks > 0:
            central_styles = [
                {
                    'selector': '[centralNode = 1]',
                    'style': {
                        'shape': 'star',
                    }
                },
                {
                    'selector': '[centralNode =0]',
                    'style': {
                        'opacity': '0.5'
                    }
                }
            ]
        else:
            central_styles = []
    nodeSize = ''
    if size == 'default':
        nodeSize = '40'
    elif size == 'degree':
        nodeSize = 'data(nodeSize)'
    else:
        nodeSize = '40'
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
    custom_style = additional_styles + central_styles
    return default_stylesheet + custom_style


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

@app.callback(dash.dependencies.Output('predicted-value-output','children'),
                [Input('predict-review', 'n_clicks')], 
                [dash.dependencies.State('review-input', 'value')], 
                )
def callback(clicks, input_value):
    if clicks is not None and clicks > 0 and input_value is not None:
        text = clean_sentence(input_value)
        predict_value = model.predict(bow.transform([text]))[0].upper()
        if predict_value == 'NEGATIVE':
            return html.Div(children=[
                    html.Div(predict_value, style={'marginRight': '20px'}),
                    html.I('sentiment_dissatisfied', className='material-icons-round', style={'fontSize': '35px', 'color': 'red'})
                ], className='flex-row flex-center predicted-sent')
        else:
            return html.Div(children=[
                    html.Div(predict_value, style={'marginRight': '20px'}),
                    html.I('sentiment_satisfied', className='material-icons-round', style={'fontSize': '35px', 'color': 'green'})
                ], className='flex-row flex-center predicted-sent')


@app.callback(Output('prod-series-output', 'children'),
              [Input('dropTimeSeries', 'value')])
def render_content(idProd):
    if idProd is not None:
        filteredDf = dfTimeSeries.loc[dfTimeSeries['product'] == idProd]
        trendCoeff = filteredDf['trendCoeff'].values[0]
        fig = fig = px.line(filteredDf, x='Period', y=['polarity', 'rating'],)
        trendLabel = 'Trending Down'
        trendIcon = 'trending_down'
        trendColor = '#E44133'
        if trendCoeff > 0:
            trendLabel = 'Trending Up'
            trendIcon = 'trending_up'
            trendColor = '#33A352'
            
        return html.Div(children=[
            dcc.Graph(id='time-series-graph', figure=fig),
            html.Div(children=[
                html.I(trendIcon, className='material-icons-round', style={'fontSize': '50px', 'color': trendColor, 'marginLeft':'auto', 'marginRight':'20px'}),
                html.Div(trendLabel, className='subtitle', style={'marginRight':'auto'})
            ], className='flex-row flex-center')
        ], className='flex-column')

if __name__ == '__main__':
    app.run_server(debug=True)