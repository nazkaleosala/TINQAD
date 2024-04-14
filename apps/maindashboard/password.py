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
from calendar import month_name



profile_image_path = '/assets/database/takagaki1.png'


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
                    'verticalAlign': 'center'
                }
            ),
            style={'textAlign': 'left', 'display': 'inline-block'}
        ),
        html.Div(
            [
                 
                html.H3("Pikachu, Pika", style={'marginBottom': 0, 'marginLeft': '25px'}),
                html.P("2020-*****", style={'marginBottom': 0, 'marginLeft': '25px'})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)




 


form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Previous Password", width=4),
                dbc.Col(dbc.Input(type="text"  ), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("New Password", width=4),
                dbc.Col(dbc.Input(type="text"), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Confirm Password", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
            ],
            className="mb-2",
        ), 
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Save", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
            ],
            className="mb-2",
        ),
         
    ],
    className="g-2",
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
                    html.Br(), 
                    form,  # Insert the profile table here
                    

                ], 
                
                    width=6, 
                    style={'marginLeft': '15px'}
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