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
                        html.H1("PROGRAM LIST"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Training Document", color="primary", 
                                        href='/training/training_documents', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='traininglist_filter',
                                        placeholder='🔎 Search by ',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                                 
                            ],
                             
                            className="align-items-center ",   
                            style={
                                "margin-right": "2px",
                                "margin-bottom": "15px",
                                   }
                        ),

 
                        html.Div(
                            id='traininglist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '800px',
                            }
                        ),

                        html.Br(),
                        html.Br(),

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
        Output('traininglist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('traininglist_filter', 'value'),
    ]
)
def traininglist_loadlist(pathname, searchterm):
    if pathname == '/training/training_documents':
        sql = """  
             
        """
 
        values = []

        if searchterm:
            like_pattern = f"%{searchterm}%"
            additional_conditions = """
                 
            """
            values.extend([like_pattern, like_pattern, like_pattern, like_pattern])
            sql += additional_conditions

        final_sql = sql + " ORDER BY pd.pro_degree_shortname"
         
        cols = ["Name, fac_posn, cluster_id, college_id, qa_training_id, departure_date, return_date, venue   "]

        df = db.querydatafromdatabase(final_sql, values, cols)
 
        if not df.empty:
            df[""] = df[""].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records under this criteria")]