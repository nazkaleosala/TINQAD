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
                    dbc.Input(id="qaofficer_sname", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_fname",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Name", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_mname",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("UP Mail", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_upmail",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
         

        dbc.Row(
            [
                dbc.Label(
                    [
                       "Cluster",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_cluster_id',
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
                       "College",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_college_id',
                        placeholder="Select College",
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
                       "Department",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_deg_unit_id',
                        placeholder="Select Department",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                       "Faculty Rank/Position",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_fac_posn_id',
                        placeholder="Select Department",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Label("Faculty Admin Position (if any)", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_facadmin_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Admin Staff/REPS Position", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_staff_posn", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        html.Br(),
         
        html.H5("QA INFORMATION", className="form-header fw-bold"),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                       "QA Position in the CU",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='qaofficer_cuposition_id',
                        placeholder="Select Position",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label("With Basic Paper as QAO?", width=4),
                dbc.Col(
                    dbc.Select(
                        id="qaofficer_basicpaper",
                        options=[
                            {"label":"Yes","value":"Yes"},
                            {"label":"No","value":"No"}
                        ],
                        placeholder="Please select yes/no"
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Remarks", width=4),
                dbc.Col(
                    dbc.Select(
                        id="qaofficer_remarks",
                        options=[
                            {"label":"With record","value":"No record"},
                            {"label":"No record","value":"No record"},
                            {"label":"For renewal","value":"For renewal"},
                        ],
                        placeholder="Select a remark"
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("ALC", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_alc", type="number"),
                    width=3,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label("Start of Term", width=4),
                dbc.Col(
                    dbc.Input(type="date", id='qaofficer_appointment_start'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("End of Term", width=4),
                dbc.Col(
                    dbc.Input(type="date", id='qaofficer_appointment_end'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Role in the CU-Level QA Committee", width=4),
                dbc.Col(
                    dbc.Input(id="qaofficer_role", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.Br(),
         
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/QAOfficers_directory"),  
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
                    html.H4('QA Officer profile added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                       "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='qaofficer_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
         
    ]
)





# CU dropdown
@app.callback(
    Output('qaofficer_fac_posn_id', 'options'),
    Input('url', 'pathname')
)
def populate_cuposition_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/QAOfficers/qaofficers_profile':
        sql = """
        SELECT fac_posn_name as label, fac_posn_id  as value
        FROM  public.fac_posns 
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_fac_posns_types = df.to_dict('records')
        return qaofficer_fac_posns_types
    else:
        raise PreventUpdate






# CU dropdown
@app.callback(
    Output('qaofficer_cuposition_id', 'options'),
    Input('url', 'pathname')
)
def populate_cuposition_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/QAOfficers/qaofficers_profile':
        sql = """
        SELECT cuposition_name as label, cuposition_id  as value
        FROM qaofficers.cuposition
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_cuposition_types = df.to_dict('records')
        return qaofficer_cuposition_types
    else:
        raise PreventUpdate








# Cluster dropdown
@app.callback(
    Output('qaofficer_cluster_id', 'options'),
    Input('url', 'pathname')
)
def populate_cluster_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/QAOfficers/qaofficers_profile':
        sql = """
        SELECT cluster_name as label, cluster_id  as value
        FROM public.clusters
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_cluster_types = df.to_dict('records')
        return qaofficer_cluster_types
    else:
        raise PreventUpdate

# College dropdown
@app.callback(
    Output('qaofficer_college_id', 'options'),
    Input('qaofficer_cluster_id', 'value')
)
def populate_college_dropdown(selected_cluster):
    if selected_cluster is None:
        return []   
    
    try:  
        sql = """
        SELECT college_name as label,  college_id  as value
        FROM public.college
        WHERE cluster_id = %s
        """
        values = [selected_cluster]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficer_college_options = df.to_dict('records')
        return qaofficer_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

# Degree Unit dropdown
@app.callback(
    Output('qaofficer_deg_unit_id', 'options'),
    Input('qaofficer_college_id', 'value')
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
        
        qaofficer_dgu_options = df.to_dict('records')
        return qaofficer_dgu_options
    except Exception as e:
        # Log the error or handle it appropriately
        return []
    




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
                        html.H1("ADD NEW QA OFFICER PROFILE"),
                        html.Hr(),
                        dbc.Alert(id='qaofficer_alert', is_open=False), # For feedback purpose
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
 


 
@app.callback(
    [
        Output('qaofficer_alert', 'color'),
        Output('qaofficer_alert', 'children'),
        Output('qaofficer_alert', 'is_open'),
        Output('qaofficer_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('qaofficer_fname', 'value'),
        State('qaofficer_mname', 'value'),
        State('qaofficer_sname', 'value'),
        State('qaofficer_upmail', 'value'),

        State('qaofficer_fac_posn_id', 'value'),
        State('qaofficer_facadmin_posn', 'value'),
        State('qaofficer_staff_posn', 'value'),


        State('qaofficer_cuposition_id', 'value'),
        State('qaofficer_basicpaper', 'value'),
        State('qaofficer_remarks', 'value'),   
        State('qaofficer_alc', 'value'),      
        State('qaofficer_appointment_start', 'value'),
        State('qaofficer_appointment_end', 'value'),  
        State('qaofficer_cluster_id', 'value'),      
        State('qaofficer_college_id', 'value'), 
        State('qaofficer_deg_unit_id', 'value'),
        State('qaofficer_role', 'value'),

    ]
)
 
def record_qaofficer_profile(submitbtn, qaofficer_fname, qaofficer_mname, 
                            qaofficer_sname, qaofficer_upmail,
                            qaofficer_fac_posn_id, qaofficer_facadmin_posn, qaofficer_staff_posn,
                            qaofficer_cuposition_id, qaofficer_basicpaper, 
                            qaofficer_remarks, qaofficer_alc,
                            qaofficer_appointment_start, qaofficer_appointment_end, 
                            qaofficer_cluster_id, qaofficer_college_id, 
                            qaofficer_deg_unit_id, qaofficer_role):
    
    if not submitbtn:
        raise PreventUpdate

    alert_open = True  # Set alert_open to True by default
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not qaofficer_sname:
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Surname.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
    
    if not qaofficer_fname:
        alert_color_fname = 'danger'
        alert_text_fname = 'Check your inputs. Please add a First Name.'
        return [alert_color_fname, alert_text_fname, alert_open, modal_open]

    if not qaofficer_mname:
        alert_color_mname = 'danger'
        alert_text_mname = 'Check your inputs. Please add a Middle Name.'
        return [alert_color_mname, alert_text_mname, alert_open, modal_open]

    

    if not qaofficer_upmail:
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a UP Mail.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_cluster_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a Cluster.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_college_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a College.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_deg_unit_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a Department.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    

    if not qaofficer_fac_posn_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a Faculty Position.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    

    if not qaofficer_cuposition_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a CU Position.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_basicpaper :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please check if there is basic paper.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_remarks :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a remark.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not qaofficer_alc :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add an ALC.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    
    if not qaofficer_appointment_start  :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a start date.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    
    if not qaofficer_appointment_end  :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a end date.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
     
    try:
        sql = """
            INSERT INTO  qaofficers.qa_officer (
                qaofficer_fname, qaofficer_mname, qaofficer_sname, qaofficer_upmail,
                qaofficer_fac_posn_id, qaofficer_facadmin_posn, qaofficer_staff_posn,
                qaofficer_cuposition_id, qaofficer_basicpaper, qaofficer_remarks, qaofficer_alc,
                qaofficer_appointment_start, qaofficer_appointment_end, qaofficer_cluster_id, 
                qaofficer_college_id, qaofficer_deg_unit_id, qaofficer_role
            )
            VALUES (%s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s,
                    %s)
        
        """
        values = (qaofficer_fname, qaofficer_mname, 
                qaofficer_sname, qaofficer_upmail,
                qaofficer_fac_posn_id, qaofficer_facadmin_posn, qaofficer_staff_posn,
                qaofficer_cuposition_id, qaofficer_basicpaper, 
                qaofficer_remarks, qaofficer_alc,
                qaofficer_appointment_start, qaofficer_appointment_end, 
                qaofficer_cluster_id, qaofficer_college_id, qaofficer_deg_unit_id,
                qaofficer_role)

        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'

    return [alert_color, alert_text, alert_open, modal_open]

  