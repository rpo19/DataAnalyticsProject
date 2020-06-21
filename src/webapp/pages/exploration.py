import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import statistics
import plotly.graph_objects as go

def getNumberOfCategories():
    return len(df['category'].value_counts())

def getAvgRating():
    return round(statistics.mean(df['avg_rating']), 2)

def getAvgPrice():
    return round(statistics.mean(df['price']), 2)

def getNumberOfLinks():
    return len(df_edges)

df = (pd.read_csv('../networkData/cytoProducts.csv', sep='\t'))
df_edges = (pd.read_csv('../networkData/cytoEdges.csv', sep='\t'))

categories = df['category'].value_counts()
pieCategories = go.Figure(data=[go.Pie(labels=categories.keys(), values=categories.values, hole=.3)])

products_layout = [
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.head(10).columns],
        data=df.head(10).to_dict('records'),
    ),
    html.Div(children=[
        html.Button(children=[
            html.H2('N. of products', className='card-rect-title'),
            html.H1(len(df))
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto'}),
        html.Button(id='btn-cat', n_clicks=0, children=[
            html.H2('N. of Categories', className='card-rect-title'),
            html.H1(getNumberOfCategories())
        ], className='card-rect zan-box-shadow'),
        html.Button(children=[
            html.H2('Avg Rating', className='card-rect-title'),
            html.H1(getAvgRating())
        ], className='card-rect zan-box-shadow'),
        html.Button(children=[
            html.H2('Avg Price', className='card-rect-title'),
            html.H1(getAvgPrice())
        ], className='card-rect zan-box-shadow'),
        html.Button(children=[
            html.H2('N. of Links', className='card-rect-title'),
            html.H1(getNumberOfLinks())
        ], className='card-rect zan-box-shadow', style={'marginRight': 'auto'}),
    ], className='flex-row flex-grow flex-wrap', style={'marginBottom': '24px'}),
    # dcc.Graph(
    #     id='example-graph-2',
    #     figure=pieCategories
    # ),
    html.Div(id='hidden-div')
]

exploration_layout = [html.Div(children=[
    html.Div(children='Dataset Exploration', className='title', style={'marginBottom': '24px'}),
    dcc.Tabs(id='tabs', value='products', children=[
        dcc.Tab(label='Products', value='products'),
        dcc.Tab(label='Reviews', value='reviews'),
    ]),
    html.Div(id='tab-content', style={'paddingTop': '20px'})
], className='flex-column')]

