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
                    dbc.Input(id="unit_head_sname", type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(id="unit_head_fname",type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Name", width=4),
                dbc.Col(
                    dbc.Input(id="unit_head_mname",type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("UP Mail", width=4),
                dbc.Col(
                    dbc.Input(id="unit_head_upmail",type="email"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Position ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='fac_posn_id',
                        options=[],
                        placeholder="Select position",
                    ),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        
        dbc.Row(
              [
               dbc.Label(
                    [
                        "Cluster ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dcc.Dropdown(
                       id='cluster_id',
                       placeholder="Select Cluster",
                   ),
                   width=6,
               ),
           ],
           className="mb-2",
       ),
        
        dbc.Row(
              [
               dbc.Label(
                    [
                        "College ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dcc.Dropdown(
                       id='college_id',
                       placeholder="Select College",
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
                        "Department ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='deg_unit_id',
                        placeholder="Select Department",
                    ),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        html.H5("QA INFORMATION", className="form-header fw-bold"),
        dbc.Row(
            [
                dbc.Label("QA Position in the CU", width=4),
                dbc.Col(
                    dbc.Input(id='unit_head_cuposition', type="text"),
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
                            id="unit_head_basicpaper",
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
                        id="unit_head_remarks",
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
                    dbc.Input(id="unit_head_alc", type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Start of Term", width=4),
                dbc.Col(
                    dbc.Input(id="unit_head_appointment_start",type="text", placeholder="MM DD YYYY"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("End of Term", width=4),
                dbc.Col(
                    dbc.Input(id="unit_head_appointment_end",type="text", placeholder="MM DD YYYY"),
                    width=5,
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
                        html.H1("ADD NEW PROFILE"),
                        html.Hr(),
                        form, 
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


