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

academic_clusters = {
    "AL": "Arts and Letters",
    "ME": "Management and Economics",
    "ST": "Science and Technology",
    "SSL": "Social Sciences and Law"
}

college = {
    "AL": [
        "College of Arts and Letters",
        "College of Fine Arts",
        "College of Human Kinetics",
        "College of Mass Communication",
        "College of Music"
    ],
    "ME": [
        "Asian Institute of Tourism",
        "Cesar E.A. Virata School of Business",
        "School of Economics",
        "School of Labor and Industrial Relations",
        "National College of Public Administration and Governance",
        "School of Urban and Regional Planning",
        "Technology Management Center",
        "UPD Extension Program in Pampanga and Olongapo"
    ],
    "ST": [
        "School of Archaeology",
        "College of Architecture",
        "College of Engineering",
        "College of Home Economics",
        "College of Science",
        "School of Library and Information Studies",
        "School of Statistics"
    ],
    "SSL": [
        "Asian Center",
        "College of Education",
        "Institute of Islamic Studies",
        "College of Law",
        "College of Social Sciences and Philosophy",
        "College of Social Work and Community Development"
    ]
}

cancel_modal = dbc.Modal(
    [
        dbc.ModalHeader("Cancel Confirmation"),
        dbc.ModalBody("Are you sure you want to cancel?"),
        dbc.ModalFooter(
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Yes", id="cancel-yes-button", color="danger"), width=6),
                    dbc.Col(dbc.Button("No", id="cancel-no-button", color="secondary"), width=6),
                ]
            )
        ),
    ],
    id="cancel-modal",
)


