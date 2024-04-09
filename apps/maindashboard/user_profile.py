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
                dbc.Label("First Name", width=4),
                dbc.Col(dbc.Input(type="text", value="Pika"), width=8),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Surname", width=4),
                dbc.Col(dbc.Input(type="text", value="Pikachu"), width=8),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("ID Number", width=4),
                dbc.Col(dbc.Input(type="text", value="2020-*****"), width=8),
            ],
            className="mb-3",
        ),
        # ... Other dbc.Row components for different fields
        dbc.Row(
            [
                dbc.Label("Department", width=4),
                dbc.Col(dbc.Input(type="text", value="Quality Assurance Office"), width=8),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Position", width=4),
                dbc.Col(dbc.Input(type="text", value="Internal Quality Assurance Team"), width=8),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Sex Assigned at Birth", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Female", "value": "F"},
                            {"label": "Male", "value": "M"},
                            # Include other options here
                        ],
                        value="F",  # Preselect "Female"
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Civil Status", width=4),
                dbc.Col(dbc.Input(type="text", value="Single"), width=8),
            ],
            className="mb-3",
        ),
        # ... Continue adding rows for each field
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
                    form,  # Insert the profile table here

                ], 
                    width=8, 
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