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

import datetime

custom_css = {
    "tabs": {"background-color": "#C2C2C2"},
    "tab": {"padding": "20px"},
    "active_tab": {"background-color": "yellow"}
}
  
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
              
                dbc.Col(
                    [
                        html.H1("RECORD EXPENSES"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='recordexpenses_filter',
                                        placeholder='🔎 Search by Payee Name, Status, BUR no.',
                                        className='ml-auto'   
                                    ),
                                    width=8,
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add expense", color="primary", 
                                        href='/record_expenses/add_expense', 
                                    ),
                                    width="auto",    
                                ),
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),
                        html.Br(),

                        dbc.Tabs(
                            [
                                dbc.Tab(label="|   Current   |", tab_id="current"),
                                dbc.Tab(label="|   View All Expenses   |", tab_id="view_all"),
                            ],
                            id="tabs",
                            active_tab="current",
                            style=custom_css["tabs"],
                            className="custom-tabs"
                        ),

                        html.Div(
                            id="tabs-content",
                            children=[
                                html.Div(
                                    id='recordexpenses_list', 
                                    style={
                                        'marginTop': '20px',
                                        'overflowX': 'auto',# This CSS property adds a horizontal scrollbar
                                        'overflowY': 'auto',   
                                        'maxHeight': '1000px',
                                    }
                                )
                            ],
                        ),
                        
                         
                    ], 
                    width=9, 
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width={"size": 12, "offset": 0}),
            ]
        )
    ]
) 


@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "active_tab")],
)
def switch_tab(tab):
    if tab == "current":
        return [
            html.Div(
                id='recordexpenses_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                }
            )
        ]
    elif tab == "view_all":
        return [
            html.Div(
                id='recordexpenses_list', 
                style={
                    'marginTop': '20px',
                    'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                    }
                )
            ]
    return html.Div("No Tab Selected")






@app.callback(
    Output('recordexpenses_list', 'children'),
    [
        Input('url', 'pathname'),   
        Input('recordexpenses_filter', 'value'),
        Input("tabs", "active_tab")
    ]
)
def recordexpenses_loadlist(pathname, searchterm, active_tab):
    if pathname == '/record_expenses':
        if active_tab == "current":
            # Get the current month and year
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year

            # Updated SQL query to select records for the current month
            sql = """
                SELECT 
                    exp_date AS "Date", 
                    exp_payee AS "Payee Name", 
                    me.main_expense_name AS "Main Expense Type",
                    se.sub_expense_name AS "Sub Expense Type",
                    exp_particulars AS "Particulars", 
                    exp_amount AS "Amount", 
                    es.expense_status_name AS "Status",
                    exp_bur_no AS "BUR No",
                    exp_submitted_by AS "Submitted by"
                FROM adminteam.expenses AS e
                LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
                LEFT JOIN adminteam.sub_expenses AS se ON e.sub_expense_id = se.sub_expense_id
                LEFT JOIN adminteam.expense_status AS es ON e.exp_status = es.expense_status_id
                WHERE EXTRACT(MONTH FROM exp_date) = %s AND EXTRACT(YEAR FROM exp_date) = %s
            """

            cols = ['Date', 'Payee Name', 'Main Expense Type', 'Sub Expense Type',  'Particulars', 'Amount', 'Status', 'BUR No', 'Submitted by']

            if searchterm:
                # Add a WHERE clause with ILIKE to filter the results
                sql += """ AND (exp_payee ILIKE %s OR es.expense_status_name ILIKE %s OR exp_bur_no ILIKE %s) """
                like_pattern = f"%{searchterm}%"
                values = [current_month, current_year, like_pattern, like_pattern, like_pattern]
            else:
                values = [current_month, current_year]

        elif active_tab == "view_all":
            # Updated SQL query to select all records from the expenses table
            sql = """
                SELECT 
                    exp_date AS "Date", 
                    exp_payee AS "Payee Name", 
                    me.main_expense_name AS "Main Expense Type",
                    se.sub_expense_name AS "Sub Expense Type",
                    exp_particulars AS "Particulars", 
                    exp_amount AS "Amount", 
                    es.expense_status_name AS "Status",
                    exp_bur_no AS "BUR No",
                    exp_submitted_by AS "Submitted by"
                FROM adminteam.expenses AS e
                LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
                LEFT JOIN adminteam.sub_expenses AS se ON e.sub_expense_id = se.sub_expense_id
                LEFT JOIN adminteam.expense_status AS es ON e.exp_status = es.expense_status_id
            """

            cols = ['Date', 'Payee Name', 'Main Expense Type', 'Sub Expense Type',  'Particulars', 'Amount', 'Status', 'BUR No', 'Submitted by']

            if searchterm:
                # Add a WHERE clause with ILIKE to filter the results
                sql += """ WHERE exp_payee ILIKE %s OR es.expense_status_name ILIKE %s OR exp_bur_no ILIKE %s """
                like_pattern = f"%{searchterm}%"
                values = [like_pattern, like_pattern, like_pattern]
            else:
                values = [] 

        df = db.querydatafromdatabase(sql, values, cols) 

        # Format the amount column
        if not df.empty:  # Check if the DataFrame is not empty
            df['Amount'] = df['Amount'].apply(lambda x: '{:,.2f}'.format(x))
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records yet this month")
    else:
        raise PreventUpdate