form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Complete Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='complete-name-input', placeholder="Last Name, First Name, Middle Initial"),
                    width=8,
                ),
            ],
            className="mb-2",
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
                        id='position-select',
                        options=[
                        {"label": "Professor 1", "value": "Professor 1"},
                        {"label": "Professor 2", "value": "Professor 2"},
                        {"label": "Professor 3", "value": "Professor 3"},
                        {"label": "Professor 4", "value": "Professor 4"},
                        {"label": "Professor 5", "value": "Professor 5"},
                        {"label": "Professor 6", "value": "Professor 6"},
                        {"label": "Professor 7", "value": "Professor 7"},
                        {"label": "Professor 8", "value": "Professor 8"},
                        {"label": "Professor 9", "value": "Professor 9"},
                        {"label": "Professor 10", "value": "Professor 10"},
                        {"label": "Professor 11", "value": "Professor 11"},
                        {"label": "Professor 12", "value": "Professor 12"},
                        {"label": "Assistant Professor 1", "value": "Assistant Professor 1"},
                        {"label": "Assistant Professor 2", "value": "Assistant Professor 2"},
                        {"label": "Assistant Professor 3", "value": "Assistant Professor 3"},
                        {"label": "Assistant Professor 4", "value": "Assistant Professor 4"},
                        {"label": "Assistant Professor 5", "value": "Assistant Professor 5"},
                        {"label": "Assistant Professor 6", "value": "Assistant Professor 6"},
                        {"label": "Assistant Professor 7", "value": "Assistant Professor 7"},
                        {"label": "Associate Professor 1", "value": "Associate Professor 1"},
                        {"label": "Associate Professor 2", "value": "Associate Professor 2"},
                        {"label": "Associate Professor 3", "value": "Associate Professor 3"},
                        {"label": "Associate Professor 4", "value": "Associate Professor 4"},
                        {"label": "Associate Professor 5", "value": "Associate Professor 5"},
                        {"label": "Associate Professor 6", "value": "Associate Professor 6"},
                        {"label": "Associate Professor 7", "value": "Associate Professor 7"},
                        {"label": "Instructor 1", "value": "Instructor 1"},
                        {"label": "Instructor 2", "value": "Instructor 2"},
                        {"label": "Instructor 3", "value": "Instructor 3"},
                        {"label": "Instructor 4", "value": "Instructor 4"},
                        {"label": "Instructor 5", "value": "Instructor 5"},
                        {"label": "Instructor 6", "value": "Instructor 6"},
                        {"label": "Instructor 7", "value": "Instructor 7"},
                        ],
                        placeholder="Select position",
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
                        "Academic Cluster ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='academic-cluster-dropdown',
                        options=[{"label": name, "value": code} for code, name in academic_clusters.items()],
                        placeholder="Select Academic Cluster",
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
                        "College ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dcc.Dropdown(
                       id='college-dropdown',
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
                    dbc.Input(type="text", id='department-input', placeholder="Enter Department"),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Label(
                    "TRAINING DETAILS",
                    width=8,
                    style={"font-size": "20px", "font-weight": "bold"}  # Style for larger and bold font
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "QA Training Attended ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='qa-training-select',
                        options=[
                            {"label": "AUN-QA Tier 1", "value": "AUN-QA Tier 1"},
                            {"label": "AUN-QA Tier 2", "value": "AUN-QA Tier 2"},
                            {"label": "AUN-QA Tier 3", "value": "AUN-QA Tier 3"},
                            {"label": "AUN-QA SAR Writing Workshop", "value": "AUN-QA SAR Writing Workshop"},
                            {"label": "UP System External Reviewers Training", "value": "UP System External Reviewers Training"},
                            {"label": "Other", "value": "Other"}
                        ],
                        placeholder="Select QA Training"
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Input(id='other-qa-training-input', placeholder="Specify if Other", style={'display': 'none'}),
                    width={"size": 8, "offset": 4},
                )
            ],
            className="mb-1",
            id='other-qa-training-row'
        ),
        dbc.Row(
           [
               dbc.Label(
                   [
                       "Date of Departure ",
                        html.Span("*", style={"color": "#F8B237"})
                   ],
                   width=4
               ),
               dbc.Col(
                   dcc.DatePickerSingle(
                       id='date-of-departure-input',
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
                       "Date of Return ",
                        html.Span("*", style={"color": "#F8B237"})
                   ],
                   width=4
               ),
               dbc.Col(
                   dcc.DatePickerSingle(
                       id='date-of-return-input',
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
                        "Training Venue/Location ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='training-venue-input', placeholder="Venue Name, City, Country"),
                    width=8,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Label(
                    "LIQUIDATION REQUIREMENTS",
                    width=12,
                    className="mb-2",
                    style={"font-size": "20px", "font-weight": "bold"}  # Style for larger and bold font
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Certificate of Participation/Attendance ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-certificate',
                        children=html.Div(
                            [
                            html.Img(src=app.get_asset_url('add_file.png'), style={'height': '15px', 'marginRight': '5px'}),
                            "add file"
                        ],
                        style={
                            'display': 'flex',
                            'alignItems': 'center'
                        }
                    ),
                    style={
                        'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                        'borderWidth': '1px', 'borderStyle': 'solid',
                        'borderRadius': '5px', 'textAlign': 'center',
                        'margin': '5px', 'display': 'flex',
                        'alignItems': 'center', 'justifyContent': 'center'
                    },
                    multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Receipt of Training Attended ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-training-receipt',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('add_file.png'),
                                    style={'height': '15px', 'marginRight': '5px'}
                                ),
                                "add file"
                            ],
                            style={'display': 'flex', 'alignItems': 'center'}
                        ),
                        style={
                            'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                            'borderWidth': '1px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Travel Report ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-travel-report',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('add_file.png'),
                                    style={'height': '15px', 'marginRight': '5px'}
                                ),
                                "add file"
                            ],
                            style={'display': 'flex', 'alignItems': 'center'}
                        ),
                        style={
                            'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                            'borderWidth': '1px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other Receipts ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-other-receipts',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('add_file.png'),
                                    style={'height': '15px', 'marginRight': '5px'}
                                ),
                                "add file"
                            ],
                            style={'display': 'flex', 'alignItems': 'center'}
                        ),
                        style={
                            'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                            'borderWidth': '1px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    "Receiving Copy (Optional) ",
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='upload-receiving-copy',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('add_file.png'),
                                    style={'height': '15px', 'marginRight': '5px'}
                                ),
                                "add file"
                            ],
                            style={'display': 'flex', 'alignItems': 'center'}
                        ),
                        style={
                            'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                            'borderWidth': '1px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                        multiple=True
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),
       dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Submit", id="submit-button", color="primary", className="me-3", style={"font-weight": "bold", "font-size": "18px"}),
                    width={"size": 2, "offset": 4}
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", style={"font-weight": "bold", "font-size": "18px"}, id="cancel-button"),
                    width={"size": 2}
                ),
            ],
            className="mb-4",
        ),
        cancel_modal
   ],
   className="g-2",
)


@app.callback(
    Output('college-dropdown', 'options'),
    Input('academic-cluster-dropdown', 'value')
)
def set_college_options(selected_cluster):
    if selected_cluster:
        return [{'label': i, 'value': i} for i in college[selected_cluster]]
    return []

