from dash import dash, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db



                        


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("SDG MANAGE EVIDENCE LIST"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add Submission",
                                        color="primary",
                                        href='/SDGimpactrankings/SDG_submission?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "✍🏻 Add Revision",
                                        color="warning",
                                        href='/SDGimpactrankings/SDG_revision?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                            ]
                        ),

                         

                        html.Br(), 

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions for Checking"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='checking_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px', 
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions in need of Revisions"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='revisions_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px',
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ),
                         

                        html.Br(),
                        html.Hr(),
 

                        html.Div(
                            [
                                 
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(html.B("View Revised Evidence")),
                                            width=8,
                                        ),
                                    ],
                                    justify="between",  
                                ),
                                html.Br(),   
                                
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Approved Revisions"),
                                                dbc.CardBody(
                                                    html.Div(
                                                        id='checkedrevisions_list', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto',
                                                            'overflowY': 'auto',
                                                            'maxHeight': '500px',
                                                        }
                                                    )
                                                )
                                            ],
                                            color="light"
                                        ),
                                        width="12"
                                    )
                                ),

                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Confirm Removal"),
                                        dbc.ModalBody("Remove evidence from list of revisions?"),
                                        dbc.ModalFooter(
                                            [
                                                dbc.Button("Cancel", id="sdgrevision_cancel_remove", color="secondary"),
                                                dbc.Button("Confirm", id="sdgrevision_confirm_remove", color="danger")
                                            ]
                                        ),
                                    ],
                                    centered=True,
                                    id='sdgrevision_confirmmodal',
                                    backdrop=True,   
                                    className="modal-success"  
                                )

                            ],
                        ),
                        html.Br(),    
                        html.Br(),    



                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)
 