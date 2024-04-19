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

#year dropdown

def get_available_years():
    # Query to get unique years from the database
    sql = """
    SELECT DISTINCT EXTRACT(YEAR FROM unithead_appointment_start) AS year
    FROM iqateam.acad_unitheads
    ORDER BY year DESC
    """
    # Execute the query and fetch the results
    values = []  # No need for values in this query
    cols = ['year']  # The column name in the result
    df = db.querydatafromdatabase(sql, values, cols)
    # Extract unique years from the dataframe
    years = df['year'].tolist()
    # Convert years to string and return as dropdown options
    return [{'label': str(year), 'value': str(year)} for year in years]


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("ACADEMIC UNIT HEADS DIRECTORY"),
                        html.Hr(),
                        
                        

                        dbc.Row(
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='acadheadsdirectory_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="6",
                                ),
                                dbc.Col( 
                                     
                                        dcc.Dropdown(
                                            id='month_dropdown',
                                            options=[
                                                {'label': 'January', 'value': '01'},
                                                {'label': 'February', 'value': '02'},
                                                {'label': 'March', 'value': '03'},
                                                {'label': 'April', 'value': '04'},
                                                {'label': 'May', 'value': '05'},
                                                {'label': 'June', 'value': '06'},
                                                {'label': 'July', 'value': '07'},
                                                {'label': 'August', 'value': '08'},
                                                {'label': 'September', 'value': '09'},
                                                {'label': 'October', 'value': '10'},
                                                {'label': 'November', 'value': '11'},
                                                {'label': 'December', 'value': '12'}
                                            ],
                                            placeholder="Filter by Start Term month",
                                        ),
                                        width="3",
                                    
                                ),
                                dbc.Col( 
                                    dcc.Dropdown(
                                        id='year_dropdown',
                                        options=get_available_years(),
                                        placeholder="Filter by Start Term year", 
                                    ),
                                    width="2"
                                ),
                            ]
                        ),

                        html.Br(),

                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/acadheadsdirectory/acadheads_profile', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                
                                
                            ],
                             
                            className="align-items-center",   
                            justify="between",  
                        ),

                        
  
                        # Placeholder for the users table
                        html.Div(
                            id='acadheadsdirectory_list', 
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
    Output('acadheadsdirectory_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('acadheadsdirectory_filter', 'value'),
        Input('month_dropdown', 'value'),  # Corrected input name
        Input('year_dropdown', 'value')
    ]
)
def acadheadsdirectory_loadlist(pathname, searchterm, selected_month, selected_years):
    if pathname == '/acad_heads_directory':
        # Fetch all data from the database
        sql = """
            SELECT au.unithead_sname AS Surname,
                au.unithead_fname AS "First Name",
                cp.cuposition_name AS Position,
                au.unithead_upmail AS Email,
                du.deg_unit_name AS Department, 
                au.unithead_appointment_start AS "Start Term",
                au.unithead_appointment_end AS "End Term"
            FROM iqateam.acad_unitheads AS au
            LEFT JOIN qaofficers.cuposition AS cp ON au.unithead_cuposition_id = cp.cuposition_id
            LEFT JOIN public.deg_unit AS du ON au.unithead_deg_unit_id = du.deg_unit_id
        """

        cols = ['Surname', 'First Name', 'Position', 'Email', 'Department', 'Start Term', 'End Term']

        df = db.querydatafromdatabase(sql, [], cols)  # No need for values, fetch all data

        # Filter the DataFrame based on the search term
        if searchterm:
            search_cols = ['Surname', 'First Name', 'Position', 'Email', 'Department']
            df = df[df[search_cols].apply(lambda row: any(searchterm.lower() in str(cell).lower() for cell in row), axis=1)]

        # Apply additional filters if necessary
        if selected_month:
            df['Start Term'] = pd.to_datetime(df['Start Term'])  # Convert to datetime objects
            df = df[df['Start Term'].dt.month == int(selected_month)]

        if selected_years:
            df = df[df['Start Term'].dt.year.isin(selected_years)]

        # Truncate the 'Start Term' column to ensure it doesn't exceed 10 characters
        df['Start Term'] = df['Start Term'].astype(str).str.slice(0, 10)

 

        # Generate the table from the filtered DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return table
        else:
            return html.Div("No records to display")
    else:
        raise PreventUpdate