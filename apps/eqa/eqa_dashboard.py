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


def get_total_checked():
    sql = "SELECT COUNT(*) FROM eqateam.sar_report WHERE sarep_checkstatus = 'Already Checked'"
    total_count = db.query_single_value(sql)
    return total_count

def get_total_ongoing():
    sql = "SELECT COUNT(*) FROM eqateam.sar_report WHERE sarep_checkstatus = 'For Checking'"
    total_count = db.query_single_value(sql)
    return total_count

def get_total_unchecked():
    sql = "SELECT COUNT(*) FROM eqateam.sar_report"
    sar_total_count = db.query_single_value(sql)

    sql = "SELECT COUNT(*) FROM eqateam.program_details"
    prog_total_count = db.query_single_value(sql)

    difference = prog_total_count - sar_total_count
    
    return difference


def generate_donut_chart():
    # Call the functions to get the counts
    checked_count = get_total_checked()
    ongoing_count = get_total_ongoing()
    unchecked_count = get_total_unchecked()
    
    # Create the data for the pie chart
    labels = ['For Next Update', 'Ongoing', 'Not Yet Started']
    values = [checked_count, ongoing_count, unchecked_count]
    
    # Define colors for the pie chart
    colors = ['#39B54A','#F8B237','#E4E4E4']
    
    # Create the pie chart trace
    trace = go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))
    
    # Define layout for the pie chart
    layout = go.Layout(showlegend=False)
    
    # Return the figure
    return {'data': [trace], 'layout': layout}

def get_undergraduate_count():
    sql = """
    SELECT COUNT(*)
    FROM eqateam.sar_report sr
    JOIN eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
    WHERE pd.pro_program_type_id = 'Undergraduate'
    """
    values = []
    cols = ['total']
    df = db.querydatafromdatabase(sql, values, cols)
    return df['total'].iloc[0]
def generate_sar_submissions_chart():
    # Retrieve data from the database
    sql = """
        SELECT 
            pro_program_type_id,
            COUNT(*) AS input_count
        FROM 
            eqateam.program_details
        GROUP BY 
            pro_program_type_id
    """
    program_data = db.querydatafromdatabase(sql, [], ['pro_program_type_id', 'input_count'])

    # Map IDs to labels
    id_to_label = {1: 'C ', 2: 'D ', 3: 'A ', 4: 'U ', 5: 'M ', 6: 'P '}
    program_data['pro_program_type_label'] = program_data['pro_program_type_id'].map(id_to_label)
    
    # Define colors for alternating bars
    colors = ['#F8B237', '#40BFBC', '#D37157', '#39B54A', '#FFC937']
    
    # Create bar chart trace with alternating colors
    trace = go.Bar(
        x=program_data['input_count'],
        y=program_data['pro_program_type_label'],
        orientation='h',
        marker=dict(color=[colors[i % len(colors)] for i in range(len(program_data['input_count']))])  # Alternating colors
    )
    
    # Define layout for the bar chart
    layout = go.Layout(
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    # Return the figure
    return {'data': [trace], 'layout': layout}



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
                                                     
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dcc.Graph(
                                                                    id='donut-chart', 
                                                                    figure=generate_donut_chart(),
                                                                    config={'displayModeBar': False},  # Hide the mode bar for a cleaner look
                                                                    style={'height': '500px', 'margin-top': '0px', 'padding-top': '0px'}  # Adjust height and remove top margin
                                                                ),
                                                                style={'padding': '0px', 'margin-top': '-20px'}  # Remove any padding around the graph and adjust margin
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Span(get_total_checked(), style={"font-weight": "bold", "font-size": "24px", "display": "flex", "align-items": "center", "justify-content": "center"}),
                                                                                style={'backgroundColor': '#F8B237', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units currently accomplishing their accreditation", 
                                                                                style={'marginLeft': '10px', 'fontSize': '0.9rem', 'textAlign': 'left', 'marginRight': '15px'}),
                                                                                width=9,
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Span(get_total_ongoing(), style={"font-weight": "bold", "font-size": "24px", "display": "flex", "align-items": "center", "justify-content": "center"}),
                                                                                style={'backgroundColor': '#39B54A', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units on schedule for next accreditation", 
                                                                                style={'marginLeft': '10px', 'fontSize': '0.9rem', 'textAlign': 'left', 'marginRight': '15px'}),
                                                                                width=9,
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Span(get_total_unchecked(), style={"font-weight": "bold", "font-size": "24px", "display": "flex", "align-items": "center", "justify-content": "center"}),
                                                                                style={'backgroundColor': '#E4E4E4', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', "margin-right": "3px"}
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units yet to commence accreditation requirements", 
                                                                                style={'marginLeft': '10px', 'fontSize': '0.9rem', 'textAlign': 'left', 'marginRight': '15px'}),
                                                                                width=9,
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    dcc.Interval(
                                                        id='interval-component',
                                                        interval=60000,  # in milliseconds (60 seconds)
                                                        n_intervals=0
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
                                            dbc.CardBody(
                                                dcc.Graph(
                                                    id='sar-submissions-chart',
                                                    figure=generate_sar_submissions_chart(),
                                                    config={'displayModeBar': False},  # Hide the mode bar for a cleaner look
                                                    style={'height': '200px', 'margin-top': '0px', 'padding-top': '0px'}  # Adjust height and remove top margin
                                                ),
                                            ),
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
