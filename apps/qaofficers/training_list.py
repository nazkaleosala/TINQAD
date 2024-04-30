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
 



def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  # Add space below each card
    )
 
def create_table(headers, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in headers],
        style_header={'fontWeight': 'bold'}, 
    )
 


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
                        html.H1("QA OFFICERS TRAINING LIST"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(create_card("No. of faculty with QA Training"), width=12),
                                
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(create_card("Total Trained Officers"), width=12),
                                
                            ]
                        ),
                        html.Br(),
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Officer", color="primary", 
                                        href='/QAOfficers/addtraining', 
                                    ),
                                    width="auto",    
                                ),
                            ],
                            className="align-items-center",   
                            style={
                                "margin-right": "2px",
                                "margin-bottom": "15px",
                            }
                        ), 

                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='qaotraininglist_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ]
                        ),

                        html.Div(
                            id='qaotraininglist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        )
                        
                    ], 
                    width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
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
    [
        Output('qaotraininglist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('qaotraininglist_filter', 'value'),
    ]
    )

def programlist_loadlist(pathname, searchterm):
    if pathname == '/training_list': 
        sql = """  
            
        """

        cols = ['Name', 'Rank/Designation', 'Department','College','Academic Cluster', 'Trainings']   

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