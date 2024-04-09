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
                        html.H1("SEARCH USERS"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/searchusers/newuser_profile', 
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='searchusers_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width=8,
                                ),
                            ],
                            className="align-items-center",   
                            justify="between",  
                        ),
                        # Placeholder for the users table
                        html.Div(id='searchusers_list', style={'marginTop': '20px'})  
                    ], 
                    width=8, 
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
        Output('searchusers_list', 'children')
    ],
    [
        Input('url', 'pathname'),  
        Input('searchusers_filter', 'value'),
    ]
)

def searchusers_loaduserlist (pathname, searchterm):
    if pathname == '/search_users':
        sql = """  
            SELECT user_sname AS "Surname", user_fname AS "First Name", user_office AS "Dept", 
                user_position AS "Position", user_email AS "Email",  
                user_phone_num AS "Phone"
            FROM maindashboard.users
        """

        
        cols = ['Surname', 'First Name', 'Dept', 'Position', 'Email', 'Phone']

        if searchterm:
            # Add a WHERE clause with ILIKE to filter the results
            sql += """ WHERE user_sname ILIKE %s OR user_fname ILIKE  %s OR user_position ILIKE %s OR 
                user_email ILIKE %s  """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern,   like_pattern  , like_pattern]
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