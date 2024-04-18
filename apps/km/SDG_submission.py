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
                dbc.Label(
                    [
                        "Ranking Body ",
                         html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="Enter Ranking Body", value="THE World Rankings"),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Evidence Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="Enter Evidence Name", value="Building XX"),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Description ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Textarea(placeholder="Enter Description"),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Office ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "UP Diliman", "value": "UP Diliman"},
                            # Add more options here
                        ],
                        value="UP Diliman",  # Pre-selected as per image
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Accomplished By ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="Name Surname", value="Name Surname"),  # Pre-filled as per image
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Date Submitted ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="Date Submitted", value="Monday, 29 January 2024, 11:00 PM"),  # Pre-filled as per image
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "File Submissions ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Upload(
                        dbc.Button('Upload File', color="primary"),
                        # To allow multiple files to be uploaded
                        multiple=True
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="url", placeholder="Enter Link"),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Add Applicable Criteria ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Checklist(
                        options=[
                            {"label": "Criteria 1", "value": 1},
                            {"label": "Criteria 2", "value": 2},
                            {"label": "Criteria 3", "value": 3},
                            # Add options for Criteria 4-6 as needed
                        ],
                        value=[1, 2],  # Pre-selected as per image
                        inline=True,
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
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
                        html.H1("ADD NEW SUBMISSION"),
                        html.Hr(),
                        dbc.Row(
                            [
                                form  
                            ] 
                        ), 
                       
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Submit for checking", color="primary", className="me-3"), 
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Submit & Add New", color="warning", className="me-3"),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="danger"),
                                    width="auto"
                                ),
                            ],
                            className="mb-3",
                            justify="end",
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


