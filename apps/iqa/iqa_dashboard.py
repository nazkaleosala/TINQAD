import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, timedelta

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db


def acad_unitheadscount():
    sql = """
        SELECT COUNT(*) 
        FROM iqateam.acad_unitheads  
        WHERE unithead_del_ind IS False
    """
    acad_unitheadstotal_count = db.query_single_value(sql)
    return acad_unitheadstotal_count

# Function to fetch the total count from the database for QA Officers
def qa_officerscount():
    sql = """
        SELECT COUNT(*) 
        FROM qaofficers.qa_officer 
        WHERE qaofficer_del_ind = False
    """
    qa_officerstotal_count = db.query_single_value(sql)
    return qa_officerstotal_count




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
                        html.Br(),

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.B("Academic Unit Heads")),
                                        dbc.CardBody(
                                            [
                                                acad_unitheadscount,
                                                html.Div(
                                                    id='acadheadsdashboard_list',
                                                    style={
                                                        'marginTop': '20px',
                                                        'overflowX': 'auto',
                                                        'overflowY': 'auto',
                                                        'maxHeight': '300px',
                                                    }
                                                )
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.B("Quality Assurance Officers")),
                                        dbc.CardBody(
                                            [
                                                qa_officerscount,
                                                html.Div(
                                                    id='qaofficersdashboard_list',
                                                    style={
                                                        'marginTop': '20px',
                                                        'overflowX': 'auto',
                                                        'overflowY': 'auto',
                                                        'maxHeight': '300px',
                                                    }
                                                )
                                            ]
                                        )
                                    ],
                                    color="light"
                                ),
                                width=12
                            )
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row(
            dbc.Col(
                cm.generate_footer(),
                width={"size": 12, "offset": 0}
            )
        )
    ]
)








@app.callback(
    Output('acadheadsdashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def acadheadsmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard':
        today = datetime.today() 

        sql = f"""
            SELECT 
                c.college_name AS "College",
                COUNT(*) AS "Term Expiry"
            FROM iqateam.acad_unitheads a
            JOIN public.college c ON a.unithead_college_id = c.college_id
            WHERE 
                a.unithead_appointment_end BETWEEN '{today}' AND '{today + timedelta(days=30)}'
                AND a.unithead_del_ind IS False
            GROUP BY a.unithead_college_id, c.college_name; 
        """
         
        cols = ['College', 'Term Expiry']
        
        # Query the database
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return (table)
        else:
            return ("No records to display")
    else:
        raise PreventUpdate
    
 


@app.callback(
    Output('qaofficersdashboard_list', 'children'),
    [Input('url', 'pathname')]
)
def qaofficersmoredetails_loadlist(pathname):
    if pathname == '/iqa_dashboard': 

        sql = """
            SELECT c.college_name AS "College",
                COUNT(*) AS "QA Officers",
                SUM(CASE WHEN qaofficer_basicpaper = 'Yes' THEN 1 ELSE 0 END) AS "Approved Papers",
                SUM(CASE WHEN qaofficer_remarks = 'For renewal' THEN 1 ELSE 0 END) AS "Renewal",
                SUM(CASE WHEN qaofficer_remarks = 'No record' THEN 1 ELSE 0 END) AS "No Record",
                SUM(CASE WHEN qaofficer_appointment_end BETWEEN '{today}' AND '{today + timedelta(days=30)}') AS "Expiring"
            FROM qaofficers.qa_officer q
            JOIN public.college c ON q.qaofficer_college_id = c.college_id
            WHERE q.qaofficer_del_ind = False
            GROUP BY q.qaofficer_college_id, c.college_name;
        """
 
        cols = ['College', 'QA Officers', 'Approved Papers',  'Renewal', 'No Record', 'Expiring']
         
        df = db.querydatafromdatabase(sql, [], cols)
        
        # Process the DataFrame if not empty
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return (table)
        else:
            return ("No records to display")
    else:
        raise PreventUpdate