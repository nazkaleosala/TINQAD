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


 

#main expense dropdown
@app.callback(
    Output('main_expenses_id', 'options'),
    Input('url', 'pathname')
)

def populate_mainexpenses_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/record_expenses':
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



#sub expense dropdown
@app.callback(
    Output('sub_expenses', 'options'),
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

#Amount
@app.callback(
   Output('exp_amount', 'value'),
   Input('exp_amount', 'value')
)
def format_amount(amount):
   if not amount or amount == '.':
       return ''
  
   cleaned_amount = ''.join([c for c in amount if c.isdigit() or c == '.']) # Filter out invalid characters
   parts = cleaned_amount.split('.')# Split into whole and decimal parts
   whole_part = parts[0]
   formatted_whole = format(int(whole_part) if whole_part else 0, ',d')# Format whole part with commas

   # Reconstruct the amount
   if len(parts) > 1:
       decimal_part = parts[1][:2]  # Take at most two decimal places
       formatted_amount = f'{formatted_whole}.{decimal_part}'
   else:
       formatted_amount = formatted_whole
   return formatted_amount


#BUR No
@app.callback(
   Output('exp_bur_no', 'value'),
   Input('exp_bur_no', 'value')
)
def format_bur_no(bur_no):
   if not bur_no:
       return ''
  
   bur_no = ''.join(filter(str.isdigit, bur_no)) # Remove non-numeric characters
   
   formatted_bur_no = ''   # Add dashes at appropriate positions
   for i, char in enumerate(bur_no):
       if i == 4 or i == 6:
           formatted_bur_no += '-'
       formatted_bur_no += char

   return formatted_bur_no[:13]  # Limit the length to fit the pattern
 
 


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
                   width=8,
               ),
           ],
           className="mb-3",
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
            className="mb-3",
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
                        "Particulars ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dbc.Textarea(id='exp_particulars', placeholder="Enter particulars"),
                   width=8,
               ),
           ],
           className="mb-3",
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
                    dbc.Input(
                        type="text", id='exp_amount', placeholder="0,000.00"
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
                        "Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dbc.Select(
                       id=' exp_status',
                       options=[
                           {"label": "Approved", "value": 1},
                           {"label": "Pending", "value": 2},
                           {"label": "Denied", "value": 3},
                           # Include other options here
                       ],
                       placeholder="Select status",
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
                        "BUR No. ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(
                        type="text", id='exp_bur_no', placeholder="0000-00-00000"
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
                        "Submitted by",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4
                ),
               dbc.Col(
                   dbc.Input(type="text", id='exp_submitted_by', placeholder="First Name Last Name"),
                   width=8,
               ),
           ],
           className="mb-3",
       ),

        dbc.Row(
                dbc.Col(
                    dcc.Upload(
                        id='exp_receipt',  
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('upload_photo.png'),
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
           className="mb-4",
       ),

       dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4('Expense added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='recordexpense_successmodal',
            backdrop=True,  # Allow clicking outside to close the modal
            className="modal-success"   
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
                   html.H1("ADD EXPENSE"),
                   html.Hr(),
                   dbc.Alert(id='recordexpense_alert', is_open=False),
                   form,
               ],
               width=8, style={'marginLeft': '15px'}
              
               )
           ]
       ),
       #footer
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
        Output('recordexpense_alert', 'color'),
        Output('recordexpense_alert', 'children'),
        Output('recordexpense_alert', 'is_open'),
        Output('recordexpense_successmodal', 'is_open')
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
 



def record_expenses(submitbtn, date, payee, mainexpense, subexpense, 
                    particulars, amount, status, bur_no, submittedby):
    ctx = dash.callback_context 
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid != 'save_button' or not submitbtn:
        raise PreventUpdate
 
    alert_open = False
    modal_open = False
    alert_color = ''
    alert_text = ''
 
    if not date:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a date.'
        return [alert_color, alert_text, alert_open, modal_open]

    if not payee:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a payee.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not mainexpense:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a mainexpense.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not subexpense:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a subexpense.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not particulars:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a particulars.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not amount:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add an amount.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not status:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a status.'
        return [alert_color, alert_text, alert_open, modal_open]
    
    if not bur_no:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a bur_no.'
        return [alert_color, alert_text, alert_open, modal_open]
 

    # Default values
    exp_receipt = 1  


    # SQL query to insert data
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
 
    values = (
        date, payee, mainexpense, subexpense, 
        particulars, amount, status, bur_no, submittedby, exp_receipt
    )

    db.modifydatabase(sql, values)
    # If this is successful, we want the successmodal to show
    modal_open = True

    return [alert_color, alert_text, alert_open, modal_open] 

 

 