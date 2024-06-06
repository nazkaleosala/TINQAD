import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


from urllib.parse import urlparse, parse_qs


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
                    dbc.Input(type="text", 
                              id='complete_name', 
                              placeholder="Last Name, First Name, Middle Initial",
                              disabled=False
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
                        "Position ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='fac_posn_name',
                        options=[],
                        placeholder="Select position",
                        disabled=False
                        
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(id="fac_posn_number", type="text", 
                              placeholder="Number",
                              disabled=False),
                    width=2,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Add new Faculty Position", 
                    ],
                    width=4
                ),
                 
                dbc.Col(
                    dbc.Input(id="add_training_fac_posn", type="text", placeholder="Faculty position not in list?"),
                    width=6,
                ),
                dbc.Col(
                    dbc.Button("➕", color="primary",  id="add_training_save_button", n_clicks=0),
                        width="auto"
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
                       disabled=False
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
                       disabled=False
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
                        disabled=False
                    ),
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
                        id='qa_training_id',
                        options=[],
                        placeholder="Select QA Training"
                    ),
                    width=6,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other QA Training Attended:", 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='qa_training_other'),
                    width=6,
                ),
            ],
            className="mb-1",
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
                       id='departure_date',
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
                       id='return_date',
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
                    dbc.Input(type="text", id='venue', placeholder="Venue Name, City, Country"),
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
                        id='parti_attendance_cert',
                        children=html.Div(
                            [
                            html.Img(src=app.get_asset_url('icons/add_file.png'), style={'height': '15px', 'marginRight': '5px'}),
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
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="parti_attendance_cert_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
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
                        id='official_receipt',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/add_file.png'),
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
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
            dbc.Col(id="official_receipt_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
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
                        id='official_travel_report',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/add_file.png'),
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
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
            dbc.Col(id="official_travel_report_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other Receipts "
                    ],
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='other_receipts',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/add_file.png'),
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
            className="mb-1",
        ),
        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="other_receipts_output",style={"color": "#F8B237"}, width="auto")],  # Output area for uploaded file names
            className="mt-0",
        ),

        dbc.Row(
            [
                dbc.Label(
                    "Receiving Copy (Optional) ",
                    width=6
                ),
                dbc.Col(
                    dcc.Upload(
                        id='receiving_copy',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/add_file.png'),
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
            className="mb-1",
        ),

        dbc.Row(
            [dbc.Label("",width=6),
             dbc.Col(id="receiving_copy_output",style={"color": "#F8B237"}, width="auto")],  
            className="mt-0",
        ),

        

   ],
   className="g-2",
)






# Callback to display the names of the uploaded files
@app.callback(
    Output("parti_attendance_cert_output", "children"),
    [Input("parti_attendance_cert", "filename")],  # Use filename to get uploaded file names
)
def display_partiattendence_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"


 
@app.callback(
    Output("official_receipt_output", "children"),
    [Input("official_receipt", "filename")],  # Use filename to get uploaded file names
)
def display_receipt_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"

 
@app.callback(
    Output("official_travel_report_output", "children"),
    [Input("official_travel_report", "filename")],  # Use filename to get uploaded file names
)
def display_travelreport_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"

 

 
@app.callback(
    Output("other_receipts_output", "children"),
    [Input("other_receipts", "filename")],  # Use filename to get uploaded file names
)
def display_otherreport_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"

 
@app.callback(
    Output("receiving_copy_output", "children"),
    [Input("receiving_copy", "filename")],  # Use filename to get uploaded file names
)
def display_receivingcopy_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"

 











#faculty positions dropdown
@app.callback(
    Output('fac_posn_name', 'options'),
    Input('url', 'pathname')
)

def populate_facultypositions_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_documents':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        fac_posns_types = df.to_dict('records')
        return fac_posns_types
    else:
        raise PreventUpdate







#college dropdown
@app.callback(
    Output('college_id', 'options'),
    Input('cluster_id', 'value')
)
def populate_college_dropdown(selected_cluster):
    if selected_cluster is None:
        return []  # Return empty options if no main expense is selected
    
    try:
        # Query to fetch sub-expenses based on the selected main expense
        sql = """
        SELECT college_name as label,  college_id  as value
        FROM public.college
        WHERE cluster_id = %s
        """
        values = [selected_cluster]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        college_options = df.to_dict('records')
        return college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 


# dgu dropdown
@app.callback(
    Output('deg_unit_id', 'options'), 
    Input('college_id', 'value')
)
def populate_dgu_dropdown(selected_college):
    if selected_college is None:
        return []  # Return empty options if no college is selected
    
    try:
        # Query to fetch degree units based on the selected college
        sql = """
        SELECT deg_unit_name as label,  deg_unit_id  as value
        FROM public.deg_unit
        WHERE college_id = %s
        """
        values = [selected_college]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        dgu_options = df.to_dict('records')
        return dgu_options
    except Exception as e:
        # Log the error or handle it appropriately
        return []
    




#qa training dropdown
@app.callback(
    Output('qa_training_id', 'options'),
    Input('url', 'pathname')
)
def populate_qatrainings_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training_documents':
        sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM qaofficers.training_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qa_training_options = df.to_dict('records')
        return qa_training_options
    else:
        raise PreventUpdate







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
                    html.Div(  
                            [
                                dcc.Store(id='trainingdocuments_toload', storage_type='memory', data=0),
                            ]
                        ),

                    html.H1("ADD TRAINING DOCUMENTS DETAILS"),
                    html.Hr(),
                    dbc.Alert(id='trainingdocuments_alert', is_open=False), # For feedback purpose
                    form, 
                    
                    html.Br(),   
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Label("Wish to delete?", width=4),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='trainingdocuments_removerecord',
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
                        id='trainingdocuments_removerecord_div'
                    ),

                    html.Br(),
                    dbc.Row(
                        [ 
                            
                            dbc.Col(
                                dbc.Button("Save", color="primary",  id="trainingdocuments_save_button", n_clicks=0),
                                width="auto"
                            ),
                            dbc.Col(
                                dbc.Button("Cancel", color="warning", id="trainingdocuments_cancel_button", n_clicks=0, href="/training_documents"),  
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
                                ],id='trainingdocuments_feedback_message'
                            ),

                            dbc.ModalFooter(
                                dbc.Button(
                                    "Proceed", href='/training_documents', id='trainingdocuments_btn_modal'
                                    ), 
                                ),
                            
                            
                        ],
                        centered=True,
                        id='trainingdocuments_successmodal',
                        backdrop=True,  
                        className="modal-success"   
                    ),
                    
                    dbc.Modal(
                            [
                                dbc.ModalHeader(className="bg-success"),
                                dbc.ModalBody(
                                    ['Faculty Position added successfully.'
                                    ],id='add_training_feedback_message'
                                ), 
                                
                            ],
                            centered=True,
                            id='add_training_successmodal',
                            backdrop=True,   
                            className="modal-success"    
                    ),
                     
                ],
                width=8, style={'marginLeft': '15px'}
                
                )
            ]
        ),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        ),
        
    ]
)