@app.callback(
    Output('other-qa-training-input', 'style'),
    [Input('qa-training-select', 'value')]
)
def toggle_other_input(selected_training):
    if selected_training == 'Other':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('certificate-output-container', 'children'),
    Input('upload-certificate', 'contents'),
    State('upload-certificate', 'filename'),
    prevent_initial_call=True
)
def upload_certificate(contents, filename):
    if contents is not None:
        return html.Div([
            html.H5("Certificate Uploaded"),
            html.P(f"Filename: {filename}")
        ])

@app.callback(
    Output('official-receipt-output-container', 'children'),
    Input('upload-official-receipt', 'contents'),
    State('upload-official-receipt', 'filename'),
    prevent_initial_call=True
)
def upload_official_receipt(contents, filename):
    if contents is not None:
        return html.Div([
            html.H5("Official Receipt Uploaded"),
            html.P(f"Filename: {filename}")
        ])

@app.callback(
    Output('official-travel-report-output-container', 'children'),
    Input('upload-official-travel-report', 'contents'),
    State('upload-official-travel-report', 'filename'),
    prevent_initial_call=True
)
def upload_official_travel_report(contents, filename):
    if contents is not None:
        return html.Div([
            html.H5("Official Travel Report Uploaded"),
            html.P(f"Filename: {filename}")
        ])

@app.callback(
    Output('other-receipts-output-container', 'children'),
    Input('upload-other-receipts', 'contents'),
    State('upload-other-receipts', 'filename'),
    prevent_initial_call=True
)
def upload_other_receipts(contents, filename):
    if contents is not None:
        return html.Div([
            html.H5("Other Receipts Uploaded"),
            html.P(f"Filename: {filename}")
        ])
    
@app.callback(
    Output('receiving-copy-output-container', 'children'),
    Input('upload-receiving-copy', 'contents'),
    State('upload-receiving-copy', 'filename'),
    prevent_initial_call=True
)
def upload_receiving_copy(contents, filename):
    if contents is not None:
        return html.Div([
            html.H5("Receiving Copy Uploaded"),
            html.P(f"Filename: {filename}")
        ])

@app.callback(
    Output('submit-button', 'disabled'),
    Input('complete-name-input', 'value'),
    Input('position-select', 'value'),
    Input('academic-cluster-dropdown', 'value'),
    Input('college-dropdown', 'value'),
    Input('department-input', 'value'),
    Input('qa-training-select', 'value'),
    Input('upload-certificate', 'contents'),
    Input('upload-official-receipt', 'contents'),  # Add input for Official Receipt of Training Attended
    Input('upload-official-travel-report', 'contents'),  # Add input for Official Travel Report
    Input('upload-other-receipts', 'contents'),  # Add input for Other Receipts
    prevent_initial_call=True
)
def enable_submit(complete_name, position, academic_cluster, college, department, qa_training, certificate_contents, official_receipt_contents, travel_report_contents, other_receipts_contents):
    if all([complete_name, position, academic_cluster, college, department, qa_training, certificate_contents, official_receipt_contents, travel_report_contents, other_receipts_contents]):
        return False
    else:
        return True

@app.callback(
    Output("cancel-modal", "is_open"),
    [Input("cancel-button", "n_clicks"), Input("cancel-yes-button", "n_clicks"), Input("cancel-no-button", "n_clicks")],
    [State("cancel-modal", "is_open")],
)
def toggle_modal(cancel_btn_click, yes_btn_click, no_btn_click, is_open):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "cancel-button":
            return True
        elif prop_id == "cancel-yes-button":
            # Redirect to cancel_page or any other action you want to perform
            return True, "/training_instructions"
        elif prop_id == "cancel-no-button":
            return False
    return is_open
    
layout = html.Div(
   [
       dbc.Row(
           [
               #navbar
               dbc.Col(
                   cm.generate_navbar(),
                   width=2
               ),


               #title
               dbc.Col(
               [
                   html.H1("ADD TRAINING DOCUMENT"),
                   html.Hr(),


                   #working form
                   form,
               ],
               width=8, style={'marginLeft': '15px'}
              
               )
           ]
       ),
       #footer
       dbc.Row (
           [
               dbc.Col(
                   cm.generate_footer(), width={"size": 12, "offset": 0}
               ),
           ]
       )
   ]
)