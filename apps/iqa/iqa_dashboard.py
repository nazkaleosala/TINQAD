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
from datetime import datetime

# Define interval time (in milliseconds) for auto-updates
interval_time = 1000  # 1 second

# Function to fetch the total count from the database for Academic Unit Heads
def get_total_count_acad_unitheads():
    sql = "SELECT COUNT(*) FROM iqateam.acad_unitheads  WHERE unithead_del_ind = False"
    total_count = db.query_single_value(sql)
    return total_count

# Function to fetch the total count from the database for QA Officers
def get_total_count_qa_officers():
    sql = "SELECT COUNT(*) FROM qaofficers.qa_officer WHERE qaofficer_del_ind = False"
    total_count = db.query_single_value(sql)
    return total_count

# Function to generate Academic Unit Heads card
def generate_acadhead_card():
    # Get the total count from the database for Academic Unit Heads
    total_count = get_total_count_acad_unitheads()
    
    # SQL query to fetch college names and count of terms expiring in the next 2 months
    sql = """
    SELECT c.college_name AS college,
           COUNT(*) AS term_expiry
    FROM iqateam.acad_unitheads a
    JOIN public.college c ON a.unithead_college_id = c.college_id
    WHERE a.unithead_appointment_end < CURRENT_DATE + INTERVAL '2 months'
      
    GROUP BY a.unithead_college_id, c.college_name;
    """
    # Execute the query and fetch data
    data = db.querydatafromdatabase(sql, [], ['college', 'term_expiry'])
    
    # Generate card layout
    card = dbc.Card(
        [
            dbc.CardHeader(html.H3("Academic Unit Heads")), 
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Strong("Total =", style={"margin-right": "3px", "margin-top": "7px"}),
                                width=1
                            ),
                            dbc.Col(
                                html.Span(total_count, style={"font-weight": "bold"}),
                                width=1,
                                style={
                                    "backgroundColor": "#A9CD46",
                                    "borderRadius": "10px",
                                    "padding": "5px",
                                    "textAlign": "center",
                                    "marginLeft": "-10px" 
                                }
                            ),
                            
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.A(
                                    dbc.Button("More details..", color="link"),
                                    href="/dashboard/more_details",
                                    style={"text-align": "right"}
                                ),
                                width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dash_table.DataTable(
                                    id='acad_unitheads_table',
                                    columns=[
                                        {'name': 'College', 'id': 'college'},
                                        {'name': 'Term Expiring in the Next 2 Months', 'id': 'term_expiry'}
                                    ],
                                    data=data.to_dict('records'),
                                    style_cell={
                                        'fontFamily': 'Arial', 
                                        'fontSize': '14px',
                                    },
                                    style_header={
                                        'fontWeight': 'bold',
                                        'textAlign': 'center',
                                    },
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': 'college'},
                                            'textAlign': 'left',
                                            'paddingLeft': '15px'
                                        },
                                        {
                                            'if': {'column_id': 'term_expiry'},
                                            'textAlign': 'center'
                                        }
                                    ],
                                    style_table={'overflowX': 'auto'}
                                ),
                                width=12
                            )
                        ]
                    ),
                    html.Br()
                ],
                className="mb-3",
                style={'overflowY': 'scroll'}  # Align items vertically in the body
            )
        ],
        style={'minHeight': '100px','maxHeight': '300px', 'overflowY': 'scroll'}
    )
    return card

