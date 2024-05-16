import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import Dash, html, dcc, Input, Output, State

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from datetime import datetime
import bcrypt 
import re

from urllib.parse import urlparse, parse_qs


def hash_password(password):
    # Convert the password to bytes if it's a string
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Generate the hashed password
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password

  

#offices dropdown
@app.callback(
    Output('user_office', 'options'),
    Input('url', 'pathname')
)

def populate_offices_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/register_user':
        sql = """
        SELECT office_name as label, office_id as value
        FROM maindashboard.offices
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        office_options = df.to_dict('records')
        return office_options
    else:
        raise PreventUpdate

 


# Define your app layout
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
                        html.H1("REGISTER NEW USER"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Label("Select user type", width="auto"),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='user_type_dropdown',
                                        options=[
                                            {"label": "Full User Profile", "value": 1},
                                            {"label": "Office User Profile", "value": 2},
                                        ],
                                        value=2
                                    ),
                                    width=4
                                )
                            ],
                            className="mb-2",
                        ), 
                        dbc.Alert(id='registeruser_alert', is_open=False), # For feedback purpose
                        html.Div(id='user_form'), 
                        html.Br(),
                        dbc.Row(
                            [ 
                                dbc.Col(
                                    dbc.Button("Save", color="primary",  id="registeruser_save_button", n_clicks=0),
                                    width="auto"
                                ),
                                dbc.Col(
                                    dbc.Button("Cancel", color="warning", id="registeruser_cancel_button", n_clicks=0, href="/search_users"),  
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
                                    ],id='registeruser_feedback_message'
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Proceed", href='/homepage', id='registeruser_btn_modal'
                                    ), 
                                )
                                
                            ],
                            centered=True,
                            id='registeruser_successmodal',
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
        html.Div(id='dummy-div', style={'display': 'none'})
    ]
)

# Define callback to enable/disable input fields based on user type selection
@app.callback(
    Output('user_form', 'children'),
    Output('user_form', 'disabled'),
    [Input('user_type_dropdown', 'value')]
)
def update_form_and_fields(user_type):
    form_disabled = user_type != 1
    form_content = [
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "First Name ", 
                            html.Span("*", style={"color": "#F8B237"})
                        ], 
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_fname', disabled=form_disabled),
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
                        dbc.Input(type="text", id='user_mname', disabled=form_disabled),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Surname ",
                            html.Span("*", style={"color": "#F8B237"})
                        ], 
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_sname', disabled=form_disabled),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Lived Name ",
                        ], 
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_livedname', disabled=form_disabled),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Sex Assigned at Birth "
                            
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Select(
                            id='user_sex',
                            options=[ 
                                {'label': 'Female', 'value': '2'},
                                {'label': 'Male', 'value': '1'}, 
                            ], 
                            disabled=form_disabled
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
                            "Birthday "
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Input(type="date", id='user_bday', disabled=form_disabled),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Phone Number "
                        ], 
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_phone_num', placeholder="0000 000 0000", maxLength=13, disabled=form_disabled),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "ID Number ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_id_num', placeholder="0000 00000", disabled=form_disabled),
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
                            html.Span("*", style={"color":"#F8B237"})
                        ],
                        width=4
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='user_office',
                            placeholder="Select Office", 
                            
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
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_position'),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Email Address ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Input(type="text", id='user_email'),
                        width=6,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Password ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Input(type="password", id='user_password'),
                        width=5,
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Confirm Password ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=4),
                    dbc.Col(
                        dbc.Input(type="password", id = 'confirm_password', placeholder = 'Confirm password' ),
                        width=5,
                    ),
                ],
                className="mb-2",
            ),
            # Access Type
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Access Type ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],width=4),
                    dbc.Col(
                        dbc.Select(
                            id='user_access_type',
                            options=[ 
                                {'label': 'Basic Access', 'value': '1'},
                                {'label': 'Full Access', 'value': '2'}, 
                            ], 
                            value='1',
                            disabled=form_disabled
                        ),
                        width=4,
                    ),
                ],
                className="mb-2",
            ),


    ]
    return form_content, form_disabled

 
 








@app.callback(
    [
        Output('registeruser_alert', 'color'),
        Output('registeruser_alert', 'children'),
        Output('registeruser_alert', 'is_open'),

        Output('registeruser_successmodal', 'is_open'),
        Output('registeruser_feedback_message', 'children'),
        Output('registeruser_btn_modal', 'href'),
    ],
    [
        Input('registeruser_save_button', 'n_clicks'),
        Input('registeruser_btn_modal', 'n_clicks'),
    ],
    [
        State('user_fname', 'value'),
        State('user_mname', 'value'),
        State('user_sname', 'value'),
        State('user_livedname', 'value'),
        State('user_sex', 'value'),
        State('user_bday', 'value'),
        State('user_phone_num', 'value'),
        State('user_id_num', 'value'),
        State('user_office', 'value'),
        State('user_position', 'value'),
        State('user_email', 'value'),
        State('user_password', 'value'),
        State('confirm_password', 'value'),
        State('url', 'search')
    ]
)
def register_user(submitbtn, closebtn, 
                  fname, mname, sname, livedname, 
                  sex, bday, phone_num, id_num, 
                  office, position, email, password, confirm_password,
                  search):
    
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'registeruser_save_button' and submitbtn:
        
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            if not password:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please add a password.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]

            if not confirm_password:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please confirm your password.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]

            if password != confirm_password:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Passwords do not match. Please try again.'
                return [alert_color, alert_text, alert_open, modal_open, None, None]
            
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]
                 
                if create_mode == 'add':
                    
                    sql = """
                        INSERT INTO maindashboard.users (
                            user_fname, user_mname, user_sname, user_livedname, 
                            user_sex, user_bday, user_phone_num, user_id_num, 
                            user_office, user_position, user_email, user_password, 
                            user_access_type, user_acc_status, user_profile_pic
                        )
                        VALUES (
                            %s, %s, %s, %s, 
                            %s, %s, %s, %s, 
                            %s, %s, %s, %s, 
                            %s, %s, %s
                        )
                    """
                    
                    hashed_password = hash_password(password)
                    fname  = "Office Account"
                    mname  = "Office Account"
                    sname  = "Office Account"
                    user_access_type = 1
                    user_acc_status = 1
                    user_profile_pic = None  

                    values = (
                        fname, mname, sname, livedname, 
                        sex, bday, phone_num, id_num, 
                        office, position, email, hashed_password, 
                        user_access_type, user_acc_status, user_profile_pic
                    )

                    db.modifydatabase(sql, values) 
                    modal_open = True
                    feedback_message = html.H5("User registered successfully.")
                    return [None, None, None, modal_open, feedback_message, None]
                    
                elif create_mode == 'edit':
                    pass

                else:
                    raise PreventUpdate

    return [None, None, None, False, None, None]