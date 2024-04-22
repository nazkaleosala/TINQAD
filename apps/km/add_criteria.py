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


 



  



form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "SDG # ",
                        html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=4
                    ),
                dbc.Col(
                    dbc.Select(
                        id="sdgcriteria_number",  # Adding an id to the Select
                            options=[
                                {"label": "Goal 1: No Poverty", "value": "1"},
                                ],
                            placeholder="Select SDG Goal",  # Optional placeholder text
                            
                        ),width=8,
                    ),
                ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Criteria Code ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                width=4
            ),
                dbc.Col(
                    dbc.Input(
                        id="sdgcriteria_code",  # Adding an id to the Textarea
                        placeholder="Enter SDG #",
                        type="text",
                    ),
                    width=8,
                ),
            ],
        className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                                    [
                                        "Description ",
                                        html.Span("*", style={"color": "#F8B237"})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Textarea(
                                        id="sdgcriteria_description", 
                                        placeholder="Enter Description", 
                                        style={"height": "80px"}),
                                    width=8,
                                ),
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