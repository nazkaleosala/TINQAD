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
                        html.H1("PROGRAM LIST"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Program", color="primary", 
                                        href='/programlist/program_details', 
                                    ),
                                    width="auto",    
                                ),
                                #dbc.Col(   
                                    #dbc.Button(
                                       # "📥 Upload CSV File", color="danger",  
                                    #),
                                    #width="auto",    
                                #),
                                #dbc.Col(   
                                    #dbc.Button(
                                       # "📁 Export as CSV File", color="secondary",  
                                   # ),
                                    #width="auto",    
                                # ),
                            ],
                             
                            className="align-items-center ",   
                            style={
                                "margin-right": "2px",
                                "margin-bottom": "15px",
                                   }
                        ),


                        dbc.Row(   
                            [
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='programlist_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ]
                        ),

                        html.Div(
                            id='programlist_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto', 
                                'overflowY': 'auto',   
                                'maxHeight': '1000px',
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
        Output('programlist_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('programlist_filter', 'value'),
    ]
)
def programlist_loadlist(pathname, searchterm):
    if pathname == '/program_list':
        base_sql = """  
            SELECT
                pd.pro_degree_shortname AS "Degree Program",
                c.college_name AS "College",
                du.deg_unit_shortname AS "Department",
                cl.cluster_shortname AS "Cluster",
                pt.programtype_name AS "Program Type",
                string_agg(ab_id, ', ') AS "Applicable Accreditation Body ID"
            FROM
                eqateam.program_details pd
                INNER JOIN public.college c ON pd.pro_college_id = c.college_id
                INNER JOIN public.deg_unit du ON pd.pro_department_id = du.deg_unit_id
                INNER JOIN public.clusters cl ON pd.pro_cluster_id = cl.cluster_id
                INNER JOIN eqateam.program_type pt ON pd.pro_program_type_id = pt.programtype_id,
                LATERAL (
                    SELECT jsonb_array_elements_text(pd.pro_accreditation_body_id) AS ab_id
                ) AS j
            WHERE
                1 = 1
        """

        values = []
        if searchterm:
            like_pattern = f"%{searchterm}%"
            additional_conditions = """
                AND (
                    pd.pro_degree_shortname ILIKE %s
                    OR c.college_name ILIKE %s
                    OR du.deg_unit_shortname ILIKE %s
                    OR cl.cluster_shortname ILIKE %s
                )
            """
            values.extend([like_pattern, like_pattern, like_pattern, like_pattern])
            base_sql += additional_conditions

        final_sql = base_sql + " GROUP BY pd.pro_degree_shortname, c.college_name, du.deg_unit_shortname, cl.cluster_shortname, pt.programtype_name ORDER BY pd.pro_degree_shortname"

        # Print the final SQL query and values for debugging
        print("Final SQL Query:", final_sql)
        print("Values:", values)

        cols = ["Degree Program", "College", "Department", "Cluster", "Program Type", "Applicable Accreditation Body ID"]

        df = db.querydatafromdatabase(final_sql, values, cols)

        # Print the resulting DataFrame for debugging
        print("Resulting DataFrame:")
        print(df)

        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate