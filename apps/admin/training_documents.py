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
                dbc.Label(
                    [
                        "Complete Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='complete_name', placeholder="Last Name, First Name, Middle Initial"),
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
                    width=8,
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
                        id='official_receipt',
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
                        id='official_travel_report',
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
                        id='other_receipts',
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
                        id='receiving_copy',
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

        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Save", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
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
                    html.H4('Training document added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='trainingdocuments_successmodal',
            backdrop=True,  # Allow clicking outside to close the modal
            className="modal-success"  # You can define this class in your CSS file for additional styling
        ),






   ],
   className="g-2",
)



#faculty positions dropdown
@app.callback(
    Output('fac_posn_id', 'options'),
    Input('url', 'pathname')
)

def populate_facultypositions_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training/training_documents':
        sql = """
        SELECT fac_posn_name as label, fac_posn_id  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        fac_posns_types = df.to_dict('records')
        return fac_posns_types
    else:
        raise PreventUpdate





#cluster dropdown
@app.callback(
    Output('cluster_id', 'options'),
    Input('url', 'pathname')
)

def populate_cluster_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/training/training_documents':
        sql = """
        SELECT cluster_name as label, cluster_id  as value
        FROM public.clusters
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        cluster_types = df.to_dict('records')
        return cluster_types
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
    if pathname == '/training/training_documents':
        sql = """
        SELECT qa_training_name as label, qa_training_id  as value
        FROM public.qa_training
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
                    html.H1("ADD TRAINING DOCUMENTS DETAILS"),
                    html.Hr(),
                    dbc.Alert(id='trainingdocuments_alert', is_open=False), # For feedback purpose
                    form, 
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
        Output('trainingdocuments_alert', 'color'),
        Output('trainingdocuments_alert', 'children'),
        Output('trainingdocuments_alert', 'is_open'),
        Output('trainingdocuments_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('complete_name', 'value'),
        State('fac_posn_id', 'value'),
        State('cluster_id', 'value'),
        State('college_id', 'value'),
        State('deg_unit_id', 'value'),
        State('qa_training_id', 'value'),
        State('departure_date', 'date'),
        State('return_date', 'date'),
        State('venue', 'value'),
        State('parti_attendance_cert', 'filename'),  
        State('official_receipt', 'filename'),      
        State('official_travel_report', 'filename'), 
        State('other_receipts', 'filename'),         
        State('receiving_copy', 'filename')          
    ]
)
 


def record_training_documents (submitbtn, complete_name, fac_posn_id, 
                               cluster_id, college_id, deg_unit_id, qa_training_id, 
                               departure_date, return_date, venue, parti_attendance_cert, 
                               official_receipt, official_travel_report, other_receipts, receiving_copy):
    if not submitbtn:
        raise PreventUpdate

    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not complete_name:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Name.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not fac_posn_id:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Position Type.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not cluster_id:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Cluster type.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not college_id:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a College.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not deg_unit_id:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Department.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not qa_training_id:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a QA training.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not departure_date:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Departure date.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not return_date:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Return date.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not venue:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Venue.'
        return [alert_color, alert_text, alert_open, modal_open]
    

     # Set default values for non-nullable fields
    if not parti_attendance_cert:
        parti_attendance_cert = b''  # Empty bytes
    if not official_receipt:
        official_receipt = b''  
    if not official_travel_report:
        official_travel_report = b'' 
    if not other_receipts:
        other_receipts = b''
     
 
 

    try:
        sql = """
            INSERT INTO adminteam.training_documents (
                complete_name, fac_posn_id, cluster_id, college_id, deg_unit_id, 
                qa_training_id, departure_date, return_date, venue, parti_attendance_cert, 
                official_receipt, official_travel_report, other_receipts, receiving_copy
            )
            VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
        """
        values = (complete_name, fac_posn_id, cluster_id, college_id, deg_unit_id, 
                  qa_training_id, departure_date, return_date, venue, parti_attendance_cert, 
                  official_receipt, official_travel_report, other_receipts, receiving_copy)
        
        
        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'
        alert_open = True

    return [alert_color, alert_text, alert_open, modal_open]

