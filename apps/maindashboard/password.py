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
                 
                html.H3("Pikachu, Pika", style={'marginBottom': 0, 'marginLeft': '25px'}),
                html.P("2020-*****", style={'marginBottom': 0, 'marginLeft': '25px'})  
            ],
            style={'display': 'inline-block', 'verticalAlign': 'center'}
        ),
    ],
    style={'textAlign': 'left', 'marginTop': '20px'}
)




 


form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Previous Password", width=4),
                dbc.Col(dbc.Input(type="text"  ), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("New Password", width=4),
                dbc.Col(dbc.Input(type="text"), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Confirm Password", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
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
         
    ],
    className="g-2",
)

  
@app.callback(
    Output("output-message", "children"),
    [Input("save_button", "n_clicks")],
    [State("prev_password", "value"),
     State("new_password", "value"),
     State("confirm_password", "value")]
)

def change_password(n_clicks, prev_password, new_password, confirm_password):
    if n_clicks > 0:
        # Verify if new password matches confirm password
        if new_password != confirm_password:
            return "New password and confirm password do not match!"
        
        # Check if previous password matches the one stored in the database
        user_id = cm.get_user_id()  # Assuming you have a function to get the user ID
        stored_password = db.get_user_password(user_id)  # Assuming you have a function to get user's password
        
        if stored_password != prev_password:
            return "Previous password is incorrect!"
        
        # Update the password in the database
        db.update_user_password(user_id, new_password)  # Assuming you have a function to update user's password
        
        return "Password changed successfully!"
    else:
        return ""



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
                    html.Hr(),
                    profile_header,  # Insert the profile header here
                    html.Br(), 
                    form,  # Insert the profile table here
                    

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