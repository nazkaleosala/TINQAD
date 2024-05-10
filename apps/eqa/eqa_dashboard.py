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

import plotly.graph_objs as go


def generate_donut_chart(labels, values):
    # Define color scale for the pie chart
    colors = ['#F8B237', '#E4E4E4', '#39B54A']
    trace = go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))
    return {'data': [trace], 'layout': go.Layout(title='', showlegend=False)}

def generate_assessment_schedule_card():
    sql = """
        SELECT 
            dp.degree_name AS program_name, 
            ae.approv_eqa_name AS assessment_type, 
            sr.sarep_sched_assessdate AS assessment_sched_date
        FROM eqateam.sar_report sr
        JOIN public.degree_programs dp 
        ON sr.sarep_degree_programs_id = dp.degree_id
        JOIN eqateam.approv_eqa ae 
        ON sr.sarep_approv_eqa = ae.approv_eqa_id
        """
    assessmentsched_data = db.querydatafromdatabase(sql, [], ['program_name', 'assessment_type', 'assessment_sched_date'])
    
    # Add index to data
    assessmentsched_data['index'] = range(1, len(assessmentsched_data) + 1)
    
    card = dbc.Card(
        [
            dbc.CardHeader(html.H3("Assessment Schedule")),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(                
                                dash_table.DataTable(
                                    id='ass-sched-table',
                                    columns=[
                                        {'name': 'Index', 'id': 'index'},
                                        {'name': 'Program Name', 'id': 'program_name'},
                                        {'name': 'Type of Assessment', 'id': 'assessment_type'},
                                        {'name': 'Scheduled Assessment Date', 'id': 'assessment_sched_date'}
                                    ],
                                    data=assessmentsched_data.to_dict('records'),
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
                        html.H1("EQA DASHBOARD"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("Summary of Degree Programs with EQA"),  # Bold only this part
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}  # Adjust font size
                                                )
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.P("40/100 programs assessed", className="card-text"),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dcc.Graph(id='donut-chart')
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#F8B237', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are currently accomplishing their accreditation", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#39B54A', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are on schedule for next accreditation", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#E4E4E4', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are yet to commence accreditation requirements", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    
                                                ]
                                            ),
                                        ]
                                    ),
                                    width=8,
                                    className="mb-3"
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("SAR Submissions 2024"),  # Bold only this part
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}  # Adjust font size
                                                )
                                            ),
                                            dbc.CardBody(),
                                        ]
                                    ),
                                    width=4
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(generate_assessment_schedule_card(), width=12)
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
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
    Output('donut-chart', 'figure'),
    [Input('donut-chart', 'id')]
)
def update_donut_chart(id):
    # Fetch data from the database
    sql = """
    SELECT sarep_checkstatus
    FROM eqateam.sar_report
    """
    df = db.querydatafromdatabase(sql, [], ['sarep_checkstatus'])

    # Calculate counts for different statuses
    for_checking_count = df[df['sarep_checkstatus'] == 'For Checking'].shape[0]
    already_checked_count = df[df['sarep_checkstatus'] == 'Already Checked'].shape[0]
    null_count = df['sarep_checkstatus'].isnull().sum()

    # Generate labels and values for the donut chart
    labels = ['For Checking', 'Already Checked', 'No Status Yet']
    values = [for_checking_count, already_checked_count, null_count]

    # Return the updated donut chart
    return generate_donut_chart(labels, values)
