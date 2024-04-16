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
                        html.H1("ACADEMIC UNIT HEADS DIRECTORY"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/acadheadsdirectory/acadheads_profile', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='acadheadsdirectory_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ],
                             
                            className="align-items-center",   
                            justify="between",  
                        ),
  
                        # Placeholder for the users table
                        html.Div(
                            id='acadheadsdirectory_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        )

                    ], width=9, style={'marginLeft': '15px'}
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
        Output('acadheadsdirectory_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('acadheadsdirectory_filter', 'value'),
    ]
    )

def acadheadsdirectory_loadlist(pathname, searchterm):
    if pathname == '/acad_heads_directory':
        # Updated SQL query to match the new table and column structure
        sql = """  
             
        """

        cols = ['Surname', 'First Name', 'Full Name', 'Position', 'Email']  # Add 'Phone', 'Dept', etc. if needed

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