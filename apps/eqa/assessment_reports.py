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
                                        "➕ Add New SAR", color="primary", 
                                        href='/assessmentreports/sar_details', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New Assessment", color="warning", 
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
                                    width="6",
                                ),
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
    # Default response if the path is not correct
    if pathname != '/assessment_reports':
        raise PreventUpdate
    
    # Initialize default values to prevent UnboundLocalError
    sql = None
    values = []

    # Generate SQL and set columns based on active_tab
    if active_tab == "sar":
        sql = """
            SELECT 
                sarep_currentdate AS "Date", 
                dp.degree_name AS "Degree Program",
                sarep_title AS "Assessment Title",
                sarep_approv_eqa AS "EQA Type",
                sarep_checkstatus AS "Status"
            FROM 
                eqateam.sar_report AS ar
            LEFT JOIN 
                public.degree_programs AS dp ON ar.sarep_degree_programs_id = dp.degree_id 
        """
        cols = ['Date', 'Degree Program', 'Assessment Title', 'EQA Type' , 'Status']

    elif active_tab == "others":
        sql = """
            SELECT 
                arep_currentdate AS "Date",
                dp.degree_name AS "Degree Program",
                arep_title AS "Assessment Title",
                arep_approv_eqa AS "EQA Type",
                arep_checkstatus AS "Status"
            FROM 
                eqateam.assess_report AS ar
            LEFT JOIN 
                public.degree_programs AS dp ON ar.arep_degree_programs_id = dp.degree_id 
        """
        cols = ['Date', 'Degree Program', 'Assessment Title', 'EQA Type' , 'Status']

    else:
        # If the active_tab is unexpected, raise PreventUpdate or return a default response
        return [html.Div("Invalid tab selection")]

    # Apply search filter if searchterm is provided
    if searchterm:
        like_pattern = f"%{searchterm}%"
        sql += """ WHERE dp.degree_name ILIKE %s OR 
                    sarep_title ILIKE %s """
        values = [like_pattern, like_pattern]

    # Ensure that sql has a valid query before accessing it
    if sql:
        df = db.querydatafromdatabase(sql, values, cols)

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    
    return [html.Div("Query could not be processed")]