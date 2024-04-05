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
from datetime import datetime

# Assuming commonmodules has a function to generate card like structures
def generate_card(header, body):
    card = dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.P(body, className="card-text"),
                ]
            ),
        ],
    )
    return card


expensetypes = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("(Supplies & Materials, Training and workshop expenses, quality assurance office (internal)"),
                    
                ],
                title="Maintenance and Other Operating Expenses (MOOE)",
            ),
            dbc.AccordionItem(
                [
                    html.P("training and workshop dropdown"),
                    
                ],
                title="Training & Workshop Expenses (External)",
            ),
            dbc.AccordionItem(
                
                [
                    html.P("equipment outlay dropdown "),
                    
                ],
                title="Equipment Outlay",
            ),
        ],
    )
)

def get_current_month():
    # Return the current month's name, e.g., "April".
    return datetime.now().strftime("%B")

def get_year_range():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return f"{previous_year}-{current_year}"



layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_navbar(), 
                    width=2 
                ),
                dbc.Col(
                    [
                        html.H1("ADMIN DASHBOARD"),
                        html.Hr(),
                        
                        dbc.Row(
                            [
                                #Accounts Card
                                dbc.Col(generate_card(html.P(html.Strong(f"ACCOUNTS {get_year_range()}")), 
                                    
                                    ""
                                        
                                    ), 
                                    width=6),

                                #Budget Card
                                dbc.Col(generate_card(
                                    html.P(
                                        [
                                            html.Span("BUDGEGT ", style={'font-weight': 'bold'}), 
                                            html.Span(get_current_month())  
                                        ]
                                    ),
                                    
                                    ""
                                                          
                                        
                                    ), 
                                    width=6),
                                
                            ],
                            className="mb-4",
                        ),
                        # Spending Overview
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("SPENDING OVERVIEW", className="mb-3"),
                                        # The details for spending overview will go here.
                                        # Using a table or list. For instance, dash_table.DataTable() can be used to create tables.
                                    ]
                                )
                            ]
                        ),
                        # Add the maintenance and other expenses section
                        dbc.Row(
                            [
                                expensetypes
                            ]
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
                
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)
