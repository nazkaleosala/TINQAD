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
                        "Surname ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_sname", type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_fname",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Middle Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_mname",type="text"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "UP Mail ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_upmail",type="text"),
                    width=6,
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
                        id='unithead_cluster_id',
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
                        id='unithead_college_id',
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
                        "Department ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_deg_unit_id',
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
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='unithead_fac_posn_name',
                        placeholder="Select Position",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(id="unithead_fac_posn_number", type="text", placeholder="#"),
                    width=1,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Official Designation",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="unithead_desig",type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ), 
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Start of Appointment",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='unithead_appointment_start'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "End of Appointment",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='unithead_appointment_end'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
         
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/acad_heads_directory"),  
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
                    html.H4('Academic head profile added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='unithead_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
         
    ]
)







# CU dropdown
@app.callback(
    Output('unithead_fac_posn_name', 'options'),
    Input('url', 'pathname')
)
def populate_fac_posn_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/acadheadsdirectory/acadheads_profile':
        sql = """
        SELECT fac_posn_name as label, fac_posn_name  as value
        FROM public.fac_posns
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        unithead_fac_posn_types = df.to_dict('records')
        return unithead_fac_posn_types
    else:
        raise PreventUpdate








# Cluster dropdown
@app.callback(
    Output('unithead_cluster_id', 'options'),
    Input('url', 'pathname')
)
def populate_cluster_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/acadheadsdirectory/acadheads_profile':
        sql = """
        SELECT cluster_name as label, cluster_id  as value
        FROM public.clusters
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        unithead_cluster_types = df.to_dict('records')
        return unithead_cluster_types
    else:
        raise PreventUpdate

# College dropdown
@app.callback(
    Output('unithead_college_id', 'options'),
    Input('unithead_cluster_id', 'value')
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
        
        unithead_college_options = df.to_dict('records')
        return unithead_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

# Degree Unit dropdown
@app.callback(
    Output('unithead_deg_unit_id', 'options'),
    Input('unithead_college_id', 'value')
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
        
        unithead_dgu_options = df.to_dict('records')
        return unithead_dgu_options
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
                        html.H1("ADD NEW ACADEMIC HEAD PROFILE"),
                        html.Hr(),
                        dbc.Alert(id='unithead_alert', is_open=False), # For feedback purpose
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
        Output('unithead_alert', 'color'),
        Output('unithead_alert', 'children'),
        Output('unithead_alert', 'is_open'),
        Output('unithead_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('unithead_fname', 'value'),
        State('unithead_mname', 'value'),
        State('unithead_sname', 'value'),
        State('unithead_upmail', 'value'),
        State('unithead_fac_posn_name', 'value'),
        State('unithead_fac_posn_number', 'value'),
        State('unithead_desig', 'value'),    
        State('unithead_appointment_start', 'value'),
        State('unithead_appointment_end', 'value'),  
        State('unithead_cluster_id', 'value'),      
        State('unithead_college_id', 'value'), 
        State('unithead_deg_unit_id', 'value')        
    ]
)
 
def record_acadhead_profile(submitbtn, unithead_fname, unithead_mname, 
                            unithead_sname, unithead_upmail,
                            unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                            unithead_appointment_start, unithead_appointment_end, 
                            unithead_cluster_id, unithead_college_id, unithead_deg_unit_id):
    if not submitbtn:
        raise PreventUpdate

    alert_open = True  # Set alert_open to True by default
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not unithead_sname:
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Surname.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
    
    if not unithead_fname:
        alert_color_fname = 'danger'
        alert_text_fname = 'Check your inputs. Please add a First Name.'
        return [alert_color_fname, alert_text_fname, alert_open, modal_open]

    if not unithead_mname:
        alert_color_mname = 'danger'
        alert_text_mname = 'Check your inputs. Please add a Middle Name.'
        return [alert_color_mname, alert_text_mname, alert_open, modal_open]

    

    if not unithead_upmail:
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a UP Mail.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not unithead_cluster_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a Cluster.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not unithead_college_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a College.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not unithead_deg_unit_id :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please select a Department.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not unithead_fac_posn_name :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a Faculty Position.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    if not unithead_desig  :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add an Official Designation.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
     
    if not unithead_appointment_start  :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a start date.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
    
    if not unithead_appointment_end  :
        alert_color_upmail = 'danger'
        alert_text_upmail = 'Check your inputs. Please add a end date.'
        return [alert_color_upmail, alert_text_upmail, alert_open, modal_open]
    
     
    try:
        sql = """
            INSERT INTO iqateam.acad_unitheads (
                unithead_fname, unithead_mname, unithead_sname, unithead_upmail,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                unithead_appointment_start, unithead_appointment_end, unithead_cluster_id, unithead_college_id, unithead_deg_unit_id
            )
            VALUES (%s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s)
        """
        values = (unithead_fname, unithead_mname, 
                unithead_sname, unithead_upmail,
                unithead_fac_posn_name, unithead_fac_posn_number, unithead_desig, 
                
                unithead_appointment_start, unithead_appointment_end, 
                unithead_cluster_id, unithead_college_id, unithead_deg_unit_id)

        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'

    return [alert_color, alert_text, alert_open, modal_open]

  
