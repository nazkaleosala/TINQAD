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

import plotly.graph_objs as go

def create_card(title, content=None):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(content if content else "")
        ],
        className="mb-3",  # Add space below each card
    )
 
def create_table(headers, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in headers],
        style_header={'fontWeight': 'bold'}, 
    )

def generate_donut_chart(labels, values):
    # Define color scale for the pie chart
    colors = ['#F8B237', '#E4E4E4', '#39B54A']
    trace = go.Pie(labels=labels, values=values, hole=0.4, marker=dict(colors=colors))
    return {'data': [trace], 'layout': go.Layout(title='', showlegend=False)}

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
                        html.H1("EQA DASHBOARD"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("Summary of Degree Programs with EQA"),  # Bold only this part
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}  # Adjust font size
                                                )
                                            ),
                                            dbc.CardBody(
                                                [
                                                    html.P("40/100 programs assessed", className="card-text"),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dcc.Graph(id='donut-chart')
                                                            ),
                                                            dbc.Col(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#F8B237', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are currently accomplishing their accreditation", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#39B54A', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are on schedule for next accreditation", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                    html.Div(
                                                                        [
                                                                            dbc.Col(
                                                                                html.Div(style={'backgroundColor': '#E4E4E4', 'borderRadius': '10px', 'height': '50px', 'width': '50px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                                                                            ),
                                                                            dbc.Col(
                                                                                html.P("Units are yet to commence accreditation requirements", style={'marginLeft': '5px', 'fontSize': '0.9rem', 'textAlign': 'left'})
                                                                            )
                                                                        ],
                                                                        style={'marginBottom': '5px', 'display': 'flex', 'alignItems': 'center'}
                                                                    ),
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                    
                                                ]
                                            ),
                                        ]
                                    ),
                                    width=8,
                                    className="mb-3"
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("SAR Submissions 2024"),  # Bold only this part
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}  # Adjust font size
                                                )
                                            ),
                                            dbc.CardBody(),
                                        ]
                                    ),
                                    width=4
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                html.H3(
                                                    [
                                                        html.Strong("Assessment Schedule"),  # Bold only this part
                                                    ],
                                                    className="mb-0",  # Remove bottom margin
                                                    style={'fontSize': '1.5rem'}  # Adjust font size
                                                )
                                            ),
                                            dbc.CardBody(
                                                create_table(headers=["Program Name", "Type of Assessment", "Scheduled Assessment Date"], id="assessment-schedule-table")
                                            ),
                                        ]
                                    ),
                                    width=12
                                ),
                            ]
                        ),
                    ]
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

@app.callback(
    Output('donut-chart', 'figure'),
    [Input('donut-chart', 'id')]
)
def update_donut_chart(id):
    # Assuming you have a function to retrieve data from the database
    # and format it as required
    labels = ['For Checking', 'Already Checked', 'No Status Yet']
    values = [30, 40, 30]  # Example data, replace with data from database
    return generate_donut_chart(labels, values)
