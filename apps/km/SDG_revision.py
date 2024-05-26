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
import json

import base64
import os
from urllib.parse import urlparse, parse_qs

# Using the corrected path
UPLOAD_DIRECTORY = r"C:\Users\Naomi A. Takagaki\OneDrive\Documents\TINQAD\assets\database"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)



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
                dbc.Label("Department", width=4),
                dbc.Col(
                    html.P(id='sdgr_deg_unit_id'),
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
                    width=5,
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
                    ),
                    width=4,
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
            [dbc.Label("",width=6),
             dbc.Col(id="sdgr_file_output",style={"color": "#F8B237"}, width=6)],  # Output area for uploaded file names
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
                        html.Div(  
                            [
                                dcc.Store(id='sdgr_toload', storage_type='memory', data=0),
                            ]
                        ),
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
        SELECT sdg_evidencename as label, sdgsubmission_id as value
        FROM kmteam.SDGSubmission
        WHERE sdg_checkstatus = '3' AND sdg_del_ind = FALSE
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        evidence_types = df.to_dict('records')
        return evidence_types
    else:
        raise PreventUpdate
    




#ranking body appear
@app.callback(
    Output('sdgr_rankingbody', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_rankingbody_text(selected_evidencename_rb):
    if selected_evidencename_rb is None:
        return ""
    else:
        try: 
            rankingbody = db.get_rankingbody(selected_evidencename_rb)
            if rankingbody:
                return rankingbody
            else:
                return "No ranking body found for this evidence name"
        except Exception as e:
            return "An error occurred while fetching the rankingbody: {}".format(str(e))




#description appear
@app.callback(
    Output('sdgr_description', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_description_text(selected_evidencename_descript):
    if selected_evidencename_descript is None:
        return ""
    else:
        try: 
            description = db.get_sdgrdescription (selected_evidencename_descript)
            if description:
                return description
            else:
                return "No description found for this evidence name"
        except Exception as e:
            return "An error occurred while fetching the description: {}".format(str(e))




#office appear
@app.callback(
    Output('sdgr_office_id', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_office_text(selected_evidencename_office):
    if selected_evidencename_office is None:
        return ""
    else:
        try: 
            office = db.get_sdgroffice (selected_evidencename_office)
            if office:
                return office
            else:
                return ""
        except Exception as e:
            return "An error occurred while fetching the office: {}".format(str(e))


#department appear
@app.callback(
    Output('sdgr_deg_unit_id', 'children'),
    [Input('sdgr_evidencename', 'value')]
)

def update_department_text(selected_evidencename_department):
    if selected_evidencename_department is None:
        return ""
    else:
        try: 
            department = db.get_sdgrdepartment (selected_evidencename_department)
            if department:
                return department
            else:
                return ""
        except Exception as e:
            return "An error occurred while fetching the department: {}".format(str(e))






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







@app.callback(
    [
        Output('sdgr_alert', 'color'),
        Output('sdgr_alert', 'children'),
        Output('sdgr_alert', 'is_open'),
        Output('sdgr_successmodal', 'is_open'),
        Output('sdgr_feedback_message', 'children'),
        Output('sdgr_btn_modal', 'href')
    ],
    [
        Input('sdgr_save_button', 'n_clicks'),
        Input('sdgr_btn_modal', 'n_clicks'),
        Input('sdgr_removerecord', 'value')
    ],
    [
        State('sdgr_rankingbody', 'value'),
        State('sdgr_evidencename', 'value'),
        State('sdgr_description', 'value'),
        State('sdgr_office_id', 'value'),
        State('sdgr_deg_unit_id', 'value'),
        State('sdgr_accomplishedby', 'value'),
        State('sdgr_datesubmitted', 'value'), 
        State('sdgr_checkstatus', 'value'), 
        State('sdgr_file', 'contents'),
        State('sdgr_file', 'filename'),  
        State('sdgr_link', 'value'), 
        State('sdgr_applycriteria', 'value'), 
        State('url', 'search')
    ]
)
def record_SDGrevision (submitbtn, closebtn, removerecord,
                         sdgr_rankingbody, sdgr_evidencename, sdgr_description,
                         sdgr_office_id, sdgr_deg_unit_id, sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus,
                         sdgr_file_contents, sdgr_file_names, sdgr_link, sdgr_applycriteria,
                         search):
    
    ctx = dash.callback_context 

    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'sdgr_save_button' or not submitbtn:
        raise PreventUpdate

    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
    feedbackmessage = None
    okay_href = None

    parsed = urlparse(search)
    create_mode = parse_qs(parsed.query).get('mode', [None])[0]

    if create_mode == 'add':
        # Validation logic only for "add" mode
        if not sdgr_rankingbody:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please add a Ranking Body.'
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        if not sdgr_accomplishedby:
            alert_open = True
            alert_color = 'danger'
            alert_text = 'Check your inputs. Please add an Accomplished by.'
            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        if sdgr_file_contents is None or sdgr_file_names is None:
            sdgr_file_contents = ["1"]
            sdgr_file_names = ["1"]

        # Process the files if there are any
        file_data = []
        if sdgr_file_contents and sdgr_file_names:
            for content, filename in zip(sdgr_file_contents, sdgr_file_names):
                if content == "1" and filename == "1":
                    continue  # Skip default "1" value
                try:
                    # Decode and save the file
                    content_type, content_string = content.split(',')
                    decoded_content = base64.b64decode(content_string)

                    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
                    with open(file_path, 'wb') as f:
                        f.write(decoded_content)

                    file_info = {
                        "path": file_path,
                        "name": filename,
                        "type": content_type,
                        "size": len(decoded_content),
                    }
                    file_data.append(file_info)

                except Exception as e:
                    alert_open = True
                    alert_color = 'danger'
                    alert_text = f'Error processing file: {e}'
                    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        sql = """
            INSERT INTO kmteam.SDGRevision (
                sdgr_rankingbody, sdgr_evidencename,
                sdgr_description, sdgr_office_id, sdgr_deg_unit_id,
                sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus,
                sdgr_link, sdgr_applycriteria,
                sdgr_file_path, sdgr_file_name, sdgr_file_type, sdgr_file_size
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        values = (
            sdgr_rankingbody, sdgr_evidencename, sdgr_description, sdgr_office_id,
            sdgr_deg_unit_id, sdgr_accomplishedby, sdgr_datesubmitted, sdgr_checkstatus, sdgr_link,
            json.dumps(sdgr_applycriteria) if sdgr_applycriteria else None,
            file_data[0]["path"] if file_data else None,
            file_data[0]["name"] if file_data else None,
            file_data[0]["type"] if file_data else None,
            file_data[0]["size"] if file_data else None,
        )

        db.modifydatabase(sql, values)
        modal_open = True
        feedbackmessage = html.H5("New evidence submitted successfully.")
        okay_href = "/SDGimpact_rankings"

    elif create_mode == 'edit':
        # Update existing user record
        sdgrevisionid = parse_qs(parsed.query).get('id', [None])[0]
        
        if sdgrevisionid is None:
            raise PreventUpdate
        
        sqlcode = """
            UPDATE kmteam.SDGRevision
            SET
                sdgr_checkstatus = %s,
                sdgr_del_ind = %s

            WHERE 
                sdgrevision_id = %s
        """
        to_delete = bool(removerecord) 

        values = [sdgr_checkstatus, to_delete, sdgrevisionid]
        db.modifydatabase(sqlcode, values)

        feedbackmessage = html.H5("Status has been updated.")
        okay_href = "/SDGimpact_rankings"
        modal_open = True

    else:
        raise PreventUpdate

    return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
