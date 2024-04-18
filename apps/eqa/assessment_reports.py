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
                        html.H1("ASSESSMENT REPORTS"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/assessmentreports/assessment_details', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='assessmentreports_filter',
                                        placeholder='🔎 Search by degree program',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ]
                        ),

                         
                        # Placeholder for the users table
                        html.Div(
                            id='assessmentreports_list', 
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
        Output('assessmentreports_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('assessmentreports_filter', 'value'),
    ]
    )


def assessmentreports_loadlist(pathname, searchterm):
    if pathname == '/assessment_reports':  # Adjusted URL path
         
        sql = """  
            SELECT 
                arep_currentdate AS "Date", 
                d.deg_prog_name AS "Degree Program",
                c.cluster_name AS "Cluster",
                a.arep_title AS "Assessment Title"
            FROM 
                eqateam.assess_report AS a 
            LEFT JOIN 
                public.deg_prog_title AS d ON a.arep_deg_prog_id = d.deg_prog_id
            LEFT JOIN 
                public.clusters AS c ON a.arep_cluster_id = c.cluster_id
        """

        cols = ['Date','Degree Program', 'Cluster', 'Assessment Title']

        if searchterm:
            sql += """ WHERE d.deg_prog_name ILIKE %s OR
                        c.cluster_name ILIKE %s OR
                        a.arep_title ILIKE %s """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern]
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