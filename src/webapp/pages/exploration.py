import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import statistics
import plotly.graph_objects as go
import plotly.express as px
import statistics

def getNumberOfCategories():
    return len(df['category'].value_counts())

def getAvgRating():
    return round(statistics.mean(df.loc[df['avg_rating'] != 0]['avg_rating'].values), 2)

def getAvgPrice():
    return round(statistics.mean(df['price']), 2)

def getNumberOfLinks():
    return len(df_edges)

def generateSampleProducts():
    return html.Div(className='flex-row flex-wrap', style={'justifyContent': 'space-between'} , children=[html.Div(children=[
        html.Img(src=row[1]['pictures'].strip('][').split(', ')[0].strip('\'\''), className='img-product'),
        html.H3(row[1]['title'])
    ], className='card-product zan-box-shadow') for row in dfSampleProducts.iloc[4:8].iterrows()])

def generateSampleReviews():
    return html.Div(className='flex-column', children=[
        html.Div(children=[
            html.Div(children=[
                html.I('account_circle', className='material-icons-round'),
                html.Div(row[1]['author-name']),
                html.Div('Rating:' + str(row[1]['rating']), style={'marginLeft': 'auto'}),
            ], className='flex-row user-review'),
            html.Div(children=[
                html.H3(row[1]['title']),
                html.Div(row[1]['body'])
            ], className='card-review zan-box-shadow')
        ], className='flex-column', style={'width': '80%', 'marginLeft': 'auto', 'marginRight': 'auto'}) for row in dfSampleReviews.iterrows()
    ])


df = (pd.read_csv('../networkData/cytoProducts.csv', sep='\t'))
dfSampleProducts = (pd.read_csv('../dataApp/sampleProducts.csv', sep='\t'))
dfSampleReviews = (pd.read_csv('../dataApp/sampleReviews.csv', sep='\t'))
dfSampleReviewsText = (pd.read_csv('../dataApp/sampleReviewsText.csv', sep='\t'))
reviewsFilteredDistrib = (pd.read_csv('../dataApp/ratingDistribFilteredReviews.csv', sep='\t'))
dfRatings = (pd.read_csv('../dataApp/ratingsDistrib.csv', sep='\t'))
df_edges = (pd.read_csv('../networkData/cytoEdges.csv', sep='\t'))

categories = pd.DataFrame({'category':df['category'].value_counts().keys(), 'value': df['category'].value_counts().values})
histCategories = px.histogram(categories, x='category', y='value', color='category')
histRating = px.histogram(df.loc[df['avg_rating'] != 0], x='avg_rating')
histPrice = px.histogram(df[['price', 'title']], x='price')
histFilteredReviews = px.bar(reviewsFilteredDistrib, x='rating', y='value')


products_layout = [
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.head(10).drop(labels=['community'], axis=1).columns],
        data=df.head(10).to_dict('records'),
    ),
    html.Div(children=[
        html.Button(id='btn-prod', n_clicks=0, children=[
            html.H2('N. of products', className='card-rect-title'),
            html.H1(len(df))
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.Button(id='btn-cat', n_clicks=0, children=[
            html.H2('N. of Categories', className='card-rect-title'),
            html.H1(getNumberOfCategories())
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.Button(id='btn-rat', n_clicks=0, children=[
            html.H2('Avg Rating', className='card-rect-title'),
            html.H1(getAvgRating())
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.Button(id='btn-price', n_clicks=0, children=[
            html.H2('Avg Price', className='card-rect-title'),
            html.H1(getAvgPrice())
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.Button(children=[
            html.H2('N. of Links', className='card-rect-title'),
            html.H1(getNumberOfLinks())
        ], className='card-rect zan-box-shadow', style={'marginRight': 'auto'}),
    ], className='flex-row flex-grow flex-wrap', style={'marginBottom': '24px'}),
    html.Div(id='title-section', className='text-center title', style={'marginBottom': '24px', 'marginTop': '24px'}),
    html.Div(id='hidden-div-1')
]

sample_products_list = [
    generateSampleProducts()
]

reviews_layout = [
    dash_table.DataTable(
        id='table2',
        columns=[{"name": i, "id": i} for i in dfSampleReviews.drop(labels=['body'], axis=1).columns],
        data=dfSampleReviews.to_dict('records'),
    ),
    html.Div(children=['Filtering Reviews Process'], className='title text-center', style={'marginBottom': '24px', 'marginTop': '60px'}),
    html.Div(children=['A filtering process has been made to select a reliable group of reviews to analyze.'], className='subtitle text-center', style={'marginBottom': '24px'}),
    html.Div(children=[
        html.Button(id='btn-reviews', n_clicks=0, children=[
            html.H2('N. of reviews', className='card-rect-title'),
            html.H1(1988854)
        ], className='card-rect zan-box-shadow', style={'marginLeft': 'auto', 'marginTop': '0px', 'marginRight': '0px'}),
        html.I('arrow_right_alt', className='material-icons-round', style={'fontSize':'60px'}),
        html.Button(id='btn-reviews', n_clicks=0, children=[
            html.I('done', className='material-icons-round', style={'fontSize': '40px', 'color': 'green'}),
            html.H1(1879228),
            html.Div('Verified Reviews', className='popup', style={'left': '35px'})
        ], className='card-rect zan-box-shadow', style={'marginTop': '0px'}),
        html.I('arrow_right_alt', className='material-icons-round', style={'fontSize':'60px'}),
        html.Button(children=[
            html.I('thumb_up_alt', className='material-icons-round', style={'fontSize': '40px', 'color': '#E1CEC8'}),
            html.H1(377671),
            html.Div('Verified Reviews with at least 1 helpful', className='popup', style={'left': '10px'})
        ], className='card-rect zan-box-shadow', style={'marginRight': 'auto', 'marginTop': '0px'}),
    ], className='flex-row flex-grow flex-center', style={'marginBottom': '100px', 'marginTop': '48px'}),
    dcc.Graph(
                    id='reviewDistrib',
                    figure=histFilteredReviews
                ),
    html.Div(children=['Sample Reviews'], className='title text-center', style={'marginBottom': '24px', 'marginTop': '60px'}),
    generateSampleReviews()
]

sample_reviews_list = [
    generateSampleReviews()
]

exploration_layout = [html.Div(children=[
    html.Div(children='Dataset Exploration', className='title', style={'marginBottom': '24px'}),
    dcc.Tabs(id='tabs', value='products', children=[
        dcc.Tab(label='Products', value='products'),
        dcc.Tab(label='Reviews', value='reviews'),
    ]),
    html.Div(id='tab-content', style={'paddingTop': '20px'})
], className='flex-column p-20')]

