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


checklist_card = dbc.Col(
    dbc.Card(
        dbc.CardBody(
            dcc.Checklist(
                id='criteria_list',
                options=[],
                inline=True,
                labelStyle={'marginRight': '10px'}  # Adjust the margin as needed
            )
        ),
        style={
            'border': '1px solid #ccc',  # Optional: custom border styling
            'padding': '10px',  # Optional: custom padding for the card body
            'background-color': '#f9f9f9'  # Optional: background color
        },
    ),
    width=12  # Adjust the column width to fit the content
)




layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("SDG IMPACT RANKINGS"),
                        html.Hr(), 

                        dbc.Row(   
                            [
                                
                                
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='add_criteria_filter',
                                        placeholder='🔎 Search by degree program',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),

                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add Criteria", color="primary", 
                                        href='/add_criteria', 
                                    ),
                                    width="auto",    
                                    
                                ),
                            ]
                        ),

                         
                         
                        html.Div(
                            id='add_criteria_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        ),

                        html.Div(
                            [
                                html.Br(),    
                                # Heading with a button on the same row
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.H5(html.B("Manage Approved Evidence")),
                                            width=8,
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Deselect Criteria Checkboxes",
                                                id="deselect_button",
                                                color="danger",
                                                size="sm",
                                            ),
                                            width="auto",
                                            style={"textAlign": "right"},   
                                        ),
                                    ],
                                    justify="between",  
                                ),
                                html.Br(),   
                                
                                dbc.Row(
                                    [
                                        checklist_card,  
                                    ],
                                ),
                                
                                
                            ],
                        ),

                        html.Div(
                            id='manageevidence_list', 
                            style={
                                'marginTop': '20px',
                                'overflowX': 'auto'  # This CSS property adds a horizontal scrollbar
                            }
                        ),




                         html.Div(
                            [
                                html.Br(),  
                                    
                                dbc.Row(
                                    [
                                        
                                        dbc.Col(
                                            dbc.Button(
                                                "➕ Add Submission",
                                                color="primary",
                                                href='/SDGimpactrankings/SDG_submission',
                                            ),
                                            width="auto",
                                            className="mb-0",
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "✍🏻 Add Revision",
                                                color="warning",
                                                href='/SDGimpactrankings/SDG_revision',
                                            ),
                                            width="auto",
                                            className="mb-0",
                                        ),
                                    ],
                                    justify="end",  # Ensures heading is on the left and buttons on the right
                                ),
                                  
                                dbc.Col(
                                            html.H5(html.B("Submitted Evidences")),
                                            width="auto",  # Auto to keep the heading at the left
                                        ),
                            ]
                        )

                    ], width=8, style={'marginLeft': '15px'}
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






#eqa types dropdown
@app.callback(
    Output('criteria_list', 'options'),
    Input('url', 'pathname')
)
def populate_criteria_list_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/SDGimpact_rankings':
        sql ="""
        SELECT sdgcriteria_code as label, sdgcriteria_id  as value
        FROM  kmteam.SDGCriteria
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        criteria_list_types = [{'label': row['label'], 'value': row['value']} for _, row in df.iterrows()]
        return criteria_list_types
    else:
        raise PreventUpdate

#eqa deselect
@app.callback(
    Output('criteria_list', 'value'),
    [Input('deselect_button', 'n_clicks')]
)
def deselect_all_options(n_clicks):
    if n_clicks:
        # Return an empty list to deselect all options
        return []
    else:
        # Return current value if no click event has occurred
        return dash.no_update



















@app.callback(
    [
        Output('add_criteria_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('add_criteria_filter', 'value'),
    ]
)

def add_criteria_list(pathname, searchterm):
    if pathname == '/SDGimpact_rankings':  # Adjusted URL path
         
        sql = """
            SELECT 
                sdgcriteria_number AS "Criteria ID.",
                sdgcriteria_code AS "Criteria Code",
                sdgcriteria_description AS "Description"
            FROM 
                kmteam.SDGCriteria 
        """
        cols = ['Criteria ID.' , 'Criteria Code','Description']

        if searchterm:
            sql += """
                WHERE 
                    sdgcriteria_code ILIKE %s OR
                    CAST(sdgcriteria_number AS VARCHAR) ILIKE %s OR 
                    sdgcriteria_description ILIKE %s
            """
            like_pattern = f"%{searchterm}%"
            values = [like_pattern, like_pattern, like_pattern]
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
    




@app.callback(
    [
        Output('manageevidence_list', 'children')
    ],
    [
        Input('url', 'pathname'), 
        Input('criteria_list', 'value'),
    ]
)

def manageevidence_list (pathname, criteria_types):
    if pathname == '/SDGimpact_rankings':  # Adjusted URL path
         
        sql = """
            SELECT 
                sdg_evidencename AS "Evidence Name",
                (SELECT office_name FROM maindashboard.offices WHERE office_id = sdg_office_id) AS "Office",
                sdg_description AS "Description",
                (SELECT ranking_body_name FROM kmteam.ranking_body WHERE ranking_body_id = sdg_rankingbody) AS "Ranking Body",
                sdg_applycriteria AS "Applicable Criteria"
                
            FROM 
                kmteam.SDGSubmission
        """
        cols = ['Evidence Name', 'Office','Description', 'Ranking Body', 'Applicable Criteria']

         

        df = db.querydatafromdatabase(sql, [], cols) 

        # Generate the table from the DataFrame
        if not df.empty:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return [html.Div("No records to display")]
    else:
        raise PreventUpdate
    




