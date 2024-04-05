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
        html.H5("PERSONAL INFORMATION", className="form-header fw-bold"),
        dbc.Row(
            [
                dbc.Label("Surname", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Initial", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("UP Mail", width=4),
                dbc.Col(
                    dbc.Input(type="email"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Cluster Name ", width=4),
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
                dbc.Label("Unit", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-5",
        ),
        html.H5("QA INFORMATION", className="form-header fw-bold"),
        dbc.Row(
            [
                dbc.Label("QA Position in the CU", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("With Basic Paper as QAO?", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"}
                        ],
                            value="Yes",  # Set the default value to 'Yes' or 'No' as needed
                            id="basicpaperqao-radio",
                            inline=True
                    ), width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Remarks", width=4),
                dbc.Col(
                    dbc.Select(
                        id="remarks-select",
                        options=[
                            {"label": "For renewal", "value": "For renewal"},
                            {"label": "No record", "value": "No record"}
                        ],
                        placeholder="Select a remark"
                    ),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("ALC", width=4),
                dbc.Col(
                    dbc.Input(type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Start of Term", width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="MM DD YYYY"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("End of Term", width=4),
                dbc.Col(
                    dbc.Input(type="text", placeholder="MM DD YYYY"),
                    width=5,
                ),
            ],
            className="mb-3", 
                                    
        ),
    ]
)


trainings_table = dbc.Table(
    [
        html.Thead(
            html.Tr([html.Th("#", style={'width': '5%'}), html.Th("Date Trained", style={'width': '20%'}), html.Th("Name of Training", style={'width': '75%'})])
        ),
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td("1", style={'width': '5%'}), 
                        html.Td(dbc.Input(type="text", placeholder="MM/DD/YYYY"), style={'width': '20%'}), 
                        html.Td(dbc.Input(type="text", placeholder="AUNQA T1/International/Local"), style={'width': '75%'}),
                        html.Td(dbc.Button("+", color="primary", className="btn-sm"), style={'width': '5%'})
                    ]
                )
            ]
        )
    ],
    bordered=True,
    hover=True
)


card_form = dbc.Card(
    [
        dbc.CardHeader("QA Trainings"),
        dbc.CardBody(
            [trainings_table]
        )
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
                                
                                html.Div(card_form, 
                                    style={
                                        'margin-top': '50px',
                                        'margin-bottom': '50px'
                                        }
                                    )
                            ]
                        ),
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


