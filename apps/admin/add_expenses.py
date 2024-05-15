import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, no_update

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

import locale
import re

form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Date ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                       id='exp_date',
                       date=str(pd.to_datetime("today").date())
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Payee ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_payee', placeholder="First Name Last Name"),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Expense Main Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='main_expense_id',
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
                        "Expense Sub Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='sub_expense_id',
                        options=[]
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Particulars "
                    ],
                    width=4
                ),
                dbc.Col(
                   dbc.Textarea(id='exp_particulars', placeholder="Enter particulars"),
                   width=8,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Amount ",
                        html.Span("*", style={"color": "#F8B237"}) 
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_amount', placeholder="0,000.00"),
                    width=5,
                ),
                dbc.Col(
                    html.Div(id='amount-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Select(
                        id='exp_status',
                        options=[ 
                            {"label": "Approved", "value": 1},
                            {"label": "Pending", "value": 2},
                            {"label": "Denied", "value": 3},
                        ]
                    ),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "BUR No. ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id='exp_bur_no', placeholder="0000-00-00000", maxLength=11),
                    width=5,
                ),
                dbc.Col(
                    html.Div(id='bur-no-copy', style={"color": "#C4BDBD"}),
                    width=2,
                )
            ],
            className="mb-2",
        ),
 
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Submitted by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="text", id = 'exp_submitted_by'),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
                dbc.Col(
                    dcc.Upload(
                        id='upload_receipt',
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/upload_photo.png'),
                                    style={'width': '50px', 'height': '50px', 'margin-bottom': '5px'}
                                ),
                                html.Div([
                                    "Add Receipt ",
                                    html.Span("*", style={'color': '#F8B237'})
                                ], style={'fontWeight': 'bold', 'fontSize': '20px', 'margin-bottom': '1px'}),
                                html.Div("Drag and Drop or Select Files", style={'fontSize': '14px'})
                            ],
                            style={
                                'display': 'flex',
                                'flexDirection': 'column',
                                'alignItems': 'center',
                                'justifyContent': 'center',
                                'height': '100%',
                                'padding': '15px 30px'  # Adjust padding as needed
                            }
                        ),
                        style={
                            'width': '100%', 'minHeight': '100px',  # Adjust height as needed
                            'borderWidth': '2px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                        multiple=True
                    ),
                    lg={'size': 8, 'offset': 2},  # Adjust size and offset for proper alignment
                    md={'size': 10, 'offset': 1},
                    sm={'size': 12},
                    style={'marginBottom': '1rem'}
                ),
            ),
          
        dbc.Row(
            [dbc.Col(id="expense_name_output",style={"color": "#F8B237"}, width=8)],  # Output area for uploaded file names
            className="mt-2",
        ),
  
        
        html.Br(),
        dbc.Row(
            [ 
                
                dbc.Col(
                    dbc.Button("Save", color="primary",  id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="warning", id="cancel_button", n_clicks=0, href="/record_expenses"),  
                    width="auto"
                ),
            ],
            className="mb-2",
            justify="end",
        ),
 
        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(html.H4('Expense added.')),
                 
            ],
            centered=True,
            id='recordexpenses_successmodal', #palit ID
            backdrop=True,   
            className="modal-success"   
        )
        
    ],
    className="g-2",
)


 


# Callback to display the names of the uploaded files
@app.callback(
    Output("expense_name_output", "children"),
    [Input("upload_receipt", "filename")],  # Use filename to get uploaded file names
)
def display_uploaded_files(filenames):
    if not filenames:
        return "No files uploaded"
    
    if isinstance(filenames, list): 
        file_names_str = ", ".join(filenames)
        return f"Uploaded files: {file_names_str}"
 
    return f"Uploaded file: {filenames}"













#main expense dropdown
@app.callback(
    Output('main_expense_id', 'options'),
    Input('url', 'pathname')
)

