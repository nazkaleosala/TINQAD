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




#year dropdown

def get_available_years():
    # Query to get unique years from the database
    sql = """
    SELECT DISTINCT EXTRACT(YEAR FROM qaofficer_appointment_start) AS year
    FROM qaofficers.qa_officer
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
                        html.H1("QA OFFICERS DIRECTORY"),
                        html.Hr(),
                        
                        

                        dbc.Row(
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='qadirectory_filter',
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
                                            placeholder="Filter by month",
                                        ),
                                        width="3",
                                    
                                ),
                                dbc.Col( 
                                    dcc.Dropdown(
                                        id='year_dropdown',
                                        options=get_available_years(),
                                        placeholder="Filter by year", 
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
                                        href='/QAOfficers/qaofficers_profile', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                
                                
                            ],
                             
                            className="align-items-center",   
                            justify="between",  
                        ),

                        html.Div(
                            id='qadirectory_list', 
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
    Output('qadirectory_list', 'children'),
    [
        Input('url', 'pathname'),
        Input('qadirectory_filter', 'value'),
        Input('month_dropdown', 'value'),
        Input('year_dropdown', 'value'),
    ],
)
def qadirectory_loadlist(pathname, searchterm, selected_month, selected_year):
    if pathname == '/QAOfficers_directory':
         
        
        # Fetch the data
        sql = """
            SELECT 
                clusters.cluster_shortname AS "Cluster",
                college.college_shortname AS "College",
                deg_unit.deg_unit_name AS "Unit",
                qaofficer_full_name AS "Full Name",
                qaofficer_upmail AS "UP Mail",
                qaofficer_fac_posn AS "Faculty Position",
                qaofficer_facadmin_posn AS "Admin Position",
                qaofficer_staff_posn AS "Staff Position",
                cuposition_name AS "QA Position",
                qaofficer_basicpaper AS "With Basic Paper",
                qaofficer_remarks AS "Remarks",
                qaofficer_alc AS "ALC",
                qaofficer_appointment_start AS "Start Term",
                qaofficer_appointment_end AS "End Term",
                qaofficer_role AS "CU-Level role"
            FROM 
                qaofficers.qa_officer  
            LEFT JOIN 
                qaofficers.cuposition ON qaofficer_cuposition_id = cuposition.cuposition_id
            LEFT JOIN 
                public.clusters ON qaofficer_cluster_id = clusters.cluster_id
            LEFT JOIN 
                public.college ON qaofficer_college_id = college.college_id
            LEFT JOIN 
                public.deg_unit ON qaofficer_deg_unit_id = deg_unit.deg_unit_id
        """

        cols = [
            'Cluster', 'College', 'Unit', 'Full Name', 'UP Mail', 'Faculty Position',
            'Admin Position', 'Staff Position', 'QA Position', 
            'With Basic Paper', 'Remarks', 'ALC', 'Start Term', 'End Term', 
            'CU-Level role'
        ]
        
        # Fetch all data
        df = db.querydatafromdatabase(sql, [], cols)
        
        
        
        # Check if DataFrame is empty after data retrieval
        if df.empty:
            return html.Div("No records to display")
        
        # Apply search term filter
        if searchterm:
            search_cols = ['Full Name', 'UP Mail', 'Faculty Position', 'Unit']
            df = df[df[search_cols].apply(
                lambda row: any(searchterm.lower() in str(cell).lower() for cell in row),
                axis=1
            )]
        
        # Apply additional filters
        df['Start Term'] = pd.to_datetime(df['Start Term'], errors='coerce')  # Handle errors gracefully
        
        if selected_month:
            df = df[df['Start Term'].dt.month == int(selected_month)]
        
        if selected_year:
            df = df[df['Start Term'].dt.year == int(selected_year)]
        
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