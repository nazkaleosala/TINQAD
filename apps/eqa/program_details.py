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
                        "Academic Cluster ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pr_cluster_id  ', 
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
                        id='pr_department_id ', 
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
                        id='pr_college_id', 
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
                        "Degree Program Title",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='pr_degree_id', 
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
                    dbc.Input(type="number", id="degree-count"),
                    width=4,
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
                        id='program_type_id', 
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
                        "Academic Calendar Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='academic_calendar_type_id ', 
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
                        "Applicable Accredited Bodies",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="pr_accreditation_body_id",
                        options=[],
                        multi=True  # Allow selecting multiple values
                    ),
                    width=5,
                ),
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
                 dbc.Col(
                    dbc.Button("Register", color="primary", className="me-3", id="save_button", n_clicks=0),
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
            id='arep_successmodal',
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
                        dbc.Row(
                            [
                                form, 
                                  
                            ] 
                        ), 
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



#degree program id dropdown
@app.callback(
    Output('pr_degree_id', 'options'),
    Input('url', 'pathname')
)
def populate_reporttype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/programlist/program_details':
        sql ="""
        SELECT degree_name as label, degree_id as value
        FROM  public.degree_programs
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        pr_degree_types = df.to_dict('records')
        return pr_degree_types
    else:
        raise PreventUpdate

