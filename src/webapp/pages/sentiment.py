import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

communities_stats = pd.read_csv("../dataApp/communities_stats.csv", sep='\t')

b64_image = communities_stats.iloc[0]["wordclouds"]

sentiment_layout = [html.Div(children=[
    html.H1(children='Sentiment'),
    html.Img(src='data:image/png;base64,{0}'.format(b64_image))
])]