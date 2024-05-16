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

import psycopg2
import json
import logging


form = dbc.Form(
    [
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Select Degree Program",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_title", type="text", placeholder= "Bachelor of Science in Industrial Engineering"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Shortname",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_shortname", type="text", placeholder= "BS Industrial Engineering"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Initials",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                
                dbc.Col(
                    dbc.Input(id="pro_degree_initials", type="text", placeholder= "BS IE"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Academic Cluster ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_cluster_id', 
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
                        id='pro_college_id', 
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
                        "Institute/ Department ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_department_id', 
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
                        "Degree Count",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="number", id="pro_degree_count"),
                    width=2,
                ),
            ],
            className="mb-1",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Type",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_program_type_id', 
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
                        "Academic Calendar Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pro_calendar_type_id', 
                        options=[
                            {"label": "Semester", "value": "1"},
                            {"label": "Trimester", "value": "2"},
                            
                        ],
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
                        "Applicable Accreditation Bodies",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="pro_accreditation_body_id",
                        multi=True  # Allow selecting multiple values
                    ),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        

        dbc.Row(
            [
                dbc.Label("Add new accreditation body",
                    width=4),
                dbc.Col(
                    dbc.Input(id="new_accreditation_body_id", type="text"),
                    width=5,
                ),
                dbc.Col(
                    dbc.Button("+", color="primary", id="add_button",
                            n_clicks=0,
                            style={"font-weight": "bold"},
                    ),
                    width="auto",
                ),
            ],
            className="mb-1",
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
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/program_list"),  
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
                    html.H4('Program Registered Successfully.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                      "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='pro_alert_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4('New accreditation body added.'),
                ),
                
            ],
            centered=True,
            id='newaccred_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
    ]
)
 


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
                        html.H1("ADD NEW PROGRAM"),
                        html.Hr(),
                        dbc.Alert(id='pro_alert', is_open=False), # For feedback purpose
                        form, 
                        html.Br(),
                         
                        
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
        Output('pro_alert', 'color'),
        Output('pro_alert', 'children'),
        Output('pro_alert', 'is_open'),
        Output('pro_alert_successmodal', 'is_open')
    ],
    [Input('save_button', 'n_clicks')],
    [
        State('pro_degree_title', 'value'),
        State('pro_degree_shortname', 'value'),
        State('pro_degree_initials', 'value'),
        State('pro_cluster_id', 'value'),
        State('pro_college_id', 'value'),
        State('pro_department_id', 'value'),
        State('pro_degree_count', 'value'),
        State('pro_program_type_id', 'value'),
        State('pro_calendar_type_id', 'value'),
        State('pro_accreditation_body_id', 'value')  # JSON string input
    ]
)
def record_program_details(
    submitbtn,
    pro_degree_title,
    pro_degree_shortname,
    pro_degree_initials,
    pro_cluster_id,
    pro_college_id,
    pro_department_id,
    pro_degree_count,
    pro_program_type_id,
    pro_calendar_type_id,
    pro_accreditation_body_id
):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    # Ensure required fields are filled
    if not all([pro_degree_title, pro_degree_shortname, pro_degree_initials]):
        return [alert_color, "Missing required fields.", alert_open, modal_open]

    try:
        check_existing_title_sql = """
            SELECT 1 
            FROM eqateam.program_details 
            WHERE pro_degree_title = %s
        """
        existing_title = db.querydatafromdatabase(check_existing_title_sql, (pro_degree_title,), ["exists"])

        check_existing_shortname_sql = """
            SELECT 1 
            FROM eqateam.program_details 
            WHERE pro_degree_shortname = %s
        """
        existing_shortname = db.querydatafromdatabase(check_existing_shortname_sql, (pro_degree_shortname,), ["exists"])

        check_existing_initials_sql = """
            SELECT 1 
            FROM eqateam.program_details 
            WHERE pro_degree_initials = %s
        """
        existing_initials = db.querydatafromdatabase(check_existing_initials_sql, (pro_degree_initials,), ["exists"])

        # Construct an alert text based on which fields already exist
        if not existing_title.empty:
            alert_text = 'Degree Program Title already exists. Please use a different title.'
        elif not existing_shortname.empty:
            alert_text = 'Degree Program Shortname already exists. Please use a different shortname.'
        elif not existing_initials.empty:
            alert_text = 'Degree Program Initials already exists. Please use different initials.'

        if not existing_title.empty or not existing_shortname.empty or not existing_initials.empty:
            return [alert_color, alert_text, True, False]

        sql = """
            INSERT INTO eqateam.program_details (
                pro_degree_title, pro_degree_shortname,
                pro_degree_initials, pro_cluster_id,
                pro_college_id, pro_department_id,
                pro_degree_count, pro_program_type_id,
                pro_calendar_type_id, pro_accreditation_body_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
             
        """

        values = (
            pro_degree_title,
            pro_degree_shortname,
            pro_degree_initials,
            pro_cluster_id,
            pro_college_id,
            pro_department_id,
            pro_degree_count,
            pro_program_type_id,
            pro_calendar_type_id, 
            json.dumps(pro_accreditation_body_id) if pro_accreditation_body_id else None,
        )
            
            
        db.modifydatabase(sql, values)
        modal_open = True

    except Exception as e:
        return set_alert("An error occurred while saving the data: " + str(e), 'danger')

    return [alert_color, alert_text, alert_open, modal_open]