def populate_mainexpenses_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/record_expenses/add_expense':
        sql = """
        SELECT main_expense_name as label,  main_expense_id  as value
        FROM adminteam.main_expenses
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        main_expense_types = df.to_dict('records')
        return main_expense_types
    else:
        raise PreventUpdate
 

#amount
locale.setlocale(locale.LC_ALL, '')

@app.callback(
    Output('amount-copy', 'children'),
    Input('exp_amount', 'value')
)
def update_amount_copy(value):
    if value is None:
        return None  # Return None if value is None

    try:
        # Try to convert the input value to a float
        float_value = float(value.replace(',', ''))
        # Format the float value with commas and two decimal places
        formatted_value = locale.format_string("%0.2f", float_value, grouping=True)
        return formatted_value
    except ValueError:
        # If conversion fails, return None
        return None




#bur
@app.callback(
    Output('bur-no-copy', 'children'),
    Input('exp_bur_no', 'value')
)
def update_bur_no_copy(value):
    if value:
        # Remove any non-digit characters
        cleaned_value = re.sub(r'\D', '', value)
        # Format the cleaned value as ####-##-#####
        formatted_value = '-'.join([cleaned_value[:4], cleaned_value[4:6], cleaned_value[6:]])
        return formatted_value
    else:
        return ''




#sub expense dropdown
@app.callback(
    Output('sub_expense_id', 'options'),
    Input('main_expense_id', 'value')
)
def update_subexpenses_options(selected_main_expense):
    if selected_main_expense is None:
        return []  # Return empty options if no main expense is selected
    
    try:
        # Query to fetch sub-expenses based on the selected main expense
        sql = """
        SELECT sub_expense_name as label, sub_expense_id as value
        FROM adminteam.sub_expenses
        WHERE main_expense_id = %s
        """
        values = [selected_main_expense]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        sub_expense_options = df.to_dict('records')
        return sub_expense_options
    except Exception as e:
        # Log the error or handle it appropriately
        return [] 






# Callbacks for formatting input fields
#BUR No
@app.callback(
    Output('exp_bur_no', 'value'),
    Input('exp_bur_no', 'n_blur'),
    State('exp_bur_no', 'value')
)
def format_bur_no(n_blur, bur_no):
    if not bur_no:
        return ''

    # Removing non-numeric characters
    bur_no = ''.join(filter(str.isdigit, bur_no))

    # Formatting the BUR number
    formatted_bur_no = ''
    for i, char in enumerate(bur_no):
        if i in [4, 6]:  # Adding dashes after 4th and 6th digit
            formatted_bur_no += '-'
        formatted_bur_no += char

    # Trimming to the pattern length (13 including dashes)
    return formatted_bur_no[:13]
 
 
 














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
                    html.H1("ADD EXPENSE"),
                    html.Hr(),
                    dbc.Alert(id='recordexpenses_alert', is_open=False), # For feedback purpose
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
        ),
        
    ]
)





@app.callback(
    [
        Output('recordexpenses_alert', 'color'),
        Output('recordexpenses_alert', 'children'),
        Output('recordexpenses_alert', 'is_open'),
        Output('recordexpenses_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('exp_date', 'date'),
        State('exp_payee', 'value'),
        State('main_expense_id', 'value'),
        State('sub_expense_id', 'value'),
        State('exp_particulars', 'value'),
        State('exp_amount', 'value'),
        State('exp_status', 'value'),  
        State('exp_bur_no', 'value'),
        State('exp_submitted_by', 'value'), 
    ]
)
 


def record_expenses(submitbtn, date, payee, mainexpense, 
                    subexpense, particulars, amount, 
                    status, bur_no, submittedby):
    if not submitbtn:
        raise PreventUpdate

    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not date:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a date.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not payee:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Payee.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not mainexpense:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Main expense.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not subexpense:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Sub expense.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not particulars:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Particulars.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not amount:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add an Amount.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not status:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Status.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not bur_no:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a BUR no.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not submittedby:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add Submitted by.'
        return [alert_color, alert_text, alert_open, modal_open]
 


    # Default values
    exp_receipt = None

    # Insert data into the database
    try:
        sql = """
            INSERT INTO adminteam.expenses (
                exp_date, exp_payee, main_expense_id, sub_expense_id, 
                exp_particulars, exp_amount, exp_status, 
                exp_bur_no, exp_submitted_by, exp_receipt
            )
            VALUES (
                %s, %s, %s, %s, 
                %s, %s, %s, 
                %s, %s, %s
            )
        """
        values = (date, payee, mainexpense, subexpense, particulars, amount, status, bur_no, submittedby, exp_receipt)
        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'
        alert_open = True

    return [alert_color, alert_text, alert_open, modal_open]
