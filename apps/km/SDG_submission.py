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
import json

 



  


# Form layout with improvements
form = dbc.Form(
    [
        # SDG Number Selector
        dbc.Row(
            [
                dbc.Label(
                    ["Ranking Body", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Select(
                        id='sdg_rankingbody', 
                        value="THE World Rankings"
                    ),
                    width=8,
                ), 
            ],
            className="mb-1",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Evidence Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_evidencename",  placeholder="Enter Evidence Name"),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Description ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Textarea(id="sdg_description",placeholder="Enter Description"),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        html.P("Please pick either Office OR a Department", style={"color": "red"}),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Office ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_office_id', 
                    ),
                    width=5,
                ),
                 
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Department",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Dropdown(
                        id='sdg_deg_unit_id', 
                    ),
                    width=5,
                ),
                 
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Accomplished By ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text", id="sdg_accomplishedby", placeholder="Name Surname" ),  # Pre-filled as per image
                    width=5,
                ),
            ],
            className="mb-3",
        ),
         
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
                        id='sdg_datesubmitted',
                        date=str(pd.to_datetime("today").date()),  # Today's date by default 
                        clearable=True,
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),

          

        dbc.Row(
            [
                dbc.Label(
                    [
                        "File Submissions ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dcc.Upload(id="sdg_file", 
                        children=html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url('icons/add_file.png'),
                                    style={'height': '15px', 'marginRight': '5px'}
                                ),
                                "add file"
                            ],
                            style={'display': 'flex', 'alignItems': 'center'}
                        ),
                        style={
                            'width': '100%', 'minHeight': '30px',  # Adjust height as needed
                            'borderWidth': '1px', 'borderStyle': 'solid',
                            'borderRadius': '5px', 'textAlign': 'center',
                            'margin': '5px', 'display': 'flex',
                            'alignItems': 'center', 'justifyContent': 'center'
                        },
                               
                        
                    
                    multiple=True
                    ),
                    width=5, 
                ),
            ],
            className="mb-3",
        ),
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link Submissions ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(type="text",id="sdg_link", placeholder="Enter Link"),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Add Applicable Criteria ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Checklist(
                        id="sdg_applycriteria", 
                        value=[],  # Initial empty value, can be pre-filled if desired
                        inline=True
                    ),
                    width=5,
                ),
            ],
            className="mb-3",
        ),
        
        # Cancel and Save Buttons
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Button("Submit for checking", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto",
                ),
            ],
            className="mb-2",
            justify="end",
        ),

        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4("Criteria added."),
                ),
                dbc.ModalFooter(
                    dbc.Button("Proceed", id="proceed_button", className="ml-auto"),
                ),
            ],
            centered=True,
            id="sdgsubmission_successmodal",
            backdrop=True,
            className="modal-success",
        ),
    ],
    className="g-2",
)


 
#rankingbody  dropdown
@app.callback(
    Output('sdg_rankingbody', 'options'),
    Input('url', 'pathname')
)
def populate_rankingbody_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT ranking_body_name as label, ranking_body_id  as value
        FROM kmteam.ranking_body
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        rankingbody_types = df.to_dict('records')
        return rankingbody_types
    else:
        raise PreventUpdate




#office dropdown
@app.callback(
    Output('sdg_office_id', 'options'),
    Input('url', 'pathname')
)
def populate_office_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT office_name as label, office_id as value
        FROM maindashboard.offices
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        office_types = df.to_dict('records')
        return office_types
    else:
        raise PreventUpdate




#depts dropdown
@app.callback(
    Output('sdg_deg_unit_id', 'options'),
    Input('url', 'pathname')
)
def populate_depts_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT deg_unit_name as label, deg_unit_id as value
        FROM  public.deg_unit
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        depts_types = df.to_dict('records')
        return depts_types
    else:
        raise PreventUpdate
 

#sdg criteria checklist
@app.callback(
    Output('sdg_applycriteria', 'options'),
    Input('url', 'pathname')
)
def populate_applycriteria_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpactrankings/SDG_submission':
        sql = """
        SELECT sdgcriteria_code as label, sdgcriteria_id   as value
        FROM kmteam.SDGCriteria
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        applycriteria_types = df.to_dict('records')
        return applycriteria_types
    else:
        raise PreventUpdate




# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("ADD NEW SDG SUBMISSION"),
                        html.Hr(),
                        html.Br(),
                        form,
                        dbc.Alert(id="sdgsubmission_alert", is_open=False),  # Alert for feedback
                    ],
                    width=6,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(),
                    width={"size": 12, "offset": 0},
                ),
            ],
        ),
    ]
)
 
@app.callback(
    [
        Output('sdgsubmission_alert', 'color'),
        Output('sdgsubmission_alert', 'children'),
        Output('sdgsubmission_alert', 'is_open'),
        Output('sdgsubmission_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('sdg_rankingbody', 'value'),
        State('sdg_evidencename', 'value'),
        State('sdg_description', 'value'),
        State('sdg_office_id', 'value'),
        State('sdg_deg_unit_id', 'value'),
        State('sdg_accomplishedby', 'value'),
        State('sdg_datesubmitted', 'value'),  
        State('sdg_file', 'value'),
        State('sdg_link', 'value'), 
        State('sdg_applycriteria', 'value'), 
    ]
) 




def record_SDGsubmission (submitbtn, sdg_rankingbody, sdg_evidencename,
                          sdg_description,sdg_office_id,sdg_deg_unit_id,
                          sdg_accomplishedby,sdg_datesubmitted,
                          sdg_file,sdg_link, sdg_applycriteria):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    # Input validation checks
    if not sdg_rankingbody:
        alert_open = True
        alert_color = 'danger'
        alert_text = 'Check your inputs. Please add a Ranking Body.'
        return [alert_color, alert_text, alert_open, modal_open]


    try:
        sql = """
            INSERT INTO kmteam.SDGSubmission (
                sdg_rankingbody, sdg_evidencename,
                sdg_description, sdg_office_id, sdg_deg_unit_id,
                sdg_accomplishedby, sdg_datesubmitted,
                sdg_file, sdg_link, sdg_applycriteria
            )
        
        VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        # Values for insertion
        values = (
            sdg_rankingbody,
            sdg_evidencename,
            sdg_description,   
            sdg_office_id,     
            sdg_deg_unit_id,   
            sdg_accomplishedby,
            sdg_datesubmitted,   
            sdg_file,           
            sdg_link,         
            json.dumps(sdg_applycriteria) if sdg_applycriteria else None  # JSONB handling
        )


        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'
        alert_open = True

    return [alert_color, alert_text, alert_open, modal_open]