# Helper function for setting alerts
def set_alert(message, color):
    return [color, message, True, False]







@app.callback(
    [Output('newaccred_successmodal', 'is_open')],
    [Input('add_button', 'n_clicks')],
    [State('new_accreditation_body_id', 'value')]
)
def new_accreditation_details(addbtn, new_accreditation_body_id):
    if not addbtn or not new_accreditation_body_id:
        raise PreventUpdate  # Don't update if there's no click or no input
    
    modal_open = False

    try:
        sql = """
            INSERT INTO public.accreditation_body (
                body_name
            )
            VALUES (%s)
        """
        values = (new_accreditation_body_id,)
        db.modifydatabase(sql, values)  # Function to execute the SQL and commit changes
        modal_open = True  # Open a success modal

    except Exception as e:
        # Handle error appropriately
        modal_open = False
 
    return [modal_open]


 

# Cluster dropdown
@app.callback(
    Output('pro_cluster_id', 'options'),
    Input('url', 'pathname')
)
def populate_cluster_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/programlist/program_details':
        sql = """
        SELECT cluster_name as label, cluster_id  as value
        FROM public.clusters
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pro_cluster_types = df.to_dict('records')
        return pro_cluster_types
    else:
        raise PreventUpdate

# College dropdown
@app.callback(
    Output('pro_college_id', 'options'),
    Input('pro_cluster_id', 'value')
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
        
        pro_college_options = df.to_dict('records')
        return pro_college_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 

# Degree Unit dropdown
@app.callback(
    Output('pro_department_id', 'options'),
    Input('pro_college_id', 'value')
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
        
        pro_dgu_options = df.to_dict('records')
        return pro_dgu_options
    except Exception as e:
        # Log the error or handle it appropriately
        return []
    

 


# Program type dropdown
@app.callback(
    Output('pro_program_type_id', 'options'),
    Input('url', 'pathname')
)
def populate_programtype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/programlist/program_details':
        sql = """
        SELECT programtype_name  as label, programtype_id as value
        FROM eqateam.program_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pro_programtype_types = df.to_dict('records')
        return pro_programtype_types
    else:
        raise PreventUpdate




# Accreditation body dropdown
@app.callback(
    Output('pro_accreditation_body_id', 'options'),
    Input('url', 'pathname')
)
def populate_accreditationbody_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/programlist/program_details':
        sql = """
        SELECT body_name as label, accreditation_body_id as value
        FROM public.accreditation_body
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        accreditationbody_types = df.to_dict('records')
        return accreditationbody_types
    else:
        raise PreventUpdate

@app.callback(
    Output('proceed_button', 'href'),
    [Input('proceed_button', 'n_clicks')]
)
def redirect_to_program_list(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    
    return '/program_list'
