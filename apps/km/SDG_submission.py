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

# Using the corrected path
UPLOAD_DIRECTORY = r"C:\Users\Naomi A. Takagaki\OneDrive\Documents\TINQAD\assets\database"

# Ensure the directory exists or create it
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)




ranking_options = [
    {"label": "THE Impact Rankings", "value": 1},
    {"label": "QS World University Rankings", "value": 2},
    {"label": "Academic Ranking of World Universities", "value": 3},
    # Add more options as needed
]
  
# Form layout with improvements
form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    ["Ranking Body", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Select(
                        id='sdg_rankingbody', 
                        options=ranking_options,
                        value=1,
                    ),
                    width=5,
                ), 
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Evidence Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_evidencename",  placeholder="Enter Evidence Name"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Description ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Textarea(id="sdg_description",placeholder="Enter Description"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Please indicate ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='selection_type',
                        options=[
                            {"label": "Office", "value": "office"},
                            {"label": "Department", "value": "department"},
                        ],
                        placeholder="Select Office or Department"
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
                        "Office ",
                         
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_office_id', 
                        disabled=True
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
                        "Department ",
                         
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_deg_unit_id',
                        disabled=True 
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
                        "Accomplished By ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_accomplishedby", placeholder="Name Surname" ),  # Pre-filled as per image
                    width=4,
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
                        id='sdg_datesubmitted',
                        date=str(pd.to_datetime("today").date()),  # Today's date by default 
                        clearable=True,
                    ),
                    width=4,
                ),
            ],
            className="mb-2"
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
                        id='sdg_checkstatus',  
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
                        id='submission_type',
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
                        id="sdg_file",
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
            [dbc.Col(id="file_name_output",style={"color": "#F8B237"}, width=8)],  # Output area for uploaded file names
            className="mt-2",
        ),
        
        html.Br(), 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ", 
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="sdg_link", placeholder="Enter Link"),
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
                        id="sdg_applycriteria", 
                        value=[],  # Initial empty value, can be pre-filled if desired
                        inline=True
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        # Cancel and Save Buttons
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/SDGimpact_rankings"),  
                    width="auto"
                ),
            ],
            className="mb-2",
            justify="end",
        ),

        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4("Criteria added."),
                ),
                dbc.ModalFooter(
                    dbc.Button("Proceed", id="proceed_button", className="ml-auto"),
                ),
            ],
            centered=True,
            id="sdgsubmission_successmodal",
            backdrop=True,
            className="modal-success",
        ),
    ],
    className="g-2",
)

# office dropdown
@app.callback(
    Output('sdg_office_id', 'options'),
    Input('url', 'pathname')
)
def populate_office_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT office_name as label, office_id as value
        FROM maindashboard.offices
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        office_types = df.to_dict('records')
        return office_types
    else:
        raise PreventUpdate

# depts dropdown
@app.callback(
    Output('sdg_deg_unit_id', 'options'),
    Input('url', 'pathname')
)
def populate_depts_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT deg_unit_name as label, deg_unit_id as value
        FROM  public.deg_unit
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        depts_types = df.to_dict('records')
        return depts_types
    else:
        raise PreventUpdate







