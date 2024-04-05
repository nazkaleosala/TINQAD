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


card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Team Messages", tab_id="tab-team-msg"),
                    dbc.Tab(label="Announcements", tab_id="tab-announcements"),
                ],
                id="card-tabs",
                active_tab="tab-team-msg",
            )
        ),
        dbc.CardBody(
            [
                html.P(id="card-content", className="card-text"),
                html.Div(
                    dbc.Button("Add Message", color="primary"),
                    className="d-flex justify-content-end",
                    
                ),
            ]
        ),
    ] 
)



# Callback to update card content
@app.callback(
    Output("card-content", "children"), 
    [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    return f"This is {active_tab}"


#timeline column
timeline_card = dbc.Card(
    [
        dbc.CardHeader("UPCOMING EVENTS", className="text-center text-bold"),
        dbc.CardBody(
            [
                html.P("Some exciting event happening soon.", className="card-text"),
            ]
        ),
    ],
    className="mb-3"
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
                    [   # Main content goes here
                        html.H1("WELCOME, PIKA!", className="my-3"),
                        dbc.Row(
                            dbc.Col(
                                card, 
                                width=8, sm=12
                            )
                        ),
                        html.Br(),
                    
                    dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.A(
                                                    html.H5("Administration Team", className="card-title fw-bold text-dark"),
                                                    href='/administration_dashboard',
                                                    style={'text-decoration': 'none'}
                                                ),
                                                html.P(
                                                    "Some quick example text to build on the card title and "
                                                    "make up the bulk of the card's content.",
                                                    className="card-text"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#007DB3"}
                                    ),
                                    width=6, md=6, sm=12
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.A(
                                                    html.H5("External Quality Assurance Team", className="card-title fw-bold  text-dark"),
                                                    href='/eqa_dashboard',
                                                    style={'text-decoration': 'none'}
                                                ),
                                                html.P(
                                                    "Some quick example text to build on the card title and "
                                                    "make up the bulk of the card's content.",
                                                    className="card-text"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#D37157"}
                                    ),
                                    width=6, md=6, sm=12
                                ),
                            

                            ],
                            className="mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.A(
                                                    html.H5("Internal Quality Assurance Team", className="card-title fw-bold text-dark"),
                                                    href='/iqa_dashboard',
                                                    style={'text-decoration': 'none'}
                                                ),
                                                html.P(
                                                    "Some quick example text to build on the card title and "
                                                    "make up the bulk of the card's content.",
                                                    className="card-text"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#F8B237"}
                                    ),
                                    width=6, md=6, sm=12
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.A(
                                                    html.H5("Knowledge Management Team", className="card-title fw-bold  text-dark"), 
                                                    href='/km_dashboard',
                                                    style={'text-decoration': 'none'}
                                                ),
                                                html.P(
                                                    "Some quick example text to build on the card title and "
                                                    "make up the bulk of the card's content.",
                                                    className="card-text"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#39B54A"}
                                    ),
                                    width=6, md=6, sm=12
                                ),
                            ],
                            className="mb-3"
                        ),
                        
                    

                    ],
                    width=8,  
                ),
                dbc.Col(
                    [   # Right column for the timeline card
                        dbc.Row ([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.A(
                                                html.H5("Quality Assurance Officers", className="card-title fw-bold text-light text-center"), 
                                                href='/qa_officers',
                                                style={'text-decoration': 'none'}
                                            ),
                                        
                                        ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#7A0911"},
                                    ),
                                    
                                ),
                        ]),
                        timeline_card,  # Your new timeline card component
                    ],
                    width=2,  md=2, sm=12
                ),
            ],
            className="mb-3",
            style={'padding-bottom': '2rem'}
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