# Function to generate QA Officers card
def generate_qaofficers_card():
    # SQL query to fetch data for the QA Officers table
    sql = """
    SELECT c.college_name AS college,
           COUNT(*) AS qa_officers,
           SUM(CASE WHEN qaofficer_basicpaper = 'Yes' THEN 1 ELSE 0 END) AS approved_papers,
           SUM(CASE WHEN qaofficer_remarks = 'For renewal' THEN 1 ELSE 0 END) AS renewal,
           SUM(CASE WHEN qaofficer_remarks = 'No record' THEN 1 ELSE 0 END) AS no_record,
           SUM(CASE WHEN qaofficer_appointment_end < CURRENT_DATE + INTERVAL '2 months' THEN 1 ELSE 0 END) AS expiring
    FROM qaofficers.qa_officer q
    JOIN public.college c ON q.qaofficer_college_id = c.college_id
    WHERE q.qaofficer_del_ind = False
    GROUP BY q.qaofficer_college_id, c.college_name;

    """
    # Execute the query and fetch data
    data = db.querydatafromdatabase(sql, [], ['college', 'qa_officers', 'approved_papers',  'renewal', 'no_record', 'expiring'])
    
    # Generate card layout
    card = dbc.Card(
        [
            dbc.CardHeader(html.H3("QA Officers")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Strong("Total =", style={"margin-right": "3px", "margin-top": "7px"}),
                                width=1
                            ),
                            dbc.Col(
                                html.Span(get_total_count_qa_officers(), style={"font-weight": "bold"}),
                                width=1,
                                style={
                                    "backgroundColor": "#A9CD46",
                                    "borderRadius": "10px",
                                    "padding": "5px",
                                    "textAlign": "center",
                                    "marginLeft": "-10px" 
                                }
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.A(
                                    dbc.Button("More details..", color="link"),
                                    href="/dashboard/more_details",
                                    style={"text-align": "right"}
                                ),
                                width={"size": 2, "offset": 10}  # Adjust width and offset for alignment
                            ),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dash_table.DataTable(
                                    id='qa_officers_table',
                                    columns=[
                                        {'name': 'College', 'id': 'college'},
                                        {'name': 'No. of QA Officers', 'id': 'qa_officers'},
                                        {'name': 'With Approved Basic Papers', 'id': 'approved_papers'},
                                        {'name': 'Term For Renewal', 'id': 'renewal'},
                                        {'name': 'No Record', 'id': 'no_record'},
                                        {'name': 'Term Expiring in the Next 2 Months', 'id': 'expiring'}
                                    ],
                                    data=data.to_dict('records'),
                                    style_cell={
                                        'fontFamily': 'Arial', 
                                        'fontSize': '14px',
                                        'width': '120px',  
                                        'whiteSpace': 'normal', 
                                        'overflow': 'hidden',  
                                        'textOverflow': 'ellipsis' 
                                    },
                                    style_header={
                                        'fontWeight': 'bold',
                                        'textAlign': 'center',
                                        'height': '50px'
                                    },
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': 'college'},
                                            'textAlign': 'left',
                                            'paddingLeft': '15px',
                                            'width': '300px'
                                        },
                                        {
                                            'if': {'column_id': 'qa_officers'},
                                            'textAlign': 'center'
                                        },
                                        {
                                            'if': {'column_id': 'approved_papers'},
                                            'textAlign': 'center'
                                        },
                                        {
                                            'if': {'column_id': 'renewal'},
                                            'textAlign': 'center'
                                        },
                                        {
                                            'if': {'column_id': 'no_record'},
                                            'textAlign': 'center'
                                        },
                                        {
                                            'if': {'column_id': 'expiring'},
                                            'textAlign': 'center'
                                        },
                                    ],
                                    style_table={'overflowX': 'auto'}
                                ),
                                width=12
                            )
                        ]
                    ),
                    html.Br()
                ],
                className="mb-3",
                style={'overflowY': 'scroll'}  # Align items vertically in the body
            )
        ],
        style={'minHeight': '100px', 'maxHeight': '300px', 'overflowY': 'scroll'}
    )
    return card

# Define layout
layout = html.Div(
    [
        dcc.Interval(id='interval-component', interval=interval_time, n_intervals=0),  # Interval component for auto-updates
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
                                dbc.Col(generate_acadhead_card(), width=12),
                            ]
                        ),

                        html.Br(),

                        dbc.Row(
                            [
                                dbc.Col(generate_qaofficers_card(), width=12),
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

# Callback function to update the content of the cards
@app.callback(
    Output('acad_unitheads_table', 'data'),
    Output('qa_officers_table', 'data'),
    Input('interval-component', 'n_intervals')
)
def update_cards(n):
    # SQL query to fetch data for Academic Unit Heads
    acad_sql = """
    SELECT c.college_name AS college,
           COUNT(*) AS term_expiry
    FROM iqateam.acad_unitheads a
    JOIN public.college c ON a.unithead_college_id = c.college_id
    WHERE a.unithead_appointment_end < CURRENT_DATE + INTERVAL '2 months'
      AND a.unithead_del_ind = False
    GROUP BY a.unithead_college_id, c.college_name;
    """
    # SQL query to fetch data for QA Officers
    qa_sql = """
    SELECT c.college_name AS college,
           COUNT(*) AS qa_officers,
           SUM(CASE WHEN qaofficer_basicpaper = 'Yes' THEN 1 ELSE 0 END) AS approved_papers,
           SUM(CASE WHEN qaofficer_remarks = 'For renewal' THEN 1 ELSE 0 END) AS renewal,
           SUM(CASE WHEN qaofficer_remarks = 'No record' THEN 1 ELSE 0 END) AS no_record,
           SUM(CASE WHEN qaofficer_appointment_end < CURRENT_DATE + INTERVAL '2 months' THEN 1 ELSE 0 END) AS expiring,
    FROM qaofficers.qa_officer q
    JOIN public.college c ON q.qaofficer_college_id = c.college_id
    WHERE q.qaofficer_del_ind = False

    GROUP BY q.qaofficer_college_id, c.college_name;
    """
    # Execute the queries and fetch data
    acad_data = db.querydatafromdatabase(acad_sql, [], ['college', 'term_expiry'])
    qa_data = db.querydatafromdatabase(qa_sql, [], ['college', 'qa_officers', 'approved_papers', 'renewal', 'no_record', 'expiring'])
    
    return acad_data.to_dict('records'), qa_data.to_dict('records')
