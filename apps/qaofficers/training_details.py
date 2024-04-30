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

import datetime
current_year = datetime.datetime.now().year








form = dbc.Form(
    [ 
        dbc.Row(
            [
                dbc.Label("QA Officer Name", 
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id="qatr_officername",
                        placeholder="Select QA Officer",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Year", 
                    width=4),
                dbc.Col(
                    dbc.Input(id="qatr_training_year", 
                        type="number",
                        value=current_year),
                    width=3,
                    
                ),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Name of Training", 
                    width=4),
                dbc.Col(
                    dbc.Input(id="qatr_training_name", type="text"),
                    width=6,
                ),
                  
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("Training Type", 
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id="qatr_training_type",
                        placeholder="Select Training Type",
                    ),
                    width=6,
                ),
                  
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label("Add new training type",
                    width=4),
                dbc.Col(
                    dbc.Input(id="new_training_type", type="text"),
                    width=5,
                ),
                dbc.Col(
                    dbc.Button("+", color="primary", id="add_button",
                            n_clicks=0,
                            style={"font-weight": "bold"},
                    ),
                    width="auto",
                ),
            ],
            className="mb-1",
        ),
 
        html.Br(),
         
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Register", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
            ],
            className="mb-2",
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4('Training added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                       "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='qatr_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(html.H4("New training type added.")),
            ],
            centered=True,
            id="newtype_successmodal",
            is_open=False,
            backdrop=True,
            className="modal-success",
        )
         
    ]
)



  






# QA Officer name dropdown
@app.callback(
    Output('qatr_officername', 'options'),
    Input('url', 'pathname')
)
def populate_qaofficername_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/QAOfficers/addtraining':
        sql = """
        SELECT qaofficer_full_name as label, qaofficer_full_name as value
        FROM  qaofficers.qa_officer
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficername = df.to_dict('records')
        return qaofficername
    else:
        raise PreventUpdate



# QA Officer name dropdown
@app.callback(
    Output('qatr_training_type', 'options'),
    Input('url', 'pathname')
)
def populate_qaofficername_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/QAOfficers/addtraining':
        sql = """
        SELECT trainingtype_name as label, trainingtype_id as value
        FROM  qaofficers.training_type
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        qaofficername = df.to_dict('records')
        return qaofficername
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
                        html.H1("ADD TRAINING"),
                        html.Hr(),
                        dbc.Alert(id='qatr_alert', is_open=False), # For feedback purpose
                        form, 
                        
                        
                        
                        html.Hr(),
                        html.H4("TRAINING LIST"),
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    id="training_details_output",  # ID for updating the section
                                    children="Select a QA officer to view their training details.",
                                ),
                                width=12,
                            ),
                            className="mb-3",
                        ),
                         
                        
                    ], width=8, style={'marginLeft': '15px'}
                ),   
            ]
        ),
        

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
        Output('qatr_alert', 'color'),
        Output('qatr_alert', 'children'),
        Output('qatr_alert', 'is_open'),
        Output('qatr_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('qatr_officername', 'value'),
        State('qatr_training_year', 'value'), 
        State('qatr_training_name', 'value'),
        State('qatr_training_type', 'value') 
    ]
)
 
def record_program_details (submitbtn, qatr_officername, qatr_training_year,
                            qatr_training_name, qatr_training_type):
    if not submitbtn:
        raise PreventUpdate

    alert_open = True  # Set alert_open to True by default
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not qatr_officername:
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add an Officer name.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
    
    if not qatr_training_year :
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Training Year.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
    
    if not qatr_training_name :
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Training Name.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
     
    if not qatr_training_type :
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Training Type.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
     
    try:
        sql = """
            INSERT INTO qaofficers.qa_training_details (
                qatr_officername, qatr_training_year,
                qatr_training_name, qatr_training_type
            )
            VALUES (%s, %s, %s, %s)
        """
        values = (
            qatr_officername, qatr_training_year,
            qatr_training_name, qatr_training_type
        )
 

        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'

    return [alert_color, alert_text, alert_open, modal_open]

  



# Callback to add a new training type and display the success modal
@app.callback(
    Output("newtype_successmodal", "is_open"),
    [Input("add_button", "n_clicks")],
    [State("new_training_type", "value")],
)
def add_new_training_type(n_clicks, new_training_type):
    if n_clicks == 0 or not new_training_type:
        raise PreventUpdate  # No action required

    modal_open = False

    try:
        sql = """
            INSERT INTO qaofficers.training_type (trainingtype_name)
            VALUES (%s)
        """
        values = (new_training_type,)
        db.modifydatabase(sql, values)  # Function to execute the SQL and commit changes
        modal_open = True  # Open the success modal
    except Exception as e:
        print(f"Error occurred: {e}")  # Log the error
        modal_open = False

    return modal_open




@app.callback(
    Output("training_details_output", "children"),
    [Input("qatr_officername", "value")],
)
def fetch_training_details(qatr_officername):
    if not qatr_officername:
        raise PreventUpdate
    
    try:
        sql = """
            SELECT 
                qatr_training_year AS "Year",
                qatr_training_name AS "Name",
                tt.trainingtype_name AS "Type"
            FROM 
                qaofficers.qa_training_details qtd
            INNER JOIN 
                qaofficers.training_type tt
            ON 
                qtd.qatr_training_type = tt.trainingtype_id
            WHERE 
                qatr_officername = %s
        """
        # Correct function call and appropriate arguments
        results = db.querydatafromdatabase(sql, (qatr_officername,), ["Year", "Name", "Type"])
        
        if results.empty:
            return "No training details found for this QA officer."

        training_list = [
            f"Year: {row['Year']}, Training Name: {row['Name']}, Type: {row['Type']}"
            for _, row in results.iterrows()
        ]

        return html.Ul([html.Li(item) for item in training_list])

    except Exception as e:
        return f"An error occurred while retrieving the training details: {e}"