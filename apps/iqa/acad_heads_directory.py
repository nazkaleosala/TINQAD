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
                        html.H1("ACADEMIC UNIT HEADS DIRECTORY"),
                        html.Hr(),
                        
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ Add New", color="primary", 
                                        href='/acadheadsdirectory/acadheads_profile', 
                                    ),
                                    width="auto",    
                                    
                                ),
                                dbc.Col(  
                                    dbc.Input(
                                        type='text',
                                        id='acadheads_filter',
                                        placeholder='🔎 Search by name, email, position, etc',
                                        className='ml-auto'   
                                    ),
                                    width="8",
                                ),
                            ],
                             
                            className="align-items-center",   
                            justify="between",  
                        ),

                        dbc.Row(  
                            [
                                 dbc.Col(   
                                    html.Div(
                                        "Table with names will go here.",
                                        id='acadheadsdirectory_list',
                                        style={'marginTop': '20px'} 
                                    ),
                                    width=12  
                                )
                            ],
                                     
                        ),

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




@app.callback(
    [
        Output('acadheadsdirectory_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('acadheadsdirectory_namefilter', 'value'),
    ]
    )

def moviehome_loadmovielist(pathname, searchterm):
    if pathname == '/movies':
        sql = """ SELECT movie_name, genre_name, movie_id
            FROM movies m
                INNER JOIN genres g ON m.genre_id = g.genre_id
            WHERE
                NOT movie_delete_ind
        """
        values = []
        cols = ['Movie Title', 'Genre', 'ID']
        
        if searchterm:
            # We use the operator ILIKE for pattern-matching
            sql += " AND movie_name ILIKE %s"

            # The % before and after the term means that
            # there can be text before and after
            # the search term
            values += [f"%{searchterm}%"]
        
        
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for movie_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit',
                href=f'movies/movies_profile?mode=edit&id={movie_id}',
                            size='sm', color='warning'),
                            style={'text-align': 'center'}
                    )
                ]   
            df['Action'] = buttons
            # remove the column ID before turning into a table
            df = df[['Movie Title', 'Genre', "Action"]]


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        
        else:
            return ["No records to display"]
    
    
    
    else:
        raise PreventUpdate