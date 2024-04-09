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
                dbc.Label("First Name", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_fname'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Initial", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_midinitial'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        # Surname
        dbc.Row(
            [
                dbc.Label("Surname", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_sname'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        # Lived Name
        dbc.Row(
            [
                dbc.Label("Lived Name", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_livedname'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Sex Assigned at Birth", width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_sex',
                        options=[ 
                            {'label': 'Female', 'value': 'Female'},
                            {'label': 'Male', 'value': 'Male'}, 
                        ]
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Birthday", width=4),
                dbc.Col(
                    dbc.Input(type="date", id='user_bday'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Phone Number", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_phone_num'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("ID Number", width=4),
                dbc.Col(
                    dbc.Input(type="number", id='user_id_num'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Office / Department", width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_office',
                        options=[ 
                            {'label': 'Department 1', 'value': '1'},
                            {'label': 'Department 2', 'value': '2'}, 
                        ]
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Position", width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_position'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Email Address", width=4),
                dbc.Col(
                    dbc.Input(type="email", id='user_email'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Password", width=4),
                dbc.Col(
                    dbc.Input(type="password", id='user_password'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        # Access Type
        dbc.Row(
            [
                dbc.Label("Access Type", width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_access_type',
                        options=[ 
                            {'label': 'Basic Access', 'value': 'Basic Access'},
                            {'label': 'Full Access', 'value': 'Full Access'}, 
                        ]
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Account Status", width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_acc_status',
                        options=[ 
                            {'label': 'Active', 'value': 'Active'},
                            {'label': 'Suspended', 'value': 'Suspended'},  
                            {'label': 'Deleted', 'value': 'Deleted'}, 
                        ]
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
                    dbc.Button("Save", color="primary", className="me-3", id="save_button", n_clicks=0),
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
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                'Message here! Edit me please!'
                ),
                    dbc.ModalFooter(
                        dbc.Button(
                        "Proceed",
                            href='/register_user' # Clicking this would lead to a change of pages
                    )
                )
            ],
            centered=True,
            id='registeruser_successmodal',
            backdrop='static' # Dialog box does not go away if you click at the background
        )
        
    ],
    className="g-2",
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
                    html.H1("CREATE NEW USER"),
                    html.Hr(),
                    dbc.Alert(id='registeruser_alert', is_open=False), # For feedback purpose
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
        )
    ]
)


@app.callback(
    [
         
        Output('registeruser_alert', 'color'),
        Output('registeruser_alert', 'children'),
        Output('registeruser_alert', 'is_open'),
         
        Output('registeruser_successmodal', 'is_open')
    ],
    [ 
        Input('save_button', 'n_clicks')
    ],
    [
    
        State('user_fname', 'value'),
        State('user_midinitial', 'value'),
        State('user_sname', 'value'),
        State('user_livedname', 'value'),
        State('user_sex', 'value'),  # You might want to handle this as a Dropdown or RadioItems
        State('user_bday', 'date'),
        State('user_phone_num', 'value'),
        State('user_id_num', 'value'),
        State('user_office', 'value'),  # This might be a Dropdown linked to your offices table
        State('user_position', 'value'),
        State('user_email', 'value'),
        State('user_password', 'value'),  # Ensure this is handled securely
        State('user_access_type', 'value'),  # Dropdown linked to your access_type table
        State('user_acc_status', 'value'),  # Dropdown linked to your account_status table
        State('user_profile_pic', 'value')  # This would require handling file upload
    ]
)

 
def register_user(submitbtn, user_fname, user_midinitial, user_sname, user_livedname, user_sex, user_bday, user_phone_num, user_id_num, user_office, user_position, user_email, user_password, user_access_type, user_acc_status, user_profile_pic):
    ctx = dash.callback_context
    # Ensure that the function is triggered by the intended action (e.g., a button click)
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'registeruser_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout
            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            if not user_fname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the first name.'
            elif not user_sname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please supply the surname.' 
            else:

                sql = """  
                    SELECT user_sname AS "Surname", user_fname AS "First Name", user_office AS "Dept", 
                        user_position AS "Position", user_email AS "Email",  
                        user_phone_num AS "Phone"
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = [submitbtn, user_fname, user_midinitial, user_sname, user_livedname, user_sex, user_bday, user_phone_num, user_id_num, user_office, user_position, user_email, user_password, user_access_type, user_acc_status, False]

                db.modifydatabase(sql, values)
                
                modal_open = True
            
            return [alert_color, alert_text, alert_open, modal_open]
        else:  
            raise PreventUpdate
    else:
        raise PreventUpdate
    