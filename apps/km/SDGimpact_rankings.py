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

criteria_data = pd.DataFrame({
    "Criteria Name": ["SAMPLE NAME", "SAMPLE NAME"],
    "Criteria ID.": ["Criteria 2.1.1", "Criteria 2.1.2"],
    "Description": ["Sample Description", "Sample Description"]
})

evidence_data = pd.DataFrame({
    "Title": ["XXX Building"],
    "Office": ["IEORD"],
    "Summary": ["Short Description..."],
    "Ranking Body": ["THE"],
    "Applicable Criteria": ["Criteria 1, 2, 3"]
})


criteria_checklist = dbc.Card(
    [
        dbc.CardHeader("Manage Approved Evidence", className= "fw-bold"),
        dbc.CardBody(
            [
                dbc.Checklist(
                    options=[
                        {"label": f"Criteria {i}", "value": i} for i in range(1, 7)
                    ],
                    id="evidence-criteria",
                    inline=True,
                    inputClassName="me-1"  # Margin to the right of the checkbox
                ),
                # Additional content can be added here
            ]
        )
    ]
)

data_revisions = pd.DataFrame({
    "Title": ["XXX Building"],
    "Office": ["HRDO"],
    "Summary": ["Short Description..."],
    "Action": ["add revision"]
})

data_checking = pd.DataFrame({
    "Title": ["XXX Building", "XXX Building", "XXX Building"],
    "Office": ["IEORD", "IEORD", "IEORD"],
    "Summary": ["Short Description...", "Short Description...", "Short Description..."],
    "Action": ["check submission", "check submission", "check submission"]
})

data_approved = pd.DataFrame({
    "Title": ["XXX Building"],
    "Office": ["IEORD"],
    "Summary": ["Short Description..."],
    "Action": ["view"]
})

def create_evidence_table(table_id, data, title):
    return dbc.Card(
        [
            dbc.CardHeader(html.H6(title, className="mb-0", style={'fontWeight': 'bold'})),
            dbc.CardBody(
                dash_table.DataTable(
                    id=table_id,
                    columns=[{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict('records'), 
                    editable=True,  # Set to False if you don't want cells to be editable
                    row_deletable=True,  # Set to False if you don't want to allow row deletion
                )
            ),  
        ], style={'marginBottom': '20px'} 
    )

add_criteria_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.H4("ADD CRITERIA", className="fw-bold")),
        dbc.ModalBody(
            [
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "SDG # ",
                                        html.Span("*", style={"color": "#F8B237"})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Textarea(placeholder="Enter SDG #", style={"height": "30px"}),
                                    width=8,
                                ),
                            ],
                            className="mb-1",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Criteria Code ",
                                        html.Span("*", style={"color": "#F8B237"})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Textarea(placeholder="Enter Criteria Code", style={"height": "30px"}),
                                    width=8,
                                ),
                            ],
                            className="mb-1",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Description ",
                                        html.Span("*", style={"color": "#F8B237"})
                                    ],
                                    width=4
                                ),
                                dbc.Col(
                                    dbc.Textarea(placeholder="Enter Description", style={"height": "80px"}),
                                    width=8,
                                ),
                            ],
                            className="mb-3",
                        ),
                    ]
                ),
            ]
        ),
        dbc.ModalFooter(
            [
                dbc.Button("Save", id="save-criteria-btn", className="ml-auto"),
                dbc.Button("Cancel", id="close-criteria-btn", className="ml-auto"),
            ]
        ),
    ],
    id="add-criteria-modal",
    centered=True,
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("ADD CRITERIA"),
                        html.Hr(),

                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add criteria", color="primary", 
                                        href='add_criteria', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "📁 Upload CSV File", color="danger",   
                                    ),
                                    width="auto",    
                                )
                            ],
                        ),

                        html.Br(),
 
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='SDGimpactrankings_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ]
                        ),
                        
                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dash_table.DataTable(
                                        id='criteria-table',
                                        columns=[
                                            {"name": i, "id": i} for i in criteria_data.columns
                                        ],
                                        data=criteria_data.to_dict('records'),
                                        style_header={'fontWeight': 'bold'},
                                    ),
                                    width=12
                                )
                            ],
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    criteria_checklist, width=12, className="mb-3 ",
                                ),
                                dbc.Col(
                                    [
                                        dash_table.DataTable(
                                            id='evidence-table',
                                            columns=[
                                                {"name": i, "id": i} for i in evidence_data.columns
                                            ],
                                            data=evidence_data.to_dict('records'),
                                            style_header={'fontWeight': 'bold'},
                                        )
                                    ],
                                    width=12
                                )
                            ],
                            className="mb-3",
                        ),

                        html.Div(
                            [
                                html.Br(),
                                html.Hr(),
                                dbc.Row(   
                                    [
                                        dbc.Col(   
                                            html.H5("SUBMITTED EVIDENCES"),
                                        ), 
                                        dbc.Col(   
                                            dbc.Button(
                                                "➕ Add Submission", color="primary", 
                                                href='/SDGimpactrankings/SDG_submission', 
                                            ),
                                            width="auto",    
                                            className="mb-3",
                                        ), 
                                        dbc.Col(   
                                            dbc.Button(
                                                "✍🏻 Add Revision", color="warning", 
                                                href='/SDGimpactrankings/SDG_revision', 
                                            ),
                                            width="auto",    
                                            className="mb-3",
                                        ), 
                                    ],
                                ),
                                create_evidence_table('table-revisions', data_revisions, "Submissions in need of Revisions"),
                                create_evidence_table('table-checking', data_checking, "Submissions for Checking"),
                                create_evidence_table('table-approved', data_approved, "Approved Submissions"),
                            ]
                        )
                    ], 
                    width=9,  style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        ),
        add_criteria_modal,
    ]
)

@app.callback(
    Output("add-criteria-modal", "is_open"),
    [Input("open-criteria-modal-btn", "n_clicks"), Input("close-criteria-btn", "n_clicks")],
    [State("add-criteria-modal", "is_open")],
)
def toggle_add_criteria_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
