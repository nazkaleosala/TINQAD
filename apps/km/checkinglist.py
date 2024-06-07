from dash import dash, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db



                        


layout = html.Div(
    [
        dbc.Row(
            [
                cm.sidebar,
                dbc.Col(
                    [
                        html.H1("SDG MANAGE EVIDENCE LIST"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "➕ Add Submission",
                                        color="primary",
                                        href='/SDGimpactrankings/SDG_submission?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "✍🏻 Add Revision",
                                        color="warning",
                                        href='/SDGimpactrankings/SDG_revision?mode=add',
                                    ),
                                    width="auto",
                                    className="mb-0",
                                ),
                            ]
                        ),

                         

                        html.Br(), 

                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions for Checking"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='basicchecking_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px', 
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Submissions in need of Revisions"),
                                        dbc.CardBody(
                                            html.Div(
                                                id='basicrevisions_list', 
                                                style={
                                                    'marginTop': '20px',
                                                    'overflowX': 'auto',
                                                    'overflowY': 'auto',
                                                    'maxHeight': '300px', 
                                                }
                                            )
                                        )
                                    ],
                                    color="light"
                                ),
                                width="12"
                            )
                        ), 
                        html.Br(),  html.Br(),    
                    ], width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(), html.Br(), html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
)







@app.callback(
    [
        Output('basicchecking_list', 'children')
    ],
    [
        Input('url', 'pathname'),
    ]
)

def basicchecking_list (pathname):
    if pathname == '/checkinglist':   
         
        sql = """
            SELECT 
                sdgsubmission_id AS "ID", 
                sdg_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                (SELECT deg_unit_name FROM public.deg_unit WHERE deg_unit_id  = sdg_deg_unit_id) AS "Department",
                sdg_description AS "Description",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
                (
                    SELECT json_agg(sdgcriteria_code)
                    FROM kmteam.SDGCriteria
                    WHERE sdgcriteria_id IN (
                        SELECT CAST(jsonb_array_elements_text(sdg_applycriteria) AS INTEGER)
                    )
                ) AS "Applicable Criteria"
            FROM  
                kmteam.SDGSubmission
            WHERE
                sdg_checkstatus = '1'   
                AND sdg_del_ind IS FALSE
        """
        cols = ['ID', 'Evidence Name', 'Office','Department', 'Description', 'Ranking Body', "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)
 
        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No submissions for checking")]
    else:
        raise PreventUpdate







@app.callback(
    [
        Output('basicrevisions_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
    ]
)

def basicrevisions_list (pathname):
    if pathname == '/checkinglist':  
         
        sql = """
            SELECT 
                sdgsubmission_id AS "ID", 
                sdg_evidencename AS "Evidence Name",
                sdg_notes  AS "Revision Notes",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                (SELECT deg_unit_name FROM public.deg_unit WHERE deg_unit_id  = sdg_deg_unit_id) AS "Department",
                sdg_description AS "Description", 
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
                (
                    SELECT json_agg(sdgcriteria_code)
                    FROM kmteam.SDGCriteria
                    WHERE sdgcriteria_id IN (
                        SELECT CAST(jsonb_array_elements_text(sdg_applycriteria) AS INTEGER)
                    )
                ) AS "Applicable Criteria"
            FROM  
                kmteam.SDGSubmission
            WHERE
                sdg_checkstatus = '3'   AND sdg_del_ind IS FALSE
        """ 
        cols = ['ID', 'Evidence Name', 'Revision Notes', 'Office', 'Department','Description', 'Ranking Body', "Applicable Criteria"]

        df = db.querydatafromdatabase(sql, [], cols)
 
        if not df.empty:
            df["Applicable Criteria"] = df["Applicable Criteria"].apply(
                lambda x: ", ".join(x) if x else "None"
            )
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No submissions for revision")]
    else:
        raise PreventUpdate




  