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

def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  # Add space below each card
    )
 
def create_table(headers, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in headers],
        style_header={'fontWeight': 'bold'}, 
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
                        html.H1("EQA DASHBOARD"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(create_card("SUMMARY OF DEGREE PROGRAMS WITH EQA"), width=8),
                                dbc.Col(create_card("SAR SUBMISSIONS 2024"), width=4),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(create_card(
                                    dbc.Col(
                                    [
                                        "ASSESSMENT SCHEDULE",
                                        create_table(["Program Name", "Type of Assessment", "Scheduled Assessment Date"], "assessment-schedule-table")
                                    ]
                                )
                                ), width=12),
                                
                            ]
                        ),
                        

                        
                        dbc.Row(
                            [
                                dbc.Col(create_card(
                                    dbc.Col(
                                    [
                                        "ONGOING ASSESSMENTS",
                                        create_table(["Department", "College", "Progress", "ECY"], "ongoing-assessments-table")
                                    ]
                                )
                                ), width=8),

                                dbc.Col(create_card(
                                    dbc.Col(
                                    [
                                        "Progress Summary"
                                    ]
                                )
                                ), width=4),
                                
                            ]
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