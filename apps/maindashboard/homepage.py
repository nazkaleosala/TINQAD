import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
import psycopg2
from dash.dependencies import Input, Output, State
from dash.dependencies import MATCH
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from dash import ALL, no_update
from datetime import datetime, timedelta
import calendar






# Function to get the start and end of the current week
def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month

#----------------------------------- Team Messages Content
team_messages_content = html.Div(
    [
        html.Div(id="teammsgs_display",
                 style={
                    'overflowX': 'auto', 
                    'overflowY': 'auto',   
                    'maxHeight': '200px',
                    }),  
        
        html.Div(
            [
                html.Div(id="teammsgs_status"),  
                dbc.Textarea(
                    id="teammsgs_content",
                    placeholder="Type a message...",
                    style={"resize": "vertical"},
                    rows=5,
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Post", id="teammsgspost_button", color="success", className="mt-2"),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button("Cancel", id="teammsgscancel_button", color="warning", className="mt-2"),
                            width="auto",
                        ),
                    ],
                    style={"justify-content": "flex-end"},
                ),
            ],
            id="teammsgs_id",
            style={"display": "none"},  # Initially hidden
        ),
    ]
)

team_messages_footer = html.Div(
    [
        dbc.Button(
            "Add Message",
            id="teammsgs_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)
app.layout = html.Div([team_messages_content, team_messages_footer, dcc.Location(id="url", refresh=False)])

# Callback to toggle the textarea visibility
@app.callback(
    Output("teammsgs_id", "style"),
    [Input("teammsgs_footer_button", "n_clicks")],
    [State("teammsgs_id", "style")],
)
def toggle_textarea(n_clicks, current_style):
    if not n_clicks:
        raise PreventUpdate
    
    return {"display": "block" if current_style["display"] == "none" else "none"}

# Callback to insert a new message into the database
@app.callback(
    Output("teammsgs_status", "children"),   
    [Input("teammsgspost_button", "n_clicks")],
    [State("teammsgs_content", "value")],
)
def insert_team_message(n_clicks, message_content):
    if not n_clicks:
        raise PreventUpdate

    try:
        sql = """
            INSERT INTO maindashboard.teammessages (teammsgs_content, teammsgs_user)
            VALUES (%s, NULL)
        """
        
        values = (message_content, )

        # Insert the message into the database
        db.modifydatabase(sql, values)
        
        return ["Message posted successfully!"]

    except Exception as e:
        return [f"Error: {str(e)}"]









@app.callback(
    Output("teammsgs_display", "children"),
    [Input("url", "pathname")],   
)
def fetch_team_messages(pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
         
        start_of_month, end_of_month = get_month_range()
        
         
        sql = """
            SELECT teammsgs_content, teammsgs_user, teammsgs_timestamp
            FROM maindashboard.teammessages
            WHERE teammsgs_timestamp BETWEEN %s AND %s
            ORDER BY teammsgs_timestamp DESC
        """

         
        values = (start_of_month, end_of_month)
        dfcolumns = ["teammsgs_content", "teammsgs_user", "teammsgs_timestamp"]

        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No messages this week")]

        formatted_messages = [] 
        for row in df.itertuples(index=False): 
            content = getattr(row, "teammsgs_content")
            user = getattr(row, "teammsgs_user")
            timestamp = getattr(row, "teammsgs_timestamp")

            formatted_messages.append(
                html.Div(
                    [
                        html.P(content),  # The main message content
                        html.Small(
                            f"{user or 'Anonymous'}, {timestamp}",
                            style={
                                "text-align": "right",
                                "font-style": "italic",
                            },
                        ),  
                        html.Hr(),
                    ],
                    style={"margin-bottom": "10px"},  
                )
            )
        
        return formatted_messages  

    except Exception as e:
        return [html.Div(f"Error retrieving messages: {str(e)}")]










# -----------------------------------Announcements Content  
 


































card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="|   Team Messages   |", tab_id="tab-team-msg"),
                    dbc.Tab(label="|   Announcements   |", tab_id="tab-announcements"),
                ],
                id="card-tabs",
                active_tab="tab-team-msg",
            )
        ),
        dbc.CardBody(id="card-body-content"),  # Will be updated dynamically
        dbc.CardFooter(id="card-footer-content"),  # Will be updated dynamically
    ] 
)



