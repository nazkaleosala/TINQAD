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

 
def create_table(headers, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in headers],
        style_header={'fontWeight': 'bold'}, 
    )


circle_style = {
    "height": "20px",  # Adjust the diameter of the circle
    "width": "20px",
    "borderRadius": "50%",
    "display": "inline-block",
    "marginRight": "10px",
    "verticalAlign": "middle",
}


links = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#39B54A"}),  # Green circle
                            html.Span("Sustainable Development Goals Impact Rankings",
                                style={"verticalAlign": "middle"}),

                        ],
                        href="/SDGimpact_rankings ",
                        style={"color": "black", "textDecoration": "none"}  # Optional style to remove underline and adjust color
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ),
         
         
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#6495ed"}),  # Blue circle
                            html.Span("QS University Rankings",
                                style={"verticalAlign": "middle"}),
                        ],
                        href="/QSworld_rankings",
                        style={"color": "black", "textDecoration": "none"}   
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        [
                            html.Div(style={**circle_style, "backgroundColor": "#ffa500"}),  # Orange circle
                            html.Span("THE World University Rankings",
                                style={"verticalAlign": "middle"}),
                        ],
                        href="/THEworld_rankings",
                        style={"color": "black", "textDecoration": "none"}   
                    ),
                    width="auto",
                    align="center",
                ),
            ],
            className="align-items-center mb-2",  
        ), 
    ],
    style={"textAlign": "left"}   
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
                        html.H1("KM DASHBOARD"),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(create_card("ANNOUNCEMENT"), width=12),
                            ]
                        ), 
                        
                        dbc.Row(
                            [
                                dbc.Col(create_card(
                                    dbc.Col(
                                    [
                                        "Recent Activities", 
                                    ]
                                )
                                ), width=7),

                                dbc.Col(create_card(
                                    dbc.Col("Ranking Body Categories"),
                                    links
                                ), width=5),
                                
                            ]
                        ),
                         
                         
                    ], 
                    width=9, style={'marginLeft': '15px'}
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