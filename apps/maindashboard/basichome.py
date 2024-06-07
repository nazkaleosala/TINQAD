import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback_context  

import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
 
from datetime import datetime 
import calendar 

def create_time_date_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(id="time", style={"font-size": "2em", "font-weight": "bold", "text-align": "center", "margin-bottom": "0"}),
                html.P(id="date", style={"text-align": "center", "margin-top": "0"}),
            ]
        ),
        className="mb-3",
        style={"backgroundColor": "#FFFFFF"}
    )

def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month


# Announcements content card
basickmannounce_content = html.Div(
    [
                html.Div(id="basickmann_display",
                         style={
                            'overflowX': 'auto',
                            'overflowY': 'auto',
                            'height': '300px', 
                         }),
                html.Br(),
                html.Div(
                    [
                        html.Div(id="basickmann_status"),
                        html.Br(),
                        dbc.Input(
                            id="basickmann_header",
                            placeholder="Format: Deadline Date, if urgent type URGENT. ex. May 05, 2024 URGENT.",
                            type="text",
                        ),
                        dbc.Textarea(
                            id="basickmann_content",
                            placeholder="Type a message...",
                            style={"resize": "vertical"},
                            rows=5,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Post", id="basickmannpost_button", color="success",
                                               className="mt-2"),
                                    width="auto",
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", id="basickmanncancel_button", color="warning",
                                               className="mt-2"),
                                    width="auto",
                                ),
                            ],
                            style={"justify-content": "flex-end"},
                        ),
                    ],
                    id="basickmann_id",
                    style={"display": "none"},  # Initially hidden
                ),
            ]
        )

# Announcements footer card
basickmannounce_footer = html.Div(
    [
        dbc.Button(
            "Add Announcement",
            id="basickmann_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)

app.layout = html.Div([basickmannounce_content, basickmannounce_footer, dcc.Location(id="url", refresh=False)])

 


   

layout = html.Div(
    [
        html.Div(  
                [
                dcc.Store(id='homeid_store', storage_type='session', data=0),
                ]
            ),
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1(html.B("👋 Welcome!")), 
                        html.Br(), 
                        dbc.Alert(
                                id="basic_kmann_alert", 
                                is_open=False, 
                                dismissable=True, 
                                duration=None, 
                                color="info"
                            ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(html.H3("KM Announcements")),
                                            dbc.CardBody(
                                                [
                                                    basickmannounce_content,
                                                    basickmannounce_footer,
                                                ]
                                            ),
                                        ]
                                    ),
                                    width="auto",
                                    className="mb-3"
                                ),
                                
                                dbc.Col(
                                    [
                                        create_time_date_card(),
                                        dcc.Interval(
                                        id="interval-component",
                                        interval=1*1000,  # in milliseconds
                                        n_intervals=0
                                        )
                                    ], width="auto",
                                )
                            ],
                            className="mb-3",
                            style={"backgroundColor": "#FFFFFF"},
                        ),
                         
                    ], width=8
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

 