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
                dbc.Label("Degree Program Title", html_for="degree-program-title", width=4),
                dbc.Col(
                    dbc.Input(id="degree-program-title", type="text"),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Cluster", html_for="cluster", width=4),
                dbc.Col(
                    dbc.Input(id="cluster", type="text"),
                    width=6,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Assessment Title", html_for="assessment-title", width=4),
                dbc.Col(
                    dbc.Input(id="assessment-title", type="text"),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Approved EQA Type", html_for="eqa-type", width=4),
                dbc.Col(
                    dbc.Select(
                        id="eqa-type",
                        options=[
                            {"label": "Type A", "value": "Type A"},
                            {"label": "Type B", "value": "Type B"},
                            {"label": "Type C", "value": "Type C"},
                            {"label": "Type D", "value": "Type D"},
                            {"label": "Type E", "value": "Type E"},
                            {"label": "Type F", "value": "Type F"},
                        ],
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("To be Assessed by", html_for="assessed-by", width=4),
                dbc.Col(
                    dbc.Select(
                        id="assessed-by",
                        options=[
                            {"label": "Engineering Accreditation Commission", "value": "Engineering Accreditation Commission"},
                            {"label": "International Accreditation", "value": "International Accreditation"},
                            {"label": "Local Accreditation", "value": "Local Accreditation"},
                        ],
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Is there a scheduled assessment date?", html_for="scheduled-assessment", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="scheduled-assessment",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                            ],
                            inline=True,  
                        ),
                ),
            ], 
        ), 

        
        # Additional field for "Scheduled Assessment Date"
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Label("Scheduled Assessment Date", html_for="scheduled-assessment-date"),  width=5, 
                             className="align-self-center",
                        ),
                        dbc.Col(
                            dbc.Input(id="scheduled-assessment-date", type="date"),  width=4
                        ),
                    ],
                    
                ), 
            ],
            className="mb-1",
            style={"display": "none"},  # Initially hide the field
            id="scheduled-assessment-date-field"
        ),  

        dbc.Row(
            [
                dbc.Label("Report type", html_for="report-type", width=4),
                dbc.Col(
                    dbc.Select(
                        id="report-type",
                        options=[
                            {"label": "Self-Assessment Report", "value": "Self-Assessment Report"},
                            {"label": "EQA Endorsement", "value": "EQA Endorsement"},
                            {"label": "EQA Assessment", "value": "EQA Assessment"},
                            {"label": "Post QA report", "value": "Post QA report"},
                        ],
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Link", html_for="link", width=4),
                dbc.Col(
                    dbc.Input(id="link", type="text"),
                    width=8,
                ),
            ],
            className="mb-1",
        ), 
        dbc.Row(
            [
                dbc.Col(
                    dbc.Label("PDF File", width=4),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label("Check Status", html_for="check-status", width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="check-status",
                        options=[
                            {"label": "For Checking", "value": "For Checking"},
                            {"label": "Already Checked", "value": "Already Checked"},
                        ],
                        inline=True,  # Display radio items inline
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),

        # Additional fields for "Already Checked" option
        dbc.Row(
            [
                dbc.Row (
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Date Reviewed", html_for="date-reviewed"), width=5),
                                dbc.Col(dbc.Input(id="date-reviewed", type="date"), width=4),
                            ],
                            className="mb-1", 
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Review Status", html_for="review-status"), width=5 ),
                                dbc.Col(
                                    dbc.Select(
                                        id="review-status",
                                        options=[
                                            {"label": "Incomplete SAR", "value": "Incomplete SAR"},
                                            {"label": "Initial Review", "value": "Initial Review"},
                                            {"label": "1st Iteration", "value": "1st Iteration"},
                                            {"label": "2nd Iteration", "value": "2nd Iteration"},
                                            {"label": "3rd Iteration", "value": "3rd Iteration"},
                                            {"label": "Presented to QAO", "value": "Presented to QAO"},
                                            {"label": "Post EQA", "value": "Post EQA"},
                                        ],
                                    ),
                                    width=4,
                                ),
                            ],
                            className="mb-1", 
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Notes", html_for="notes"), width=5),
                                dbc.Col(
                                    dbc.Textarea(id="notes", style={'resize': 'vertical', 'minHeight': '50px', 'maxHeight': '200px'}),
                                    width=6, className="ml-2"
                                ),
                            ],
                            className="mb-1", 
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("SAR Score", html_for="sar-score"), width=5),
                                dbc.Col(dbc.Input(id="sar-score", type="number"), width=4),
                            ],
                            
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
                dbc.Col(
                    dbc.Label("Ready for presenting to QAO?", html_for="ready-for-qao"),width=4,  
                    className="align-self-center",  # Vertically center the label
                ),
                dbc.Col(
                    dbc.RadioItems(
                        id="ready-for-qao",
                        options=[
                            {"label": "Yes", "value": "Yes"},
                            {"label": "No", "value": "No"},
                        ],
                        inline=True,  
                    ),
                    width=4, 
                ),
            ],
            className="mb-1",
        ),

        
        # Additional fields for "Ready for presenting to QAO?" option
        dbc.Row(
            [
                dbc.Row(
                    [
                         dbc.Row(
                            [
                                dbc.Col(dbc.Label("Date to be presented to QAO", html_for="date-presented-to-qao"), width=5),
                                dbc.Col(dbc.Input(id="date-presented-to-qao", type="date"), width=6),
                            ],
                            className="mb-1",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Mode of External Quality Assurance Assessment/Accreditation/Review", html_for="mode-of-external-qa"), width=5  ),
                                dbc.Col(
                                    dbc.Select(
                                        id="mode-of-external-qa",
                                        options=[
                                            {"label": "Within the CU", "value": "Within the CU"},
                                            {"label": "Another CU", "value": "Another CU"},
                                            {"label": "Outside UP - Local", "value": "Outside UP - Local"},
                                            {"label": "Outside UP - International", "value": "Outside UP - International"},
                                        ]
                                    ),
                                    width=6, className="ml-2"
                                ),
                            ],
                            className="mb-1",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Specific EQA Assessment/Accreditation/Review", html_for="specific-qa"), width=5 ),
                                dbc.Col(
                                    dbc.Select(
                                        id="specific-qa",
                                        options=[
                                            {"label": "A-EQA by assessors/external reviewers from within the CU", "value": "A-EQA"},
                                            {"label": "D-EQA by assessors/external reviewers from outside UP", "value": "D-EQA"},
                                            {"label": "F-EQA by an international accrediting/assessing body", "value": "F-EQA"},
                                        ]
                                    ),
                                    width=6, 
                                ),
                            ],
                            className="mb-1 ",
                        )
                    ]
                )
            ],
            className="mb-1",
            style={"display": "none"},  # Initially hide the fields
            id="ready-for-qao-fields"
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