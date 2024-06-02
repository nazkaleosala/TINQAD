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

import bcrypt 

profile_image_path = '/assets/database/takagaki1.png'


# Your profile header component with circular image
profile_header = html.Div(
    [
        html.Div(
            html.Img(
                src=profile_image_path, 
                style={
                    'height': '100px', 
                    'width': '100px', 
                    'borderRadius': '50%',
                    'objectFit': 'cover',
                    'display': 'inline-block', 
                    'verticalAlign': 'center'
                }
            ),
            style={'textAlign': 'left', 'display': 'inline-block'}
        ),
        html.Div(
            [
                 
                html.H3(id="user_name_header", style={'marginBottom': 0, 'marginLeft': '25px'}),
                html.P("2020-*****", style={'marginBottom': 0, 'marginLeft': '25px'})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)

# Callback to update user name header
@app.callback(
    Output("user_name_header", "children"),
    [Input("currentuserid", "data")]
)
def update_user_name_header(user_id):
    user_info = db.get_user_info(user_id)  # Assuming get_user_info function retrieves user info
    if user_info:
        user_fname = user_info.get('user_fname', '')
        user_mname = user_info.get('user_mname', '')
        user_sname = user_info.get('user_sname', '')

        full_name = f"{user_fname} {user_mname} {user_sname}" if user_mname else f"{user_fname} {user_sname}"

        return full_name
    else:
        return "User Not Found"

 


form = dbc.Form( 
    [  
                dbc.Row(
                    [
                        dbc.Label("Previous Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="prev_password"), width=8),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Label("New Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="new_password"), width=8),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Label("Confirm Password", width=4),
                        dbc.Col(dbc.Input(type="password", id="confirm_password"), width=8),
                    ],
                    className="mb-2",
                ),
                html.Br(),
                dbc.Row(
                    [
                    dbc.Col(
                            dbc.Button("Save", color="primary", className="me-3", id="password_save_button", n_clicks=0),
                            width="auto"
                        ),
                    dbc.Col(
                            dbc.Button("Cancel", color="secondary", id="password_cancel_button", n_clicks=0),
                            width="auto"
                    ),
                ],
                className="mb-2",
            ),
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
                        html.H1("PROFILE"),
                        html.Div(  
                            [
                            dcc.Store(id='password_store', storage_type='session', data=0),
                            ]
                        ),
                        dbc.Row(
                            dbc.Col(
                                dbc.Alert(id = 'password_alert', color = 'dark')
                            )
                        ),
                        html.Hr(),
                        
                        html.Br(), 
                        form,  
                    ], 
                    width=6, 
                    style={'marginLeft': '15px'}
                ), 
            ]
        ),
        dbc.Row(
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
        Output('password_alert', 'color'),
        Output('password_alert', 'children'),
        Output('password_alert', 'is_open'),  
    ],
    [Input("password_save_button", "n_clicks")],
    [
        State("prev_password", "value"),
        State("new_password", "value"),
        State("confirm_password", "value"),
        State("user_id_store", "data")
    ]
)
def change_password_alert(n_clicks, prev_password, new_password, confirm_password, user_id):
    if n_clicks: 
        stored_password_hash = db.get_user_password_hash(user_id)   

        if bcrypt.checkpw(prev_password.encode('utf-8'), stored_password_hash):
            if new_password != confirm_password:
                return "danger", "New password and confirm password do not match!", True
            
            # Add validation for new password strength, minimum length, etc.
            if len(new_password) < 8:
                return "danger", "Password must be at least 8 characters long!", True
            
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            try:
                db.update_user_password_hash(user_id, new_password_hash)  
                return "success", "Password changed successfully!", True
            except Exception as e:
                print("Error updating password:", e)
                return "danger", "An error occurred while changing password.", True
        else:
            return "danger", "Current password is incorrect!", True
    else:
        return "", "", False