@app.callback(
    [
        Output('cluster_id', 'options'),
        Output('trainingdocuments_toload', 'data'),
        Output('trainingdocuments_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')  
    ]
)


def trainingdocuments_loaddropdown(pathname, search):
    if pathname == '/training_documents':
        sql = """
            SELECT cluster_name as label, cluster_id  as value
            FROM public.clusters
            
            WHERE cluster_del_ind = False
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        cluster_options = df.to_dict('records')
        
        
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        removediv_style = {'display': 'none'} if not to_load else None
    
    else:
        raise PreventUpdate
    return [cluster_options, to_load, removediv_style]




@app.callback(
    [
        Output('trainingdocuments_alert', 'color'),
        Output('trainingdocuments_alert', 'children'),
        Output('trainingdocuments_alert', 'is_open'),

        Output('trainingdocuments_successmodal', 'is_open'),
        Output('trainingdocuments_feedback_message', 'children'),
        Output('trainingdocuments_btn_modal', 'href'),
    ],
    [
        Input('trainingdocuments_save_button', 'n_clicks'),
        Input('trainingdocuments_btn_modal', 'n_clicks'),
        Input('trainingdocuments_removerecord', 'value'),
    ],
    [
        State('complete_name', 'value'),
        State('fac_posn_name', 'value'),
        State('fac_posn_number', 'value'),
        State('cluster_id', 'value'),
        State('college_id', 'value'),
        State('deg_unit_id', 'value'),
        State('qa_training_id', 'value'),
        State('qa_training_other', 'value'),
        State('departure_date', 'date'),
        State('return_date', 'date'),
        State('venue', 'value'),
        State('parti_attendance_cert', 'filename'),
        State('official_receipt', 'filename'),
        State('official_travel_report', 'filename'),
        State('other_receipts', 'filename'),
        State('receiving_copy', 'filename'),
        State('url', 'search'),
    ]
)


def record_training_documents(submitbtn, closebtn, removerecord,
                              complete_name, fac_posn_name, fac_posn_number,
                              cluster_id, college_id, deg_unit_id, qa_training_id,
                              qa_training_other,
                              departure_date, return_date, venue, parti_attendance_cert,
                              official_receipt, official_travel_report, other_receipts, receiving_copy,
                              search):
    
        ctx = dash.callback_context
    
        if not ctx.triggered:
            raise PreventUpdate
        
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'trainingdocuments_save_button' and submitbtn:
    
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
     
             
            if not complete_name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Name.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]

            if not fac_posn_name:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Position Type.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not cluster_id:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Cluster type.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not college_id:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a College.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not deg_unit_id:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Department.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not qa_training_id:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a QA training.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not departure_date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Departure date.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not return_date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Return date.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            if not venue:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a Venue.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            

            # Set default values for non-nullable fields
            if not parti_attendance_cert:
                parti_attendance_cert = b''  # Empty bytes
            if not official_receipt:
                official_receipt = b''  
            if not official_travel_report:
                official_travel_report = b'' 
            if not other_receipts:
                other_receipts = b''
     
            parsed = urlparse(search)
            create_mode = parse_qs(parsed.query)['mode'][0]
                    
            if create_mode == 'add':
                        
                    sql = """
                        INSERT INTO adminteam.training_documents (
                            complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id,
                            qa_training_id, qa_training_other, departure_date, return_date, venue, parti_attendance_cert, 
                            official_receipt, official_travel_report, other_receipts, receiving_copy, train_docs_del_ind 
                        )
                        VALUES (
                                %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s
                            )
                        """
    
                    values = (complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id, 
                        qa_training_id, qa_training_other, departure_date, return_date, venue, parti_attendance_cert, 
                        official_receipt, official_travel_report, other_receipts, receiving_copy, False
                    )
            
                    db.modifydatabase(sql, values) 
                    modal_open = True
                    feedbackmessage = html.H5("Training document registered successfully.")
                    okay_href = "/training_record" 
                        
            elif create_mode == 'edit':
                parsed = urlparse(search)
                trainingdocumentsid = parse_qs(parsed.query)['id'][0]
                
                sqlcode = """
                    UPDATE adminteam.training_documents
                    SET
                        complete_name = %s,
                        fac_posn_name = %s,
                        fac_posn_number = %s,
                        qa_training_id = %s, 
                        qa_training_other = %s, 
                        departure_date = %s,
                        return_date = %s,
                        venue = %s,
                        train_docs_del_ind = %s 
                    WHERE 
                        training_documents_id  = %s
                """
                to_delete = bool(removerecord) 
                        
                values = [complete_name, fac_posn_name, fac_posn_number, qa_training_id, qa_training_other, departure_date, return_date, venue, to_delete, trainingdocumentsid]
                db.modifydatabase(sqlcode, values)
                    
                feedbackmessage = html.H5("Document has been updated." )
                okay_href = "/training_record"
                modal_open = True

            else:
                raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        else:
            raise PreventUpdate
        
 




@app.callback(
    [
        Output('complete_name', 'value'),
        Output('fac_posn_name', 'value'),
        Output('fac_posn_number', 'value'),
        Output('cluster_id', 'value'),
        Output('college_id', 'value'),
        Output('deg_unit_id', 'value'),
        Output('qa_training_id', 'value'),
        Output('qa_training_other', 'value'),
        Output('departure_date', 'date'),
        Output('return_date', 'date'),
        Output('venue', 'value'),
        Output('parti_attendance_cert', 'filename'),
        Output('official_receipt', 'filename'),
        Output('official_travel_report', 'filename'),
        Output('other_receipts', 'filename'),
        Output('receiving_copy', 'filename'),
    ],
    [  
        Input('trainingdocuments_toload', 'modified_timestamp')
    ],
    [
        State('trainingdocuments_toload', 'data'),
        State('url', 'search')
    ]
)
def trainingdocuments_loadprofile(timestamp, toload, search):
    if toload:
        parsed = urlparse(search)
        trainingdocumentsid = parse_qs(parsed.query)['id'][0]
 
        sql = """
            SELECT 
                complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id,
                qa_training_id, qa_training_other, departure_date, return_date, venue, parti_attendance_cert, 
                official_receipt, official_travel_report, other_receipts, receiving_copy
            FROM adminteam.training_documents
            WHERE training_documents_id = %s
        """
        values = [trainingdocumentsid]

        cols = [
            'complete_name', 'fac_posn_name', 'fac_posn_number', 'cluster_id', 'college_id', 'deg_unit_id',
            'qa_training_id', "qa_training_other" , 'departure_date', 'return_date', 'venue', 'parti_attendance_cert', 
            'official_receipt', 'official_travel_report', 'other_receipts', 'receiving_copy' 
        ]

         
        df = db.querydatafromdatabase(sql, values, cols)

        
        complete_name = df['complete_name'][0]
        fac_posn_name = df['fac_posn_name'][0]
        fac_posn_number = df['fac_posn_number'][0]
        cluster_id = int(df['cluster_id'][0])
        college_id = int(df['college_id'][0])
        deg_unit_id = int(df['deg_unit_id'][0])
        qa_training_id = int(df['qa_training_id'][0])
        qa_training_other = df['qa_training_other'][0]
        departure_date = df['departure_date'][0]
        return_date = df['return_date'][0]
        venue = df['venue'][0]
        parti_attendance_cert = df['parti_attendance_cert'][0]  
        official_receipt = df['official_receipt'][0]
        official_travel_report = df['official_travel_report'][0]
        other_receipts = df['other_receipts'][0]
        receiving_copy = df['receiving_copy'][0] 
        
        return [complete_name, fac_posn_name, fac_posn_number, cluster_id, college_id, deg_unit_id, 
                            qa_training_id, qa_training_other , departure_date, return_date, venue, parti_attendance_cert, 
                            official_receipt, official_travel_report, other_receipts, receiving_copy]
    
    else:
        raise PreventUpdate




@app.callback(
    [  
        Output('complete_name', 'disabled'),
        Output('fac_posn_name', 'disabled'),
        Output('fac_posn_number', 'disabled'),
        Output('cluster_id', 'disabled'),
        Output('college_id', 'disabled'),
        Output('deg_unit_id', 'disabled'), 
        Output('add_training_fac_posn', 'disabled'), 
    ],
    [Input('url', 'search')]
)
def training_inputs_disabled(search):
    if search:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]
        if create_mode == 'edit':
            return [True] * 7
    return [False] * 7








@app.callback(
    [Output('add_training_successmodal', 'is_open')],
    [Input('add_training_save_button', 'n_clicks')],
    [State('add_training_fac_posn', 'value'), 
     State('url', 'search')]
)
 
def register_training_unithead(submitbtn, add_training_fac_posn, search):
    if submitbtn:
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query).get('mode', [None])[0]

        if create_mode == 'add' and add_training_fac_posn:
            sql = """
                INSERT INTO public.fac_posns (fac_posn_name)
                VALUES (%s)
            """
            values = (add_training_fac_posn,)
            db.modifydatabase(sql, values)
            return [True]  
    raise PreventUpdate
