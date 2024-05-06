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
                        html.H1("QA OFFICERS TRAINING LIST"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='viewlist_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="6",
                                ),
                                 
                            ]
                        ),

                        html.Br(),
 
                        html.Div(
                            id='viewlist_list', 
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
        Output('viewlist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('viewlist_filter', 'value'),
    ]
    )

def traininglist_loadlist(pathname, searchterm):
    if pathname == '/QAOfficers/datalist': 
        sql = """
            SELECT 
                qo.qaofficer_full_name AS "Name",
                cp.cuposition_name AS "Rank/Designation",
                du.deg_unit_name AS "Department",
                cl.college_name AS "College",
                clus.cluster_name AS "Academic Cluster",
                STRING_AGG(qtd.qatr_training_name, ', ') AS "Trainings"
            FROM 
                qaofficers.qa_officer AS qo
            LEFT JOIN 
                qaofficers.qa_training_details AS qtd
                ON qo.qaofficer_id = qtd.qatr_officername_id
            LEFT JOIN 
                qaofficers.cuposition AS cp
                ON qo.qaofficer_cuposition_id = cp.cuposition_id
            LEFT JOIN 
                public.deg_unit AS du
                ON qo.qaofficer_deg_unit_id = du.deg_unit_id
            LEFT JOIN 
                public.college AS cl
                ON qo.qaofficer_college_id = cl.college_id
            LEFT JOIN 
                public.clusters AS clus
                ON qo.qaofficer_cluster_id = clus.cluster_id
            GROUP BY 
                qo.qaofficer_full_name, cp.cuposition_name, du.deg_unit_name, cl.college_name, clus.cluster_name
        """


        cols = ['Name', 'Rank/Designation', 'Department','College','Academic Cluster', 'Trainings']   

        if searchterm:
            sql += """
                WHERE
                    qaofficer_sname ILIKE %s OR
                    qaofficer_fname ILIKE %s OR
                    qaofficer_role ILIKE %s
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern] * 3
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