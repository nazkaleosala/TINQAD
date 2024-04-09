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


# Define the mapping for main expense types and corresponding sub-types
main_expense_types = {
   "MOOE": "Maintenance and Other Operating Expenses (MOOE)",
   "Training": "Training & Workshop Expenses (External)",
   "Equipment": "Equipment Outlay"
}


sub_expense_types = {
   "MOOE": [
       "General office supplies", "Meals and other Pantry Supplies",
       "Printing and Publication expenses", "VoIP/Communication Expenses",
       "Subscription Expenses", "Courier, Postage, and Transportation expenses",
       "Janitorial/Office Maintenance", "Semi-Expendable Equipment and Peripherals",
       "Strategic Planning, Mid-year Review, and Year End Review", "Transportation",
       "Benchmarking Activity"
   ],
   "Training": [
       "INSPIRE", "ISO 21001:2018", "Philippine Quality Award (PQA)", "ASPIRE",
       "Registration Fees and Airfare for QA training", "External Assessment (AUN-QA) fees and expenses",
       "External Assessment (PTC-ACBET) fees and expenses", "Honoraria of API 2024 Reviewers"
   ],
   "Equipment": [
       "Database Server", "Videoconferencing Equipment", "2 units High Resolution Camera",
       "Heavy Duty Printer"
   ]
}




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
                       id='date-input',
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
                   dbc.Input(type="text", id='payee-input', placeholder="First Name Last Name"),
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
                   dcc.Dropdown(
                       id='expense-main-type-dropdown',
                       options=[{"label": name, "value": code} for code, name in main_expense_types.items()],
                       placeholder="Select Expense Main Type",
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
                        "Expense Sub Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dcc.Dropdown(
                       id='expense-sub-type-dropdown',
                       placeholder="Select Expense Sub Type",
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
                        "Particulars ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4
                ),
               dbc.Col(
                   dbc.Textarea(id='particulars-input', placeholder="Enter particulars"),
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
                        type="text", id='amount-input', placeholder="0,000.00"
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
                       id='status-select',
                       options=[
                           {"label": "Approved", "value": "Approved"},
                           {"label": "Pending", "value": "Pending"},
                           {"label": "Denied", "value": "Denied"},
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
                        type="text", id='bur-no-input', placeholder="0000-00-00000"
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
                        "Submitted by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4
                ),
               dbc.Col(
                   dbc.Input(type="text", id='submitted-by-input', placeholder="First Name Last Name"),
                   width=8,
               ),
           ],
           className="mb-3",
       ),

        dbc.Row(
                dbc.Col(
                    dcc.Upload(
                        id='upload-receipt',
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
               dbc.Col(dbc.Button("Save", id="submit-button", color="primary", className="me-3", style={"font-weight": "bold", "font-size": "18px"}), width={"size": 2, "offset": 4}),
               dbc.Col(dbc.Button("Clear", color="secondary", style={"font-weight": "bold", "font-size": "18px"}), width={"size": 2}),
           ],
           className="mb-4",
       ),
   ],
   className="g-2",
)

#Expense Type Dropdowns
@app.callback(
   Output('expense-sub-type-dropdown', 'options'),
   Input('expense-main-type-dropdown', 'value')
)
def set_sub_expense_options(selected_main_type):
   if not selected_main_type:
       # If no main type is selected, return an empty list of options
       return []
   return [{"label": sub, "value": sub} for sub in sub_expense_types[selected_main_type]]

#Amount
@app.callback(
   Output('amount-input', 'value'),
   Input('amount-input', 'value')
)
def format_amount(amount):
   if not amount or amount == '.':
       return ''
  
   # Filter out invalid characters
   cleaned_amount = ''.join([c for c in amount if c.isdigit() or c == '.'])


   # Split into whole and decimal parts
   parts = cleaned_amount.split('.')
   whole_part = parts[0]


   # Format whole part with commas
   formatted_whole = format(int(whole_part) if whole_part else 0, ',d')


   # Reconstruct the amount
   if len(parts) > 1:
       decimal_part = parts[1][:2]  # Take at most two decimal places
       formatted_amount = f'{formatted_whole}.{decimal_part}'
   else:
       formatted_amount = formatted_whole


   return formatted_amount

#BUR No
@app.callback(
   Output('bur-no-input', 'value'),
   Input('bur-no-input', 'value')
)
def format_bur_no(bur_no):
   if not bur_no:
       return ''
  
   # Remove non-numeric characters
   bur_no = ''.join(filter(str.isdigit, bur_no))


   # Add dashes at appropriate positions
   formatted_bur_no = ''
   for i, char in enumerate(bur_no):
       if i == 4 or i == 6:
           formatted_bur_no += '-'
       formatted_bur_no += char


   return formatted_bur_no[:13]  # Limit the length to fit the pattern

#Upload file
@app.callback(
    Output('output-upload', 'children'),
    Input('upload-receipt', 'contents'),
    State('upload-receipt', 'filename'),
    State('upload-receipt', 'last_modified')
)
def update_output(uploaded_files_contents, uploaded_files_names, uploaded_files_dates):
    if uploaded_files_contents is not None:
        children = [
            html.Div(f"{filename} uploaded successfully.")
            for filename in uploaded_files_names
        ]
        return children

#Save button
@app.callback(
    Output('save-button', 'disabled'),
    [
        Input('date-input', 'date'),
        Input('payee-input', 'value'),
        Input('expense-main-type-dropdown', 'value'),
        Input('expense-sub-type-dropdown', 'value'),
        Input('particulars-input', 'value'),
        Input('amount-input', 'value'),
        Input('status-select', 'value'),
        Input('bur-no-input', 'value'),
        Input('submitted-by-input', 'value'),
        Input('upload-receipt', 'contents'),
    ]
)
def toggle_save_button(date, payee, main_type, sub_type, particulars, amount, status, bur_no, submitted_by, upload):
    # Check if all fields are filled out
    if all([date, payee, main_type, sub_type, particulars, amount, status, bur_no, submitted_by, upload]):
        return False  # All fields are filled, button is enabled
    return True  # Not all fields are filled, button remains disabled







layout = html.Div(
   [
       dbc.Row(
           [
               #navbar
               dbc.Col(
                   cm.generate_navbar(),
                   width=2
               ),


               #title
               dbc.Col(
               [
                   html.H1("ADD EXPENSE"),
                   html.Hr(),


                   #working form
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

