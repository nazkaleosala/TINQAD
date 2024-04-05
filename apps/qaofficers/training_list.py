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
 


training_data = pd.DataFrame({
    "Name ": [
        "Name Surname ",
         
    ],
    "Rank/ Designation ": [
        "BS Industrial Engineering"
    ],
    "College ": [
        "Engineering"
    ],
    "Department ": [
        "IEORD"
    ],
    "Academic Cluster ": [
        "Science and Engineering"
    ],
    "Trainings ": [
        "Training 1, Training 2, Training 3.............."
    ]
})
  
 
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
                        html.H1("QA OFFICERS TRAINING LIST"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Officer", color="primary", 
                                        href='/qaofficers_profile', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "📁 Upload CSV File", color="danger",  
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "💾 Export as CSV File", color="secondary",  
                                    ),
                                    width="auto",    
                                ),
                            ],
                            className="align-items-center",   
                            style={
                                "margin-right": "2px",
                                "margin-bottom": "15px",
                            }
                        ), 
                        html.Div(
                            dash_table.DataTable(
                                id='criteria-table',
                                columns=[
                                    {"name": i, "id": i} for i in training_data.columns
                                ],
                                data=training_data.to_dict('records'),
                                style_header={'fontWeight': 'bold'},
                                style_data_conditional=[
                                    {
                                        'if': {'column_id': 'Last Accessed'},
                                        'color': 'blue'
                                    },
                                    {
                                        'if': {'column_id': 'Action'},
                                        'color': 'green'
                                    }
                                ]
                            ),
                            style={'overflowX': 'auto'}
                        ),
                    ], 
                    width=9, style={'marginLeft': '15px'}
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