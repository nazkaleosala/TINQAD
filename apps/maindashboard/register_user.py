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
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Surname", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("ID Number", width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="0000-00000"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Access Type", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Basic Access", "value": "Basic"},
                            {"label": "Full Access", "value": "Full"},
                            # Include other options here
                        ],
                        placeholder="Select access type",
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Office", width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder= "Quality Assurance Office"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Position", width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder= "Administration Team / Outside of QAO"),
                    width=6,
                ),
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
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Password", width=4),
                dbc.Col(
                    dbc.Input(type="password", placeholder="Enter new password"),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Register", color="primary", className="me-3"), 
                    # Removed the offset and changed the size to 'auto' to take up only as much space as needed
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary"),
                    # Set the width to 'auto' to align the button to the left alongside the "Register" button
                    width="auto"
                ),
            ],
            className="mb-3",
        )
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
                    html.H1("CREATE NEW USER"),
                    html.Hr(),
                    form,
                ],
                width=8, style={'marginLeft': '15px'}
                
                )
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