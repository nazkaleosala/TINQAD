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

def hash_password(password):
    # Convert the password to bytes if it's a string
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Generate the hashed password
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ", 
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_fname'),
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
                    dbc.Input(type="text", id='user_mname'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        # Surname
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
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
                dbc.Label(
                    [
                        "Lived Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_livedname'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Sex Assigned at Birth ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_sex',
                        options=[ 
                            {'label': 'Female', 'value': '2'},
                            {'label': 'Male', 'value': '1'}, 
                        ]
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
                        "Birthday ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="date", id='user_bday'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Phone Number ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id='user_phone_num'),
                    width=6,
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
                    dbc.Input(type="text", id='user_id_num'),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Office ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Select(
                        id='user_office',
                        options=[]
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
                    width=6,
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
                    width=6,
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
                    dbc.Button("Save", color="primary", className="me-1", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
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
                    html.H4('User registered successfully.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='registeruser_successmodal',
            backdrop=True,  # Allow clicking outside to close the modal
            className="modal-success"  # You can define this class in your CSS file for additional styling
        ),
        
    ],
    className="g-2",
)

  
#cancel button callback
cancel_modal = dbc.Modal(
    [
        dbc.ModalHeader(className="bg-warning"),
        dbc.ModalBody([
            html.P("Are you sure you want to cancel? "),
        ]),
        dbc.ModalFooter(
            [
                dbc.Button("Close", id="close_modal", className="mr-2", n_clicks=0),
                dbc.Button("Confirm Cancellation", color="danger", id="confirm_cancel", n_clicks=0),
            ],
            className="justify-content-end"
        )
    ],
    id="cancel_modal",
    is_open=False,  # Starts hidden
)

@app.callback(
    Output("cancel_modal", "is_open"),
    [Input("cancel_button", "n_clicks"), Input("close_modal", "n_clicks"), Input("confirm_cancel", "n_clicks")],
    [State("cancel_modal", "is_open")],
)
def toggle_modal(cancel_click, close_click, confirm_click, is_open):
    if cancel_click or close_click or confirm_click:
        return not is_open
    return is_open

@app.callback(
    Output('dummy-div', 'children'),
    [Input('confirm_cancel', 'n_clicks')],
    prevent_initial_call=True
)
def refresh_on_confirm(n_clicks):
    return dash.no_update

@app.callback(
    Output('url', 'pathname'),
    [Input('confirm_cancel', 'n_clicks')],
    prevent_initial_call=True
)
def redirect_to_homepage(n_clicks):
    if n_clicks:
        return '/homepage'
    raise PreventUpdate


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
                    cancel_modal,
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
        State('confirm_password', 'value')  
    ]
)
 

def register_user(submitbtn, fname, mname, sname, livedname, 
                  sex, bday, phone_num, id_num, 
                  office, position, email, password, confirm_password):
    ctx = dash.callback_context
    # Check if the callback was triggered by the 'save_button'
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'save_button' or not submitbtn:
        raise PreventUpdate

    # Initialize the alert variables
    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Validate password and confirmation password
    if not password:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a password.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not confirm_password:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please confirm your password.'
        return [alert_color, alert_text, alert_open, modal_open]

    if password != confirm_password:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Passwords do not match. Please try again.'
        return [alert_color, alert_text, alert_open, modal_open]

    # Hash the password
    hashed_password = hash_password(password)


    # Default values
    user_access_type = 1
    user_acc_status = 1
    user_profile_pic = None  # This will be interpreted as NULL in SQL


    # SQL query to insert data
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
 
    values = (
        fname, mname, sname, livedname, 
        sex, bday, phone_num, id_num, 
        office, position, email, hashed_password, 
        user_access_type, user_acc_status, user_profile_pic
    )

    db.modifydatabase(sql, values)
    # If this is successful, we want the successmodal to show
    modal_open = True

    return [alert_color, alert_text, alert_open, modal_open] 

 
