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

from dash import ALL, no_update
from datetime import datetime, timedelta
import calendar

from dash import Output, Input, State, callback_context

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





 
def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month





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





 




# -----------------------------------Announcements Content  
km_announcement_content = html.Div(
    [
        html.Div(
            id="kmann_display",
            style={
                "overflowX": "auto",
                "overflowY": "auto",
                "maxHeight": "200px",
            },
        ),
        html.Div(
            [
                html.Div(id="kmann_status"),
                html.Br(),
                dbc.Input(
                    id="kmann_header",
                    placeholder="Format: [TEAM NAME] Deadline Date, if urgent type URGENT. ex. [KM TEAM] May 05, 2024 URGENT.",
                    type="text",
                ),
                dbc.Textarea(
                    id="kmann_content",
                    placeholder="Type a message...",
                    style={"resize": "vertical"},
                    rows=5,
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button("Post", id="kmmsgspost_button", color="primary", className="mt-2"),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Button("Cancel", id="kmmsgscancel_button", color="secondary", className="mt-2"),
                            width="auto",
                        ),
                    ],
                    style={"justify-content": "flex-end"},
                ),
            ],
            id="kmann_id",
            style={"display": "none"},
        ),
    ]
)

km_announcement_footer = html.Div(
    [
        dbc.Button(
            "Add Message",
            id="kmann_footer_button",
            className="mt-2",
            color="success",
        ),
    ],
    className="d-flex justify-content-end",
)

app.layout = html.Div([km_announcement_content, km_announcement_footer, dcc.Location(id="url", refresh=False)])



@app.callback(
    Output("kmann_id", "style"),
    [Input("kmann_footer_button", "n_clicks"), 
     Input("kmmsgscancel_button", "n_clicks")],
    [State("kmann_id", "style")],  
)
def toggle_announcement_form(footer_clicks, cancel_clicks, current_style):
    ctx = callback_context  

    footer_clicks = footer_clicks or 0
    cancel_clicks = cancel_clicks or 0

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "kmann_footer_button" and footer_clicks > 0:
        return {"display": "block"}

    elif trigger_id == "kmmsgscancel_button" and cancel_clicks > 0:
        return {"display": "none"}

    raise PreventUpdate






# Callback to insert a new message into the database
@app.callback(
    Output("kmann_status", "children"),
    [Input("kmmsgspost_button", "n_clicks")],
    [State("kmann_header", "value"),  # New header input
     State("kmann_content", "value")],
)
def insert_announcement(n_clicks, kmann_header, kmann_content):
    if not n_clicks or not kmann_header or not kmann_content:
        raise PreventUpdate

    try:
        sql = """
            INSERT INTO kmteam.announcements
              (kmann_header , kmann_content, kmann_user)
            VALUES (%s, %s, NULL)   
        """

        db.modifydatabase(sql, (kmann_header, kmann_content))
        return ["Announcement posted successfully!"]

    except Exception as e:
        return [f"Error: {str(e)}"]

# Callback to fetch announcements and display them
@app.callback(
    Output("kmann_display", "children"),
    [Input("url", "pathname")],   
)
def fetch_km_announcements(pathname):
    if pathname != "/homepage":
        raise PreventUpdate

    try:
        start_of_month, end_of_month = get_month_range()

        sql = """
            SELECT kmann_header, kmann_content, kmann_user, kmann_timestamp
            FROM kmteam.announcements
            WHERE kmann_timestamp BETWEEN %s AND %s
            ORDER BY kmann_timestamp DESC
        """

        values = (start_of_month, end_of_month)
        dfcolumns = ["kmann_header", "kmann_content", "kmann_user", "kmann_timestamp"]
        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return [html.Div("No announcements this month")]

        formatted_km_announcements = []
        for row in df.itertuples(index=False):
            km_announcement_header = getattr(row, "kmann_header")
            km_announcement_content = getattr(row, "kmann_content")
            km_announcement_user = getattr(row, "kmann_user")
            km_announcement_timestamp = getattr(row, "kmann_timestamp")

            formatted_km_announcements.append(
                html.Div(
                    [
                        html.P(km_announcement_header),
                        html.P(km_announcement_content),
                        html.Small(
                            f"{km_announcement_user or 'Anonymous'}, {km_announcement_timestamp}",
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

        return formatted_km_announcements

    except Exception as e:
        return [html.Div(f"Error retrieving announcements: {str(e)}")]



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
                                dbc.Col(
                                    create_card("ANNOUNCEMENT", km_announcement_content),
                                    width=12
                                ),
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