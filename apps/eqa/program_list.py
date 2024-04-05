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
                                dbc.Col(   
                                    dbc.Button(
                                        "📁 Upload CSV File", color="danger",  
                                    ),
                                    width="auto",    
                                ),
                                dbc.Col(   
                                    dbc.Button(
                                        "💾 Export as CSV File", color="secondary",  
                                    ),
                                    width="auto",    
                                ),
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

                        dbc.Row(  
                            [
                                 dbc.Col(   
                                    html.Div(
                                        "Table with names will go here.",
                                        id='programlist_table',
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



