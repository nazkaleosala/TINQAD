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
password_header = html.Div(
    [
        html.Div(
            [
                html.H3(id="password_name_header", style={'marginBottom': 0}),
                html.P(id="password_idnumber", style={'marginBottom': 0})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)
 

@app.callback(
    [
        Output('password_name_header', 'children'),
        Output('password_idnumber', 'children'),
    ], 
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)
def update_password_header(pathname, current_userid):
    user_info = db.get_user_info(current_userid)

    if user_info: 
        user_fname = user_info.get('user_fname', '')
        user_sname = user_info.get('user_sname', '')
        user_livedname = user_info.get('user_livedname', '')
        user_id_num = user_info.get('user_id_num', '')

        # Concatenate full name
        fullname_parts = [part for part in [user_fname, user_sname] if part]   
        if user_livedname:
            fullname_parts.append('"' + user_livedname + '"')
        fullname = " ".join(fullname_parts)

        return fullname, user_id_num
    else:
        return "",""
  
 


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
                        password_header,
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

 