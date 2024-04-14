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
                        html.H1("EQA TRACKER"),
                        html.Hr(),
 
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='accreditationtracker_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ]
                        ),

                        html.Div(
                            id='accreditationtracker_list', 
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
        Output('accreditationtracker_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('accreditationtracker_filter', 'value'),
    ]
    )

def accreditationtracker_loadlist(pathname, searchterm):
    if pathname == '/accreditation_tracker': 
        sql = """  
            
        """

        cols = ['Degree Program', 'EQA Type A', 'EQA Type B', 'EQA Type C', 'EQA Type D', 'EQA Type E', 'EQA Type F']   

        if searchterm:
            
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