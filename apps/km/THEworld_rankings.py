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

THEworldranking_data = pd.DataFrame({
    "Office": [
        "Human Resource and Development Office",
        "Office of the University Registrar",
        "Computerized Registration System",
        "Office of Scholarship and Grants",
        "Quality Assurance Office"
    ],
    "Last Accessed": [
        "March 24, User A",
        "March 24, User A",
        "March 24, User A",
        "March 24, User A",
        "March 24, User A"
    ],
    "Status": [
        "For Revision",
        "Checked",
        "For Checking",
        "For Checking",
        "Checked"
    ],
    "Action": [
        "check submission",
        "check submission",
        "check submission",
        "check submission",
        "check submission"
    ]
})
 
  
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("THE WORLD RANKINGS"),
                        html.Hr(),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dash_table.DataTable(
                                        id='criteria-table',
                                        columns=[
                                            {"name": i, "id": i} for i in THEworldranking_data.columns
                                        ],
                                        data=THEworldranking_data.to_dict('records'),
                                        style_header={'fontWeight': 'bold'},
                                        style_data_conditional=[
                                            {
                                                'if': {'column_id': 'Last Accessed'},
                                                'color': 'blue'
                                            },
                                            {
                                                'if': {'column_id': 'Action'},
                                                'color': 'green'
                                            }
                                        ]
                                    ),
                                    width=12
                                )
                            ],
                            className="mb-3",
                        ),
                    ], 
                    width=9,  style={'marginLeft': '15px'}
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