# Callback to update card content
@app.callback(
    [Output("card-body-content", "children"),
     Output("card-footer-content", "children")],
    [Input("card-tabs", "active_tab")]
)
def update_card_content(active_tab):
    if active_tab == "tab-team-msg":
        return team_messages_content, team_messages_footer
    elif active_tab == "tab-announcements":
        return team_messages_content, team_messages_footer
    else:
        return "Tab not found", None  # Fallback case
 
 
 
timeline_card = dbc.Card(
    [
        dbc.CardHeader("TIMELINE", className="text-center text-bold"),
        dbc.CardBody(
            [
                html.P("Some exciting event happening soon.", className="card-text"),
            ]
        ),
    ],
    className="mb-3"
)

upcomingevents_card = dbc.Card(
    [
        dbc.CardHeader("UPCOMING EVENTS", className="text-center text-bold"),
        dbc.CardBody(
            [
                html.P("Some exciting event happening soon.", className="card-text"),
            ]
        ),
    ],
    className="mb-3"
)





layout = html.Div(
    [
        dcc.Store(id='stored-messages', storage_type='memory'),
        dcc.Store(id='message-store', data=[]),
        
        html.Div(id='post-trigger', style={'display': 'none'}),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_navbar(), 
                    width=2 
                ),
                dbc.Col(
                    [   # Main content goes here
                        html.H1("WELCOME, PIKA!", className="my-3"),
                        dbc.Row(
                            dbc.Col(
                                card, 
                                width=8, sm=12
                            )
                        ),
                        html.Br(),
                    
                    dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/admin_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#31356E', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Administration Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
                                                            ]
                                                        )
                                                    ],
                                                    align="center"
                                                ),
                                            ] 
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"}
                                    ),
                                    href='/administration_dashboard'
                                    ),
                                    width=6, md=6, sm=12
                                ),
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/eqa_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#F8B237', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("External Quality Assurance Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
                                                            ]
                                                        )
                                                    ],
                                                    align="center"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"}
                                    ),
                                    href='/eqa_dashboard'
                                    ),
                                    width=6, md=6, sm=12
                                ),
                            ],
                            className="mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/iqa_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#D37157', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Internal Quality Assurance Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
                                                            ]
                                                        )
                                                    ],
                                                    align="center"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"}
                                    ),
                                    href='/iqa_dashboard'
                                    ),
                                    width=6, md=6, sm=12
                                ),
                                dbc.Col(
                                    html.A(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(html.Img(src=app.get_asset_url("icons/km_icon.png"), style={"height": "100px"})),
                                                        dbc.Col(
                                                            [
                                                                html.Div(style={'background-color': '#39B54A', 'width': '100%', 'height': '20px'}),  # Rectangle
                                                                html.H5("Knowledge Management Team", className="card-title fw-bold text-dark", style={"text-align": "right",'text-decoration': 'none'})
                                                            ]
                                                        )
                                                    ],
                                                    align="center"
                                                ),
                                            ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"}
                                    ),
                                    href='/km_dashboard'
                                    ),
                                    width=6, md=6, sm=12
                                ),
                            ],
                            className="mb-3"
                        ),
                    ],
                    width=7,  
                ),
                dbc.Col(
                    [   # Right column for the timeline card
                        dbc.Row ([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(style={'background-color': '#7A0911', 'width': '100%', 'height': '20px'}),  # Rectangle
                                            html.A(
                                                html.H5("Quality Assurance Officers", className="card-title fw-bold text-dark text-center"), 
                                                href='/qa_officers',
                                                style={'text-decoration': 'none'}
                                            ),
                                        
                                        ]
                                        ),
                                        className="mb-3",
                                        style={"backgroundColor": "#FFFFFF"},
                                    ),
                                    
                                ),
                        
                        ]),
                        timeline_card,  # timeline card component
                        upcomingevents_card,
                    ],
                    width=3,  md=3, sm=12
                ),
            ],
            className="mb-3",
            style={'padding-bottom': '2rem'}
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
