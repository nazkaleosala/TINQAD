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
         
        dbc.Row(
            [
                dbc.Label("Degree Program Title",   width=4),
                 
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Cluster",  width=4),
                 
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label("Assessment Title", width=4),
                dbc.Col(
                    dbc.Input(id="arep_title", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Date ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                       id='arep_currentdate ',
                       date=str(pd.to_datetime("today").date())
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
                       "Approved EQA Type",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_approv_eqa',
                        placeholder="Select EQA Type",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("To be Assessed by", width=4),
                dbc.Col(
                    dbc.Select(
                        id="arep_assessedby",
                        options=[
                            {"label": "Engineering Accreditation Commission", "value": "Engineering Accreditation Commission"},
                            {"label": "International Accreditation", "value": "International Accreditation"},
                            {"label": "Local Accreditation", "value": "Local Accreditation"},
                        ],
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("UP Mail", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_upmail",type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Is there a scheduled assessment date?", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="arep_qscheddate",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            ],
                            inline=True,  
                        ),
                ),
            ],
            className="mb-2", 
        ), 
        
        
        dbc.Row(
            [
                dbc.Label("Scheduled Assessment Date", width=4),
                dbc.Col(
                    dbc.Input(type="date", id='arep_sched_assessdate'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
 

        dbc.Row(
            [
                dbc.Label(
                    [
                       "Report type",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_report_type',
                        placeholder="Select Report Type",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        
        dbc.Row(
            [
                dbc.Label("Link", width=4),
                dbc.Col(
                    dbc.Input(id="arep_link", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("PDF File", width=4),
                dbc.Col(
                    dbc.Input(id="arep_pdf", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        
        dbc.Row(
            [
                dbc.Label("Check Status", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="arep_checkstatus ",
                        options=[
                            {"label": "For Checking", "value": "For Checking"},
                            {"label": "Already Checked", "value": "Already Checked"},
                            ],
                            inline=True,  
                        ),
                ),
            ],
            className="mb-2", 
        ), 

        # Additional fields for "Already Checked" option
        dbc.Row(
            [
                dbc.Row (
                    [
                
                        dbc.Row(
                            [
                                dbc.Label("Date to be Reviewed", width=4),
                                dbc.Col(
                                    dbc.Input(type="date", id='arep_datereviewed '),
                                    width=4,
                                ),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                    "Review Status",
                                        html.Span("*", style={"color":"#F8B237"})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='arep_review_status',
                                        placeholder="Select Review Status",
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
                                        "Notes"
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                dbc.Textarea(id='arep_notes', placeholder="Add notes"),
                                width=8,
                                ),
                            ],
                            className="mb-2",
                        ),

                        dbc.Row(
                            [
                                dbc.Label("SAR Score", width=4),
                                dbc.Col(
                                    dbc.Input(id="arep_sarscore",type="number"),
                                    width=3,
                                ),
                            ],
                            className="mb-2",
                        ),
                    ]
                )
            ],
            className="mb-1", 
            style={"display": "none"},  # Initially hide the fields
            id="already-checked-fields"
        ),

 
         

        dbc.Row(
            [
                dbc.Label("Ready for presenting to QAO?", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="arep_qqaopresent",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            ],
                            inline=True,  
                        ),
                ),
            ],
            className="mb-2", 
        ), 

        # Additional fields for "Ready for presenting to QAO?" option
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Date to be presented to QAO", width=4),
                                dbc.Col(
                                    dbc.Input(type="date", id='arep_presdate'),
                                    width=4,
                                ),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                    "Mode of EQA Assessment", 
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='arep_mode_eqa_assess',
                                        placeholder="Select Mode",
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
                                    "Specific EQA Assessment", 
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='arep_spec_eqa_assess',
                                        placeholder="Select EQA",
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-2",
                        ),
                    ]
                )
            ],
            className="mb-1",
            style={"display": "none"},  # Initially hide the fields
            id="ready-for-qao-fields"
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
                    html.H4('QA Officer profile added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                       "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='arep_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
         
    ]
)



 



 



  


# Define callback to show/hide additional fields based on radio button selection
@app.callback(
    [Output("already-checked-fields", "style"),
     Output("ready-for-qao-fields", "style"),
     Output("scheduled-assessment-date-field", "style")],
    [Input("check-status", "value"),
     Input("ready-for-qao", "value"),
     Input("scheduled-assessment", "value")]
)


def toggle_additional_fields(check_status, ready_for_qao, scheduled_assessment):
    if check_status == "Already Checked":
        already_checked_style = {"display": "block"}  # Show the "Already Checked" fields
    else:
        already_checked_style = {"display": "none"}  # Hide the "Already Checked" fields
        
    if ready_for_qao == "Yes":
        ready_for_qao_style = {"display": "block"}  # Show the "Ready for presenting to QAO?" fields
    else:
        ready_for_qao_style = {"display": "none"}  # Hide the "Ready for presenting to QAO?" fields
    
    if scheduled_assessment == "Yes":
        scheduled_assessment_style = {"display": "block"}  # Show the "Scheduled Assessment Date" field
    else:
        scheduled_assessment_style = {"display": "none"}  # Hide the "Scheduled Assessment Date" field
    
    return already_checked_style, ready_for_qao_style, scheduled_assessment_style

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
                            ]
                        )
                    ], width=8, style={'marginLeft': '15px'}
                ),   
            ]
        ),
        
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}, 
                ),
            ], className="mt-4"
        )
    ]
)