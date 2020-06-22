import dash
import dash_core_components as dcc
import dash_html_components as html

about_layout = [html.Div(children=[
    html.Img(src='/assets/logo.png', className='logo-big', style={'marginTop': 'auto', 'marginBottom': 'auto'}),
    html.Div(children='Network and Sentiment Anlysis on Amazon Dataset', className="text-center title", style={'marginTop': '24px'}),
    html.Div(children='Data Analytics Project', className="text-center subtitle", style={'marginTop': '24px', 'marginBottom': 'auto'}),

    html.Div(children=[
        dcc.Link(children=[
                html.Div(children=[
                        html.Div(className='img-dataset'),
                        html.Div(children='Dataset Exploration'),
                    ], className="zan-box-shadow card-small")],
                href='/exploration', className="text-decor-none", style={'marginLeft': 'auto'}),
        dcc.Link(children=[
                html.Div(children=[
                        html.Div(className='img-network'),
                        html.Div(children='Network Analysis'),
                    ], className="zan-box-shadow card-small")],
                href='/network', className="text-decor-none"),
        dcc.Link(children=[
                html.Div(children=[
                        html.Div(className='img-sentiment'),
                        html.Div(children='Sentiment Anlysis'),
                    ], className="zan-box-shadow card-small")],
                href='/sentiment', className="text-decor-none", style={'marginRight': 'auto'}),
    ], className="flex-row", id='about', style={'marginTop': '24px', 'marginBottom': '24px'}),

    html.Div(children='Authors: Christian Bernasconi - Gabriele Ferrario - Riccardo Pozzi - Marco Ripamonti', className="text-center caption", style={'marginTop': 'auto', 'marginBottom': '10px'}),
    html.Div(children='Date: 06/07/2020', className="text-center caption", style={'marginBottom': '10px'}),
], className='flex-column-center p-20')]