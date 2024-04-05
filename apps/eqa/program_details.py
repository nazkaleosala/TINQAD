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


form = dbc.Form(
    [
        html.H5("DEGREE PROGRAM INFORMATION", className="form-header fw-bold"),
        dbc.Row(
            [
                dbc.Label("Degree Program Title", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("College", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Institute/ Department", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Academic Cluster", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Science and Technology", "value": "Science and Technology"},
                            {"label": "Social Sciences and Law", "value": "Social Sciences and Law"},
                            {"label": "Management and Economics", "value": "Management and Economics"},
                            {"label": "Arts and Letters", "value": "Arts and Letters"},
                        ],
                    ),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Degree Count", width=4),
                dbc.Col(
                    dbc.Input(type="number"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Degree Program Type", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Certificate", "value": "Certificate"},
                            {"label": "Diploma", "value": "Diploma"},
                            {"label": "Associate", "value": "Associate"},
                            {"label": "Undergraduate", "value": "Undergraduate"},
                            {"label": "Master's", "value": "Master's"},
                            {"label": "Doctorate", "value": "Doctorate"},
                        ],
                    ),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Academic Calendar Type", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Semester", "value": "Semester"},
                            {"label": "Trimester", "value": "Trimester"},
                        ],
                    ),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Applicable accreditation body", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
    ]
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
                        html.H1("ADD NEW PROFILE"),
                        html.Hr(),
                        dbc.Row(
                            [
                                form, 
                                  
                            ] 
                        ), 
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Register", color="primary", className="me-3"), 
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="secondary"),
                                    width="auto"
                                ),
                            ],
                            className="mb-3",
                        ),
                        
                    ], width=8, style={'marginLeft': '15px'}
                ),   
            ]
        ),
        

        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)


