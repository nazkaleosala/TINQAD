import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.dependencies import MATCH
from dash.exceptions import PreventUpdate
import pandas as pd

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db

from dash import ALL, no_update

from datetime import datetime

# Components for the message functionality
add_message_button = dbc.Button(
    "Add Message",
    id="show-input-button",
    className="mt-2",
    style={"backgroundColor": "#0A4323", "borderColor": "#0A4323", "display": "block"}
)

message_input_div = html.Div(
    [
        dbc.Textarea(
            id="message-input",
            placeholder="Type a message...",
            style={"resize": "vertical"},  # Allow vertical resizing
            rows=5  # Set the initial number of rows
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(), width="auto"),  # Empty column to push buttons to the right
                dbc.Col(
                    [
                        dbc.Button("Post", id="post-message-button", color="success", className="mr-1 mt-2"),
                        dbc.Button("Cancel", id="cancel-message-button", color="secondary", className="mt-2", style={"margin-left": "5px"}),  # Add margin to the left for spacing
                    ],
                    width="auto",
                ),
            ],
            style={"margin-top": "5px", "justify-content": "flex-end"}  # Align buttons to the right
        )
    ],
    id="message-input-div",
    style={"display": "none"}  # Hidden initially
)
messages_display = html.Div(id="messages-display", children="No team messages")


all_messages = []
MAX_MESSAGES = 100

# Team Messages Content
team_messages_content = html.Div([
    messages_display,
    html.Div(id="message-input-area", children=message_input_div)
])

team_messages_footer = html.Div([add_message_button], className="d-flex justify-content-end")

# Announcements Content (adjust as needed)
announcements_content = html.Div([
    html.P("Announcements content goes here...")  # Placeholder, replace with actual content
])

announcements_footer = html.Div()


card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Team Messages", tab_id="tab-team-msg"),
                    dbc.Tab(label="Announcements", tab_id="tab-announcements"),
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
        return announcements_content, announcements_footer
    else:
        return "Tab not found", None  # Fallback case

@app.callback(
    [Output('message-input-div', 'style'),
     Output('show-input-button', 'style')],
    [Input('show-input-button', 'n_clicks'),
     Input('cancel-message-button', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_input_area(show_clicks, cancel_clicks):
    # Toggle the visibility based on which button was clicked
    if show_clicks and cancel_clicks:
        # If both buttons have been clicked, check which was clicked last
        if show_clicks > cancel_clicks:
            # If "Add Message" was clicked after "Cancel", show the input area
            return {"display": "block"}, {"display": "none"}
        else:
            # Otherwise, hide the input area
            return {"display": "none"}, {"display": "block"}
    elif show_clicks:
        # If only "Add Message" was clicked, show the input area
        return {"display": "block"}, {"display": "none"}
    elif cancel_clicks:
        # If only "Cancel" was clicked, hide the input area
        return {"display": "none"}, {"display": "block"}

    # Default state if none of the buttons have been clicked
    return {"display": "none"}, {"display": "block"}

#Post message    
@app.callback(
    [Output('messages-display', 'children'), 
     Output('message-input', 'value')],  # Add an output for the message input
    [Input('post-message-button', 'n_clicks')],
    [State('message-input', 'value'), 
     State('messages-display', 'children')],
    prevent_initial_call=True
)
def post_message(n_clicks, message, displayed_messages):
    if not message:
        return dash.no_update, message 

    timestamp = datetime.now().strftime("%d %B %Y, %I:%M:%S %p")
    message_id = f"message-{n_clicks}"

    # Create a text-based "Delete" link
    delete_link = html.A(
        html.Img(
            src=app.get_asset_url("delete_icon.png"),  # Assuming 'delete_icon.png' is in the assets folder
            style={"height": "20px", "width": "20px"}  # Adjust the size as needed
        ),
        href="#",
        id={"type": "delete", "index": message_id},
        style={"cursor": "pointer", "display": "block", "text-align": "right"}
    )

    # Construct the formatted message with the Delete link on the right
    formatted_message = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(message, id={"type": "message-text", "index": message_id}),
                dbc.Textarea(id={"type": "edit-message-input", "index": message_id}, style={"display": "none"}, value=message),
                html.P("Last updated: " + timestamp, style={'fontSize': 'small', 'color': '#888888'})
            ], width=10),
            dbc.Col(delete_link, width=2, className="text-right")  # Place the delete link in its own column
        ]),
        html.Hr()  # Horizontal line separator
    ], id={"type": "message-container", "index": message_id})

    new_message = [formatted_message]
    # Check if there are existing messages
    if displayed_messages and displayed_messages != "No team messages":
        updated_messages = displayed_messages + new_message
    else:
        updated_messages = new_message

    return updated_messages, ""


#Delete
def generate_delete_callback(index):
    @app.callback(
        Output({'type': 'message-container', 'index': index}, 'style'),
        [Input({'type': 'delete', 'index': index}, 'n_clicks')],
        prevent_initial_call=True
    )
    def delete_message(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        # Hide the message container
        return {"display": "none"}

# Generate callbacks for each message
for i in range(MAX_MESSAGES):  # Replace MAX_MESSAGES with the maximum expected number of messages
    generate_delete_callback(f"message-{i}")


#timeline column
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
                                                        dbc.Col(html.Img(src=app.get_asset_url("admin_icon.png"), style={"height": "100px"})),
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
                                                        dbc.Col(html.Img(src=app.get_asset_url("eqa_icon.png"), style={"height": "100px"})),
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
                                                        dbc.Col(html.Img(src=app.get_asset_url("iqa_icon.png"), style={"height": "100px"})),
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
                                                        dbc.Col(html.Img(src=app.get_asset_url("km_icon.png"), style={"height": "100px"})),
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