#Check Status dropdown
@app.callback(
    Output('sdg_checkstatus', 'options'),
    Input('url', 'pathname')
)
def populate_status_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql ="""
        SELECT checkstatus_name as label, checkstatus_id  as value
        FROM  kmteam.checkstatus
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        checkstatus_types = [{'label': row['label'], 'value': row['value']} for _, row in df.iterrows()]
        return checkstatus_types
    else:
        raise PreventUpdate







# sdg criteria checklist
@app.callback(
    Output('sdg_applycriteria', 'options'),
    Input('url', 'pathname')
)
def populate_applycriteria_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT sdgcriteria_code as label, sdgcriteria_id   as value
        FROM kmteam.SDGCriteria
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        applycriteria_types = df.to_dict('records')
        return applycriteria_types
    else:
        raise PreventUpdate

# Callback to handle enabling/disabling office and department dropdowns based on selection_type
@app.callback(
    [Output('sdg_office_id', 'disabled'),
     Output('sdg_deg_unit_id', 'disabled')],
    [Input('selection_type', 'value')]
)
def toggle_dropdowns(selection_type):
    if selection_type == 'office':
        return False, True  # Enable Office, Disable Department
    elif selection_type == 'department':
        return True, False  # Disable Office, Enable Department
    return True, True  # Disable both by default

# Callback to handle enabling/disabling file and link submissions based on submission_type
@app.callback(
    [Output('sdg_file', 'disabled'),
     Output('sdg_link', 'disabled')],
    [Input('submission_type', 'value')]
)
def toggle_submissions(submission_type):
    if submission_type == 'file':
        return False, True  # Enable File, Disable Link
    elif submission_type == 'link':
        return True, False  # Disable File, Enable Link
    elif submission_type == 'both':
        return False, False  # Enable both
    return True, True  # Disable both by default

# Callback to display the names of the uploaded files
@app.callback(
    Output("file_name_output", "children"),
    [Input("sdg_file", "filename")],  # Use filename to get uploaded file names
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list):
        # If multiple files are uploaded, join their names
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"

    # For single file upload, return the file name directly
    return f"Uploaded file: {filenames}"


# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("ADD NEW SDG SUBMISSION"),
                        html.Hr(),
                        html.Br(),
                        dbc.Alert(id="sdgsubmission_alert", is_open=False),  # Alert for feedback
                        form,
                        
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





@app.callback(
    [
        Output('sdgsubmission_alert', 'color'),
        Output('sdgsubmission_alert', 'children'),
        Output('sdgsubmission_alert', 'is_open'),
        Output('sdgsubmission_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('sdg_rankingbody', 'value'),
        State('sdg_evidencename', 'value'),
        State('sdg_description', 'value'),
        State('sdg_office_id', 'value'),
        State('sdg_deg_unit_id', 'value'),
        State('sdg_accomplishedby', 'value'),
        State('sdg_datesubmitted', 'value'), 
        State('sdg_checkstatus', 'value'), 
        State('sdg_file', 'contents'),
        State('sdg_file', 'filename'),  
        State('sdg_link', 'value'), 
        State('sdg_applycriteria', 'value'), 
    ]
)
def record_SDGsubmission(submitbtn, sdg_rankingbody, sdg_evidencename, sdg_description,
                        sdg_office_id, sdg_deg_unit_id, sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus,
                        sdg_file_contents, sdg_file_names, sdg_link, sdg_applycriteria
                            ):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

 
    if not sdg_rankingbody:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Ranking Body.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not sdg_evidencename:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add an Evidence Name.'
        return [alert_color, alert_text, alert_open, modal_open]
 

    if not (sdg_office_id or sdg_deg_unit_id):
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Please provide an Office ID or a Degree Unit ID.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not sdg_accomplishedby:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Accomplished by.'
        return [alert_color, alert_text, alert_open, modal_open]
    

    if sdg_file_contents is None or sdg_file_names is None:
        sdg_file_contents = ["1"]
        sdg_file_names = ["1"]

    # Process the files if there are any
    file_data = []
    if sdg_file_contents and sdg_file_names:
        for content, filename in zip(sdg_file_contents, sdg_file_names):
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
                return set_alert(f"Error processing uploaded files: {str(e)}", 'danger')

    try:
        sql = """
            INSERT INTO kmteam.SDGSubmission (
                sdg_rankingbody, sdg_evidencename,
                sdg_description, sdg_office_id, sdg_deg_unit_id,
                sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus,
                sdg_link, sdg_applycriteria,
                sdg_file_path, sdg_file_name, sdg_file_type, sdg_file_size
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        values = (
            sdg_rankingbody, sdg_evidencename, sdg_description, sdg_office_id,
            sdg_deg_unit_id, sdg_accomplishedby, sdg_datesubmitted, sdg_checkstatus, sdg_link,
            json.dumps(sdg_applycriteria) if sdg_applycriteria else None,
            file_data[0]["path"] if file_data else None,
            file_data[0]["name"] if file_data else None,
            file_data[0]["type"] if file_data else None,
            file_data[0]["size"] if file_data else None,
        )

        db.modifydatabase(sql, values)
        modal_open = True

    except Exception as e:
        return set_alert("An error occurred while saving the data: " + str(e), 'danger')

    return [alert_color, alert_text, alert_open, modal_open]


# Helper function for setting alerts
def set_alert(message, color):
    return [color, message, True, False]


 