import dash
from dash import callback_context, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

import bcrypt
 
layout = dbc.Row(
    [
        dbc.Col(
            html.Div(
            [
                html.Div(  
                            [
                                dcc.Store(id='user_id_store', storage_type='session', data=0),
                            ]
                        ),
                
                html.Div(
                    [
                        html.Img(src=app.get_asset_url('icons/qao-logo-block.png'),
                                style = {
                                    'max-width': '25vw',
                                    'margin': 'auto',  # Center the image horizontally
                                    'display': 'block'  # Make sure it's displayed as a block element
                                },
                        ),
                        html.H5("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-center"),
                        html.P("Copyright © 2024. Quality Assurance Office, University of the Philippines", className="text-center"),
                   
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.A("About TINQAD", href="/about-us", className="link-style"), " • ",
                                        html.A("Main Website", href="https://qa.upd.edu.ph/", className="link-style"), " • ",
                                        html.A("Facebook", href="https://www.facebook.com/QAODiliman", className="link-style"), " • ",
                                        html.A("LinkedIn", href="https://www.linkedin.com/company/quality-assurance-office/about/", className="link-style")
                                    ],
                                    width = "auto"
                                ),
                            ],
                            style = {'margin' : 'auto'},
                            align = 'center', justify = 'center'
                        ),
                    ],
                    style = {
                        'top': '10rem',
                        'right': '25rem',
                        'position': 'relative',   
                        'z-index': 1,
                        'max-width': '70vw',
                        'margin': 'auto',
                        'text-align': 'center',
                        'padding': '2em',
                        
                    }
                ),




                html.Div(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("LOG IN", className="card-title fw-bolder "),
                                        html.Br(),

                                            dbc.Alert(
                                                'User email or password is incorrect',
                                                color = 'danger',
                                                id = 'login_alert',
                                                is_open = False
                                            ),
                                            
                                            dbc.Label("Registered Email"),
                                            dbc.Input(type="text", id="login_username", ),
                                            html.Br(),
                                            
                                            dbc.Label("Password"),
                                            dbc.Input(type="password", id="login_password"),
                                            html.Br(),
                                                
                                                dbc.Row(
                                                    dbc.Col(
                                                        dbc.Button("Log in", 
                                                                   color="primary", 
                                                                   className="fw-bolder", 
                                                                   id = 'login_loginbtn'),
                                                            width={'size': 4, 'offset': 8},   
                                                            className="d-flex justify-content-end"
                                                    )
                                                ),
                                                html.Br(),
                                                html.Br(),
                                                html.H4("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-danger" ),
                                                html.P ("The Total Integrated Network for Quality Assurance and Development (TINQAD) is a centralized network that allows the singular monitoring of the Quality Assurance teams activities."),
                                                 
                                            ]
                                        ),
                                    ),
                                     
                                    width={"size": 6, "offset": 1},   
                                    style={
                                        'position': 'fixed',
                                        'right': '2rem',  # Position the div at the right of the screen
                                        'width': '45%',  # Set the width of the div
                                        'bottom': '3rem',  # Adjusted bottom margin
                                        'padding': '1rem',
                                        'border-radius': '10px',
                                        'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',  # Add box shadow
                                    }
                                 
                                 
                                ),
                            ]
                        ),
                    ],
            id='bg',
            style={
                'position': 'fixed',
                'top': '3.5rem',  # Adjust the top margin as needed
                'left': '0',
                'width': '100%',
                'height': '100%',
                'min-height': 'calc(100% + 20rem)',  # Set a minimum height to ensure content is scrollable
                'background-image': 'url("' + app.get_asset_url('icons/bg.png') + '")',
                'background-size': 'cover',
                'background-position': 'center bottom',
                'mask-image': 'linear-gradient(to bottom, rgba(0, 0, 0, 1.0) 50%, transparent 100%)',
                
            }
        ),
        ),
    ]
)



# Function to verify password
def verify_password(password, stored_password):
    return stored_password == password

 
def encrypt_string(string):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(string.encode('utf-8'), salt)
    return hashed



@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
        Output('currentrole', 'data'),  
        Output('url', 'pathname'),  # Adding URL pathname output
    ],
    [
        Input('login_loginbtn', 'n_clicks'), 
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'), 
        State('currentuserid', 'data'), 
        State('url', 'pathname'),
    ]
)
def loginprocess(loginbtn, useremail, password, currentuserid, pathname):    
    ctx = callback_context
    if ctx.triggered:
        accesstype = 0
        openalert = False
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
         
        if eventid == 'login_loginbtn':
            if loginbtn and useremail and password:
                sql = """
                SELECT 
                    user_id, 
                    user_access_type,
                    user_password
                FROM maindashboard.users
                WHERE
                    user_email = %s 
                """

                values = [useremail]
                cols = ['user_id', 'user_access_type', 'user_password']

                df = db.querydatafromdatabase(sql, values, cols)
                if not df.empty:
                    if df['user_password'][0] == password:
                        currentuserid = df['user_id'][0]
                        accesstype = df['user_access_type'][0]  
                        # Redirect to homepage
                        return [openalert, currentuserid, accesstype, '/homepage']
                    else:
                        currentuserid = -1
                        openalert = True
                else:
                    raise PreventUpdate
        return [openalert, currentuserid, accesstype, pathname]  # Returning the current URL pathname if login fails
    else:
        raise PreventUpdate