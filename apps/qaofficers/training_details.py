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
                dbc.Label("QA Officer Name", 
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id='',
                        placeholder="Select QA Officer",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Year", 
                width=4),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Name of Training", 
                width=4),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Training Type", 
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='',
                        placeholder="Select Training Type",
                    ),
                    width=6,
                ),
                  
            ],
            className="mb-2",
        ),
 
        html.Br(),
         
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Register", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
            ],
            className="mb-2",
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
                        html.H1("ADD TRAINING"),
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
 