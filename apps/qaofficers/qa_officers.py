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

def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  
    )


total_trained_qao = pd.DataFrame({
    "Cluster Type": ["A","B","C","D"], 
    "Year": ["2024","2024","2024","2024"],
    "Tier 1": ["12","12","12","12"],
    "Tier 2": ["5","5","5","5"],
    "Tier 3": ["6","6","6","6"]
}) 



def create_table(table_id, data, title):
    return dbc.Card(
        [
            dbc.CardHeader(html.H6(title, className="mb-0", style={'fontWeight': 'bold'})),
            dbc.CardBody(
                dash_table.DataTable(
                    id=table_id,
                    columns=[{"name": i, "id": i} for i in data.columns],
                    data=data.to_dict('records'), 
                    editable=True,  # Set to False if you don't want cells to be editable
                    row_deletable=True,  # Set to False if you don't want to allow row deletion
                )
            ),  
        ], style={'marginBottom': '20px'} 
    )

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
                        html.H1("QA OFFICERS DASHBOARD"),
                        html.Hr(),
                        dbc.Row(   
                            [
                                dbc.Col(   
                                    dbc.Button(
                                        "➕ View Data List", color="primary", 
                                        href='/QAOfficers/ViewListTrainedOfficers', 
                                    ),
                                    width="auto",    
                                    
                                )
                            ],
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(create_card("No. of faculty with QA Training"), width=12),
                            ]
                        ), 
                        
                         
                        html.Div(
                            [ 
                                create_table('trained-officers-table', total_trained_qao, "Total Trained Officers"), 
                            ]
                        ),
 
                         
                    ], 
                    width=8, style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row (
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)