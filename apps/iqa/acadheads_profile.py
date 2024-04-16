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
                    dbc.Input(id="unithead_sname", type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_fname",type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Name", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_mname",type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("UP Mail", width=4),
                dbc.Col(
                    dbc.Input(id="unithead_upmail",type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
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
                        id='unithead_cluster_id',
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
                        id='unithead_college_id',
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
                        id='unithead_deg_unit_id',
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
                    dbc.Input(id='unithead_cuposition', type="text"),
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
                            id="unithead_basicpaper",
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
                        id="unithead_remarks",
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
                    dbc.Input(id="unithead_alc", type="text"),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Start of Term", width=4),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='unithead_appointment_start',
                        date=str(pd.to_datetime("today").date()), 
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("End of Term", width=4),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='unithead_appointment_end',
                        date=str(pd.to_datetime("today").date()), 
                    ),
                    width=8,
                ),
            ],
            className="mb-3", 
                                    
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Register", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
            ],
            className="mb-2",
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4('Expense added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='unithead_successmodal',
            backdrop=True,   
            className="modal-success"  
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
