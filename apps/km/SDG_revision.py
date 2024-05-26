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
                dbc.Label("Select Evidence Name", width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdgr_evidencename',
                        options=[],
                    ),
                    width=4,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Ranking Body", width=4),
                dbc.Col(
                    html.P(id='sdgr_rankingbody'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Description", width=4),
                dbc.Col(
                    html.P(id='sdgr_description'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Office", width=4),
                dbc.Col(
                    html.P(id='sdgr_office_id'),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Accomplished by",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),

                dbc.Col(
                    dbc.Input(type="text", placeholder="Name Surname",id='sdgr_accomplishedby'),  
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Date Submitted", width=4),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='sdgr_datesubmitted',
                        date=str(pd.to_datetime("today").date()),  
                        clearable=True,
                    ),
                    width=4,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Check Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdgr_checkstatus',  
                        value='pending',
                    ),
                    width=5,
                ),
 
            ],
            className="mb-3"
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Submission Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdgrsubmission_type',
                        options=[
                            {"label": "File", "value": "file"},
                            {"label": "Link", "value": "link"},
                            {"label": "Both File and Link", "value": "both"},
                        ],
                        placeholder="Select Submission Type"
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "File Submissions ",
                        
                    ],
                    width=4,
                ),
                dbc.Col(
                    dcc.Upload(
                        id="sdgr_file",
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url("icons/add_file.png"),
                                    style={"height": "15px", "marginRight": "5px"},
                                ),
                                "Add file",
                            ],
                            style={"display": "flex", "alignItems": "center"},
                        ),
                        style={
                            "width": "100%",
                            "minHeight": "30px",
                            "borderWidth": "1px",
                            "borderStyle": "solid",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "5px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                        },
                        multiple=True,  # Enable multiple file uploads
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
                        "Link Submissions ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="sdgr_link", placeholder="Enter Link"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Add Applicable Criteria ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Checklist(
                        id="sdgr_applycriteria", 
                        value=[],  # Initial empty value, can be pre-filled if desired
                        inline=True
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
    ],
    className="g-2",
)



# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("ADD REVISION"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="sdgr_alert", is_open=False),  # Alert for feedback
                        form,
                        html.Br(),

                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='sdgr_removerecord',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ], 
                                            style={'fontWeight':'bold'},
                                        ),
                                        width=5,
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='sdgr_removerecord_div'
                        ),

                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="sdgr_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="sdgr_cancel_button", n_clicks=0, href="/search_users"),  
                                    width="auto"
                                ),
                            ],
                            className="mb-2",
                            justify="end",
                        ),

                        

                        dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['User registered successfully.'
                                    ],id='sdgr_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/search_users', id='sdgr_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='sdgr_successmodal',
                            backdrop=True,   
                            className="modal-success"    
                        ),
                    ],
                    width=8,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(),
                    width={"size": 12, "offset": 0},
                ),
            ],
        ),
    ]
)





#select evidence name from list of revisions
@app.callback(
    Output('sdgr_evidencename', 'options'),
    Input('url', 'pathname')
)
def populate_evidence_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_revision':
        sql = """
        SELECT sdg_evidencename as label, sdgsubmission_id   as value
        FROM kmteam.SDGSubmission
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        evidence_types = df.to_dict('records')
        return evidence_types
    else:
        raise PreventUpdate
    



#Check Status dropdown
@app.callback(
    Output('sdgr_checkstatus', 'options'),
    Input('url', 'pathname')
)
def populate_sdgrstatus_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_revision':
        sql ="""
        SELECT checkstatus_name as label, checkstatus_id  as value
        FROM  kmteam.checkstatus
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        sdgrcheckstatus_types = [{'label': row['label'], 'value': row['value']} for _, row in df.iterrows()]
        return sdgrcheckstatus_types
    else:
        raise PreventUpdate




# sdg criteria checklist
@app.callback(
    Output('sdgr_applycriteria', 'options'),
    Input('url', 'pathname')
)
def populate_applysdgrcriteria_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_revision':
        sql = """
        SELECT sdgcriteria_code as label, sdgcriteria_id   as value
        FROM kmteam.SDGCriteria
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        applysdgrcriteria_types = df.to_dict('records')
        return applysdgrcriteria_types
    else:
        raise PreventUpdate


# Callback to handle enabling/disabling file and link submissions based on submission_type
@app.callback(
    [Output('sdgr_file', 'disabled'),
     Output('sdgr_link', 'disabled')],
    [Input('sdgrsubmission_type', 'value')]
)
def toggle_submissions(sdgrsubmission_type):
    if sdgrsubmission_type == 'file':
        return False, True  
    elif sdgrsubmission_type == 'link':
        return True, False   
    elif sdgrsubmission_type == 'both':
        return False, False   
    return True, True  
 
@app.callback(
    Output("sdgr_file_output", "children"),
    [Input("sdgr_file", "filename")],  
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"






