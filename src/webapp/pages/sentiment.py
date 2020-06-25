import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pickle
import nltk
import string
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import plotly.express as px

dfNeutral = pd.read_csv('../dataApp/neutralReviews.csv')
dfSentProducts = pd.read_csv('../dataApp/sentimentProducts.csv', sep='\t')
dfTimeSeries= pd.read_csv('../dataApp/dataReviewsMonthly.csv')
fig = px.pie(dfNeutral, values='count', names='polarity', color_discrete_sequence=['#E44133', '#33A352'])

def readBow():
    with open('./model/bow.bin', 'rb') as f:
        return pickle.load(f)
def readModel():
    with open('./model/model.bin', 'rb') as f:
        return pickle.load(f)

def stemming_token(sentence,stemmer):
    stem = []
    for elem in sentence:
        stem.append(stemmer.stem(elem))
    return stem

def clean_sentence(sentence):
    tokens = word_tokenize(sentence)
    tokens_clean = []
    for word in tokens:
        if word.lower() not in stop_words and word.lower() not in punctuation and not word.isnumeric() and len(word)> 1:
            tokens_clean.append(stemmer.stem(word))
    return ' '.join(tokens_clean)

stop_words=nltk.corpus.stopwords.words('italian')
punctuation = string.punctuation
punctuation = punctuation + "..."+ "''" + "``" + "--"+ ".."
stemmer = SnowballStemmer("italian")
bow = readBow()
model = readModel()

sentiment_layout = [
    html.Div(children=[
        html.Div(children='Sentiment Anlysis', className='title text-center', style={'marginBottom': '80px'}),
        html.Div(children=[
            html.Img(id='happy', src='/assets/happy.png', className='emoji-icon', style={'marginLeft': 'auto'}),
            html.Img(id='sad', src='/assets/sad.png', className='emoji-icon', style={'marginLeft': '60px', 'marginRight': '60px'}),
            html.Img(id='angry', src='/assets/angry.png', className='emoji-icon', style={'marginRight': 'auto'}),
        ], className='flex-row', style={'marginBottom': '24px'}),
        # dcc.Tabs(id='tabs-sentiment', value='supervised', children=[
        #     dcc.Tab(label='Supervised Sentiment', value='supervised'),
        #     dcc.Tab(label='Tab two', value='tab-2'),
        # ]),
        html.Div(children=[
        html.Div('Write a review to predict its polarity', className='subtitle', style={'marginTop':'60px', 'marginBottom':'60px'}),
        dcc.Input(
            id='review-input',
            type='text',
            placeholder='Write here your review...',
            autoComplete='off',
            spellCheck='false'
        ),
        html.Button(id='predict-review', n_clicks=0, children=[
            'Predict Sentiment'
        ], className='predict-button zan-box-shadow', style={'marginBottom': '80px'}),
        html.Div(id='predicted-value-output', className='subtitle'),
        html.Div(children=[
            html.Div('Prediction on reviews rated', className='subtitle', style={'marginRight':'10px'}),
            html.I('grade', className='material-icons-round', style={'fontSize': '30px','color': '#FFDA6C'}),
            html.I('grade', className='material-icons-round', style={'fontSize': '30px','color': '#FFDA6C'}),
            html.I('grade', className='material-icons-round', style={'fontSize': '30px','color': '#FFDA6C'})
        ], className='flex-row flex-center', style={'marginTop':'120px', 'marginBottom':'20px'}),
        html.Div(children=[
            'After training the model on positive and negative reviews we wanted',
            html.Br(),
            'to see if reviews rated three stars were mostly positive, mostly negative or, in fact, neutral.',
        ], className='text-center', style={'marginBottom': '80px'}),
        dcc.Graph(figure=fig),
        html.Div(children=[
            'Time Series',
        ], className='subtitle', style={'marginTop': '80px', 'marginBottom':'20px'}),
        html.Div(children=[
            'Select a product to analyze its reviews trend and determine if it is positive or negative.',
        ], className='text-center', style={'marginBottom':'20px'}),
        dcc.Dropdown(
            id='dropTimeSeries',
            options=[
                {'label': dfSentProducts.iloc[0]['title'][0:50], 'value': dfSentProducts.iloc[0]['_id']},
                {'label': dfSentProducts.iloc[1]['title'][0:50], 'value': dfSentProducts.iloc[1]['_id']},
                {'label': dfSentProducts.iloc[2]['title'][0:50], 'value': dfSentProducts.iloc[2]['_id']},
                {'label': dfSentProducts.iloc[3]['title'][0:50], 'value': dfSentProducts.iloc[3]['_id']},
            ]
        ),
        html.Div(id='prod-series-output', style={'width': '90%'}),
    ], className='flex-column flex-center'),
    html.Div(id='tabs-sentiment-output')
    ], className='p-20', style={'paddingBottom':'100px'})
]