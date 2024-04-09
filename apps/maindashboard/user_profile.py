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
from calendar import month_name



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





# Generate month options as words
month_options = [{'label': month, 'value': str(index)} for index, month in enumerate(month_name) if index != 0]



form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("First Name", width=4),
                dbc.Col(dbc.Input(type="text"  ), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Middle Initial", width=4),
                dbc.Col(dbc.Input(type="text"), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Surname", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("ID Number", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
            ],
            className="mb-2",
        ), 
        dbc.Row(
            [
                dbc.Label("Lived Name", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
            ],
            className="mb-2", 
        ),
        dbc.Row(
            [
                dbc.Label("Sex Assigned at Birth", width=4),
                dbc.Col(
                    dbc.Select(
                        options=[
                            {"label": "Female", "value": "F"},
                            {"label": "Male", "value": "M"},
                             
                        ], 
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Birthday", width=4),
                dbc.Col(dbc.Input(type="text" ), width=8),
            ],
            className="mb-2", 
        ),

        dbc.Row(
               [
                dbc.Label( "Phone Number ", width=4),
                dbc.Col(
                    dbc.Input(
                        type="text", id='phone-no-input', placeholder="0000-00-00000"
                    ),
                    width=8,
                ),
            ],
            className="mb-3",
        ),
       
        dbc.Row(
            [
                dbc.Label("Office/Department", width=4),
                dbc.Col(dbc.Input(type="text"  ), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Position", width=4),
                dbc.Col(dbc.Input(type="text"  ), width=8),
            ],
            className="mb-2",
        ),
        
         
        
        dbc.Row(
            [
                dbc.Label("Email Address (primary)", width=4),
                dbc.Col(dbc.Input(type="text"), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Present Housing", width=4),
                dbc.Col(dbc.Input(type="text"), width=8),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Save", color="primary", className="me-3"),  
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary"), 
                    width="auto"
                ),
            ],
            className="mb-2",
        )
        
    ],
    className="g-2",
)

  

#phone-no  format:
@app.callback(
   Output('phone-no-input', 'value'),
   Input('phone-no-input', 'value')
)
def format_phone_no(phone_no):
   if not phone_no:
       return ''
  
   # Remove non-numeric characters
   bur_no = ''.join(filter(str.isdigit, bur_no))


   # Add dashes at appropriate positions
   formatted_phone_no = ''
   for i, char in enumerate(bur_no):
       if i == 4 or i == 6:
           formatted_phone_no += '-'
       formatted_phone_no += char


   return formatted_phone_no[:13]  # Limit the length to fit the pattern





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
                
                    width=8, 
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