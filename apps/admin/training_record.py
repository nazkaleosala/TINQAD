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
                        html.H1("TRAINING LIST"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Training Document", color="primary", 
                                        href='/training_documents?mode=add',  
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
    if pathname == '/view/training_record':
        sql = """
            SELECT 
                td.complete_name AS "QAO Name",
                td.fac_posn AS "Faculty Position",
                clu.cluster_name AS "Cluster",
                col.college_name AS "College",
                qt.trainingtype_name AS "QA Training",
                td.departure_date AS "Departure Date",
                td.return_date AS "Return Date",
                td.venue AS "Venue"
            FROM 
                adminteam.training_documents td
            LEFT JOIN 
                public.clusters clu ON td.cluster_id = clu.cluster_id
            LEFT JOIN 
                public.college col ON td.college_id = col.college_id
            LEFT JOIN 
                qaofficers.training_type qt ON td.qa_training_id = qt.trainingtype_id
            WHERE 
                NOT train_docs_del_ind
        
        """

        cols = ["QAO Name","Faculty Position","Cluster","College","QA Training", "Departure Date", "Return Date","Venue"]

        if searchterm: 
            sql += """ WHERE td.complete_name ILIKE %s OR td.fac_posn ILIKE  %s OR qt.trainingtype_name ILIKE %s OR 
                clu.cluster_name ILIKE %s  """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern, like_pattern]
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols) 

        if df.shape[0] > 0:
            buttons = []
            for training_documents_id in df['ID']:
                buttons.append(
                    html.Div(
                        dbc.Button('Edit',
                                   href=f'training_documents?mode=edit&id={training_documents_id}',
                                   size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['Action'] = buttons

            df = df[["QAO Name","Faculty Position","Cluster","College","QA Training", "Departure Date", "Return Date","Venue", "Action"]]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate
    
