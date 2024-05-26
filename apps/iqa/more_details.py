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
from datetime import datetime, timedelta

# Function to fetch the data from the database for Academic Unit Heads Tracker
def generate_acadhead_tracker_card():
    # Calculate the date 2 months from now
    two_months_from_now = datetime.now() + timedelta(days=60)
    # SQL query to fetch data from the database
    sql = f"""
    SELECT c.cluster_shortname AS cluster,
           cl.college_shortname AS academic_unit,
           du.deg_unit_shortname AS degree_granting_unit,
           a.unithead_full_name AS name,
           a.unithead_upmail AS up_mail,
           a.unithead_appointment_end AS end_of_term
    FROM iqateam.acad_unitheads a
    JOIN public.clusters c ON a.unithead_cluster_id = c.cluster_id
    JOIN public.college cl ON a.unithead_college_id = cl.college_id
    JOIN public.deg_unit du ON a.unithead_deg_unit_id = du.deg_unit_id
    WHERE a.unithead_appointment_end <= '{two_months_from_now}'
        AND a.unithead_del_ind = False
    ;
    """
    # Execute the query and fetch data
    acadheads_data = db.querydatafromdatabase(sql, [], ['cluster', 'academic_unit', 'degree_granting_unit', 'name', 'up_mail', 'end_of_term'])
    
    # Add index to data
    acadheads_data['Index'] = range(1, len(acadheads_data) + 1)

    # Calculate the number of days left
    acadheads_data['days_left'] = (pd.to_datetime(acadheads_data['end_of_term']) - pd.Timestamp.now()).dt.days

    # Generate card layout
    card = dbc.Card(
        [
            dbc.CardHeader(html.H3("Academic Unit Heads Tracker")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(                
                                dash_table.DataTable(
                                    id='acad-unit-table',
                                    columns=[
                                        {'name': 'Index', 'id': 'Index'},
                                        {'name': 'Cluster', 'id': 'cluster'},
                                        {'name': 'Academic Unit', 'id': 'academic_unit'},
                                        {'name': 'Degree Granting Unit', 'id': 'degree_granting_unit'},
                                        {'name': 'Name', 'id': 'name'},
                                        {'name': 'UP Mail', 'id': 'up_mail'},
                                        {'name': 'End of Term', 'id': 'end_of_term'},
                                        {'name': 'Days Left', 'id': 'days_left'}
                                    ],
                                    data=acadheads_data.to_dict('records'),
                                    style_cell={
                                        'fontFamily': 'Arial', 
                                        'fontSize': '14px',
                                        'textAlign': 'left', 
                                        'whiteSpace': 'normal',
                                        'paddingLeft': '15px', 
                                        'overflow': 'hidden',  
                                        'textOverflow': 'ellipsis' 
                                    },
                                    style_header={
                                        'fontWeight': 'bold',
                                        'textAlign': 'center',
                                        'paddingLeft': '-15px',
                                        'height': '50px'
                                    },
                                    style_table={'overflowX': 'auto', 'maxWidth': '100%'},
                                    style_data_conditional=[
                                        {
                                            'if': {'column_id': 'index', 'column_id': 'days_left'},
                                            'textAlign': 'center',
                                            'paddingLeft': '-15px',
                                        }
                                    ]
                                ),
                                width=12
                            )
                        ]
                    ),
                    html.Br(),
                ],
                className="mb-3",
                style={'overflowY': 'scroll'}  # Align items vertically in the body
            ),
            dbc.CardFooter(id='acadhead-row-count')
        ],
        style={'minHeight': '100px','maxHeight': '400px', 'overflowY': 'scroll'}
    )
    return card

# Generate card layout for QA Officers Tracker
def generate_qaofficers_card():
    # SQL query to fetch data from the database
    sql = """
    SELECT 
        c.cluster_shortname AS cluster,
        cl.college_shortname AS academic_unit,
        du.deg_unit_shortname AS degree_granting_unit,
        q.qaofficer_full_name AS name,
        q.qaofficer_upmail AS up_mail,
        q.qaofficer_appointment_end AS end_of_term,
        q.qaofficer_remarks AS status
    FROM qaofficers.qa_officer q
    JOIN public.clusters c ON q.qaofficer_cluster_id = c.cluster_id
    JOIN public.college cl ON q.qaofficer_college_id = cl.college_id
    JOIN public.deg_unit du ON q.qaofficer_deg_unit_id = du.deg_unit_id
    WHERE q.qaofficer_del_ind = False
    ;
    """
    # Execute the query and fetch data
    qaofficers_data = db.querydatafromdatabase(sql, [], ['cluster', 'academic_unit', 'degree_granting_unit', 'name', 'up_mail', 'end_of_term', 'status'])

    # Generate index for each row
    qaofficers_data['Index'] = range(1, len(qaofficers_data) + 1)

    # Generate card layout
    card = dbc.Card(
        [
            dbc.CardHeader(html.H3("QA Officers Tracker")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(  
                                dash_table.DataTable(
                                    id='qa-officer-table',
                                    columns=[
                                        {'name': 'Index', 'id': 'index'},
                                        {'name': 'Cluster', 'id': 'cluster'},
                                        {'name': 'Academic Unit', 'id': 'academic_unit'},
                                        {'name': 'Degree Granting Unit', 'id': 'degree_granting_unit'},
                                        {'name': 'Name', 'id': 'name'},
                                        {'name': 'UP Mail', 'id': 'up_mail'},
                                        {'name': 'End of Term', 'id': 'end_of_term'},
                                        {'name': 'Status', 'id': 'status'}
                                    ],
                                    data=qaofficers_data.to_dict('records'),
                                    style_cell={
                                        'fontFamily': 'Arial', 
                                        'fontSize': '14px',
                                        'textAlign': 'left',  
                                        'paddingLeft': '15px',
                                        'whiteSpace': 'normal',  
                                        'overflow': 'hidden',  
                                        'textOverflow': 'ellipsis' 
                                    },
                                    style_header={
                                        'fontWeight': 'bold',
                                        'textAlign': 'center',
                                        'paddingLeft': '-15px',
                                        'height': '50px'
                                    },
                                    style_table={'overflowX': 'auto', 'maxWidth': '100%'},
                                    style_data_conditional=[
                                        {
                                            'if': {'column_id': 'status', 'column_id': 'index'},
                                            'textAlign': 'center',
                                            'paddingLeft': '-15px',
                                        }
                                    ]
                                ),
                                width=12
                            )
                        ]
                    ),
                    html.Br(),
                ],
                className="mb-3",
                style={'overflowY': 'scroll'}  # Align items vertically in the body
            ),
            dbc.CardFooter(id='qaofficers-row-count')
        ],
        style={'minHeight': '100px','maxHeight': '400px', 'overflowY': 'scroll'}
    )
    return card

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
                        html.H1("IQA DASHBOARD"),
                        html.Hr(),

                        dbc.Row(
                            [
                                dbc.Col(generate_acadhead_tracker_card(), width=12)
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(generate_qaofficers_card(), width=12)
                            ]
                        ), 

                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
                html.Br()
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)

# Callbacks to update row count dynamically
@app.callback(
    Output('acadhead-row-count', 'children'),
    [Input('acad-unit-table', 'data')]
)
def update_acadhead_row_count(acadheads_data):
    return f"Row Count: {len(acadheads_data)}"

@app.callback(
    Output('qaofficers-row-count', 'children'),
    [Input('qa-officer-table', 'data')]
)
def update_qaofficers_row_count(qaofficers_data):
    return f"Row Count: {len(qaofficers_data)}"
