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
                        html.H1("RECORD EXPENSES"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add expense", color="primary", 
                                        href='/record_expenses/add_expense', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='recordexpenses_filter',
                                        placeholder='🔎 Search by name, office, position',
                                        className='ml-auto'   
                                    ),
                                    width=8,
                                ),
                                 
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),
                        # Placeholder for the users table
                        html.Div(
                            id='recordexpenses_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        )
                    ], 
                    width=9, 
                    style={'marginLeft': '15px'}
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
        Output('recordexpenses_list', 'children')
    ],
    [
        Input('url', 'pathname'),   
        Input('recordexpenses_filter', 'value'),
    ]
)


def recordexpenses_loadlist(pathname, searchterm):
    if pathname == '/record_expenses':
        # Updated SQL query to select all records from the expenses table
        sql = """
            SELECT 
                exp_date AS "Date", 
                exp_payee AS "Payee Name", 
                me.main_expense_name AS "Main Expense Type",
                se.sub_expense_name AS "Sub Expense Type",
                exp_particulars AS "Particulars", 
                exp_amount AS "Amount", 
                exp_status AS "Status",
                exp_bur_no AS "BUR No"
            FROM adminteam.expenses AS e
            LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
            LEFT JOIN adminteam.sub_expenses AS se ON e.sub_expense_id = se.sub_expense_id
        """

        cols = ['Date', 'Payee Name', 'Main Expense Type', 'Sub Expense Type',  'Particulars', 'Amount', 'Status', 'BUR No']

        if searchterm:
            # Add a WHERE clause with ILIKE to filter the results
            sql += """ WHERE exp_payee ILIKE %s OR exp_particulars ILIKE %s OR exp_bur_no ILIKE %s """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern]
        else:
            values = []

        df = db.querydatafromdatabase(sql, values, cols) 

        # Generate the table from the DataFrame
        if not df.empty:  # Check if the DataFrame is not empty
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate