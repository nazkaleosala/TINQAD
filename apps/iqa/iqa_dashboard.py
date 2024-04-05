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
from datetime import datetime

# Assuming commonmodules has a function to generate card like structures
def generate_card(header, body):
    card = dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.P(body, className="card-text"),
                ]
            ),
        ],
    )
    return card
 


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
                        html.H1("IQA DASHBOARD"),
                        html.Hr(),
                        
                        dbc.Row(
                            [
                                #Reports Card
                                dbc.Col(generate_card("IAADS REPORTS SUBMISSIONS",  ""
                                        
                                    ), 
                                ),
                                
                            ],
                            className="mb-4",
                        ),

                        dbc.Row(
                            [
                            
                                #Unit heads Card
                                dbc.Col(generate_card("ACADEMIC UNIT HEADS & QA OFFICERS", ""
                                                          
                                        
                                    )
                                ), 
                                    
                                
                            ],
                            className="mb-4",
                        ),
                         
                    ],
                    width=9,
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
