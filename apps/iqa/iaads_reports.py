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



layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("iAADS REPORTS SUMMARY AND CONSOLIDATIONS"),
                        html.Hr(),


                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Report", color="primary", 
                                        href='/iaadsreport/report_details', 
                                    ),
                                    width="auto",    
                                )
                            ],
                             
                             
                        ),

                        html.Br(),
                        html.H4("CONSOLIDATED REPORTS"),
                          
                         
                        html.Div(
                            id='iaadsreports_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        )


                    ], width=8, style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)




@app.callback(
    [
        Output('iaadsreports_list', 'children')
    ],
    [
        Input('url', 'pathname'), 
    ]
    )

def acadheadsdirectory_loadlist(pathname, searchterm):
    if pathname == '/iaads_reports':
        # Updated SQL query to match the new table and column structure
        sql = """  
            SELECT 
                
        """

        cols = ['Academic Unit', 'Degree Granting Unit', 'Department Goals/Direction']  

        if searchterm:
            # Add a WHERE clause with ILIKE to filter the results
            sql += """ WHERE a.unit_head_sname ILIKE %s OR a.unit_head_fname ILIKE %s OR
                        a.unit_head_full_name ILIKE %s OR d.designation_name ILIKE %s  """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern, like_pattern]
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols) 

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate