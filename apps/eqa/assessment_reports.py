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
                                    dbc.Input(
                                        type='text',
                                        id='assessmentreports_filter',
                                        placeholder='🔎 Search by degree program',
                                        className='ml-auto'   
                                    ),
                                    width="6",
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New SAR", color="primary", 
                                        href='/assessmentreports/sar_details?mode=add', 
                                    ),
                                    width="auto",    
                                     
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New Assessment", color="warning", 
                                        href='/assessmentreports/assessment_details?mode=add', 
                                    ),
                                    width="auto",    
                                )
                            ]
                        ),

                        html.Br(),

                        dbc.Tabs(
                            [
                                dbc.Tab(label="|   Self Assessment Reports   |", tab_id="sar"),
                                dbc.Tab(label="|   Other Assessments   |", tab_id="others"),
                            ],
                            id="tabs",
                            active_tab="sar",
                             
                            className="custom-tabs"
                        ),

                         
                        html.Div(
                            id="content-tab",
                            children=[
                                html.Div(
                                    id='assessmentreports_list', 
                                    style={
                                        'marginTop': '20px',
                                        'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                                    }
                                )
                            ],
                        ),

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
    Output("content-tab", "children"),
    [Input("tabs", "active_tab")],
)
def switch_tab(tab):
    if tab == "sar":
        return [
            html.Div(
                id='assessmentreports_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                }
            )
        ]
    elif tab == "others":
        return [
            html.Div(
                id='assessmentreports_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                    }
                )
            ]
    return html.Div("No Tab Selected")




 
@app.callback(
    [Output('assessmentreports_list', 'children')],
    [
        Input('url', 'pathname'),
        Input('assessmentreports_filter', 'value'),
        Input('tabs', 'active_tab'),
    ]
)
def assessmentreports_loadlist(pathname, searchterm, active_tab):
    if pathname != '/assessment_reports':
        raise PreventUpdate

    sql = None
    values = []
    cols = []

    # Generate SQL and set columns based on active_tab
    if active_tab == "sar":
        sql = """
            SELECT 
                sarep_id AS "ID", 
                sarep_currentdate AS "Date", 
                dp.pro_degree_title  AS "Degree Program", 
                sarep_checkstatus AS "Check Status",
                sarep_link AS "SAR Link",
                sarep_file_path AS "SAR File",
                sarep_review_status AS "Review Status",
                sarep_sarscore AS "SAR Score"
            FROM 
                eqateam.sar_report AS ar
            LEFT JOIN 
                eqateam.program_details AS dp ON ar.sarep_degree_programs_id = dp.programdetails_id 
            WHERE
                sarep_del_ind IS FALSE
        """
        cols = ['ID', 'Date', 'Degree Program', "Check Status", 'SAR Link', "SAR File", "Review Status", "SAR Score"]

    elif active_tab == "others":
        sql = """
            SELECT 
                arep_id AS "ID",
                arep_currentdate AS "Date",
                arep_degree_programs_id AS "Degree Program",
                arep_title AS "Assessment Title",
                arep_approv_eqa AS "EQA Type",
                arep_checkstatus AS "Check Status",
                rt.report_type_name AS "Report Type",
                arep_link AS "Link",
                arep_file_path AS "PDF",
                rs.review_status_name AS "Review Status"
            FROM 
                eqateam.assess_report AS assr
            LEFT JOIN 
                eqateam.report_type AS rt ON assr.arep_report_type = rt.report_type_id 
            LEFT JOIN 
                eqateam.review_status AS rs ON assr.arep_review_status = rs.review_status_id 
            
            WHERE
                arep_del_ind IS FALSE
        """
        cols = ['ID','Date', 'Degree Program', 'Assessment Title', 'EQA Type', 'Check Status', "Report Type", "Link","PDF","Review Status"]

    else:
        return [html.Div("Invalid tab selection")]

    # Apply search filter if searchterm is provided
    if searchterm:
        like_pattern = f"%{searchterm}%"
        if active_tab == "sar":
            sql += """ AND (dp.pro_degree_title ILIKE %s OR 
                            sarep_checkstatus ILIKE %s OR
                            sarep_link ILIKE %s OR
                            sarep_file_path ILIKE %s OR
                            sarep_review_status ILIKE %s OR
                            sarep_sarscore ILIKE %s) """
            values = [like_pattern] * 6
        elif active_tab == "others":
            sql += """ AND (arep_degree_programs_id ILIKE %s OR
                            arep_title ILIKE %s OR
                            arep_approv_eqa ILIKE %s OR
                            arep_checkstatus ILIKE %s OR
                            rt.report_type_name ILIKE %s OR
                            rs.review_status_name ILIKE %s) """
            values = [like_pattern] * 6

    # Ensure that sql has a valid query before accessing it
    if sql:
        df = db.querydatafromdatabase(sql, values, cols)

        if "Review Status" in df.columns:
            df["Review Status"] = df["Review Status"].replace({1: "Endorsed for EQA", 2: "For Revision"})

        # Generate the table from the DataFrame
        if not df.empty:
            if active_tab == "sar":
                df["Action"] = df["ID"].apply(
                    lambda x: html.Div(
                        dbc.Button('Edit', href=f'/assessmentreports/sar_details?mode=edit&id={x}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
                df = df[['Date', 'Degree Program', "Check Status", 'SAR Link', "SAR File", "Review Status", "SAR Score", 'Action']]
            
            elif active_tab == "others":
                df["Action"] = df["ID"].apply(
                    lambda x: html.Div(
                        dbc.Button('Edit', href=f'/assessmentreports/assessment_details?mode=edit&id={x}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
                df = df[['Date', 'Degree Program', 'Assessment Title', 'EQA Type', 'Check Status', "Report Type", "Link", "PDF", "Review Status", 'Action']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    
    return [html.Div("Query could not be processed")]
