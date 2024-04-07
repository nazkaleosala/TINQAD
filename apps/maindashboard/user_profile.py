import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


profile_image_path = '/database/takagaki1.png'

# Your profile header component with circular image
profile_header = html.Div(
    [
        html.Div(
            html.Img(
                src=profile_image_path, 
                style={
                    'height': '100px', 
                    'width': '100px', 
                    'borderRadius': '50%',
                    'objectFit': 'cover',
                    'display': 'inline-block', 
                    'verticalAlign': 'middle'
                }
            ),
            style={'textAlign': 'center', 'display': 'inline-block'}
        ),
        html.Div(
            [
                html.H2("PROFILE", style={'display': 'inline-block', 'margin': '0 10px'}),
                html.H3("Pikachu, Pika", style={'marginBottom': 0}),
                html.P("2020-*****")
            ],
            style={'display': 'inline-block', 'verticalAlign': 'middle'}
        ),
    ],
    style={'textAlign': 'center', 'marginTop': '20px'}
)


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_navbar(), 
                    width=2 
                ),
                dbc.Col(
                [
                    html.H1("PROFILE"),
                    html.Hr(),
                    profile_header,  # Insert the profile header here
                ], width=8, style={'marginLeft': '15px'}
                ),
                 
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)