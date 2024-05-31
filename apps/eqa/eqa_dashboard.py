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




#year dropdown
def assess_get_available_years(): 
    sql = """
    SELECT DISTINCT EXTRACT(YEAR FROM arep_sched_assessdate + INTERVAL '5 years') AS year
    FROM eqateam.assess_report
    ORDER BY year DESC
    """
    
    values = []   
    cols = ['year']   
    df = db.querydatafromdatabase(sql, values, cols)
    
    years = df['year'].tolist()
    
    return [{'label': str(year), 'value': str(year)} for year in years]










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
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    html.H3(
                                                        [
                                                            html.Strong("SAR Submissions"),  # Bold only this part
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

                                        html.Br(),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    html.H3(
                                                        [
                                                            html.Strong("SAR (For Checking)"),  
                                                        ],
                                                        className="mb-0",  # Remove bottom margin
                                                        style={'fontSize': '1.5rem'}  # Adjust font size
                                                    )
                                                ),
                                                dbc.CardBody(
                                                    html.Div(
                                                        id='sar_forchecking', 
                                                        style={
                                                            'marginTop': '20px',
                                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                                        }
                                                    ),
                                                ),
                                            ]
                                        ),
                                    ],
                                    width=4
                                ),
 
                            ]
                        ),

                        
                        html.H5(html.B("Assessment Schedule")),

                        dbc.Row(
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='assesschedule_filter',
                                        placeholder='🔎 Search by degree program, college',
                                        className='ml-auto'   
                                    ),
                                    width=6,
                                ),
                                dbc.Col( 
                                    dcc.Dropdown(
                                        id='assesschedule_yeardropdown',
                                        options=assess_get_available_years(),
                                        placeholder="Filter by year",
                                        multi=True
                                    ),
                                    width=2
                                ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        id='assesschedule_list', 
                                        style={
                                            'marginTop': '20px',
                                            'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                        }
                                    ),
                                    width=8,
                                ),

                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("Assessments (For Checking)"),  
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}
                                                )
                                            ),
                                            dbc.CardBody(
                                                html.Div(
                                                    id='assessments_forchecking', 
                                                    style={
                                                        'marginTop': '20px',
                                                        'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                                    }
                                                ),
                                            ),
                                        ]
                                    ),
                                    width=4,
                                ),
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
    Output('sar_forchecking', 'children'),
    [Input('url', 'pathname')]
) 
def eqa_sar_forchecking(pathname):
    if pathname == '/eqa_dashboard': 
        sql = """
        SELECT 
            pd.pro_degree_shortname AS "Degree Program",
            sr.sarep_currentdate AS "Date Submitted"
        FROM 
            eqateam.sar_report sr
        JOIN 
            eqateam.program_details pd ON sr.sarep_degree_programs_id = pd.programdetails_id
        WHERE 
            sr.sarep_checkstatus = 'For Checking'
            AND sr.sarep_del_ind IS FALSE

        """

        cols = ['Degree Program', 'Date Submitted']
        values = []
         
        df = db.querydatafromdatabase(sql, values, cols) 
   
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No SAR for checking yet")
    else:
        return html.Div("No SAR for checking yet")







@app.callback(
    Output('assessments_forchecking', 'children'),
    [Input('url', 'pathname')]
) 
def eqa_assessments_forchecking(pathname):
    if pathname == '/eqa_dashboard': 
        sql = """
        SELECT 
            arep_degree_programs_id AS "Degree Program",
            arep_currentdate AS "Date Submitted"
        FROM 
            eqateam.assess_report  
        WHERE 
            arep_checkstatus = 'For Checking'
            AND arep_del_ind IS FALSE

        """

        cols = ['Degree Program', 'Date Submitted']
        values = []
         
        df = db.querydatafromdatabase(sql, values, cols) 
   
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No Assessment for checking yet")
    else:
        return html.Div("No Assessment for checking yet")












@app.callback(
    Output('assesschedule_list', 'children'),
    [
        Input('url', 'pathname'), 
        Input('assesschedule_filter', 'value'), 
        Input('assesschedule_yeardropdown', 'value')
    ]
)


def assessmentschedule_loadlist(pathname, searchterm, selected_years):
    if pathname == '/eqa_dashboard': 
        sql = """  
            SELECT 
                arep_degree_programs_id AS "Degree Program", 
                arep_sched_assessdate AS "Latest Assessment Date",
                EXTRACT(YEAR FROM arep_sched_assessdate + INTERVAL '5 years') AS "Next Assessment Year"
            FROM 
                eqateam.assess_report AS a 
            WHERE
                arep_del_ind IS FALSE
                AND arep_report_type = '2'
                AND arep_review_status = '1';
        """

        cols = ["Degree Program", 'Latest Assessment Date','Next Assessment Year']   
        
        values = []
         
        if selected_years:  # selected_years will be a list of selected years
            sql += " AND EXTRACT(YEAR FROM arep_sched_assessdate + INTERVAL '5 years') IN %s"
            values.append(tuple(selected_years))

        df = db.querydatafromdatabase(sql, values, cols) 

         # Filter by search term
        if searchterm:
            sql += " AND (arep_degree_programs_id ILIKE %s)"
            values.extend(['%' + searchterm + '%', '%' + searchterm + '%'])

        df = db.querydatafromdatabase(sql, values, cols)

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No recorded assessments yet")
    else:
        raise PreventUpdate