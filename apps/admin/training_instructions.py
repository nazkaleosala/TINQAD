import dash_bootstrap_components as dbc
from dash import html, Input, Output 
from dash import callback_context 

import dash
from apps import commonmodules as cm
from app import app
from apps import dbconnect as db 





layout = html.Div(
    [
        dbc.Row(
            [
                # Navbar
                cm.sidebar,

                dbc.Col(
                    dbc.Card(
                        id="instructions-card",
                        children=[
                            dbc.CardBody(
                                [
                                    html.H4(
                                        "Training Document Submission Reminders",
                                        className="card-title",
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        id="traininginstructions_display",
                                        style={
                                            "border": "1px solid #ccc",
                                            "padding": "10px",
                                            "borderRadius": "5px",
                                            "minHeight": "150px",
                                            "overflowY": "auto",
                                            "white-space": "pre-wrap",
                                        },
                                    ),

                                    html.Br(),
                                    html.Div(
                                        [
                                            dbc.Checkbox(id="accept_checkbox", className="mr-2"),
                                            html.Label("I have read and accept all of the instructions carefully."),
                                            dbc.Button("Proceed", id="proceed_button", color="primary", href="/training_documents?mode=add", disabled=True),
                                        ],
                                        style={"display": "flex", "justify-content": "flex-end", "gap": "10px"},
                                    ),

                                ],
                            ),
                        ],
                    ),
                    width=8,
                ),
            ]
        ),
        html.Div(style={"margin-top": "20px"}),

        html.Br(),
        html.Br(),
        html.Br(),
        # Footer
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width=12),
            ],
        ),
    ],
)

# Callback to fetch announcements and display them
@app.callback(
    Output("traininginstructions_display", "children"),
    [Input("url", "pathname")],
)
def fetch_announcements(pathname):
    if pathname == "/training_instructions":
        sql = """
            SELECT trinstructions_content
            FROM adminteam.training_instructions
            ORDER BY trinstructions_id DESC
            LIMIT 1;
        """

        values = ()
        dfcolumns = ["trinstructions_content"]
        df = db.querydatafromdatabase(sql, values, dfcolumns)

        instruction_content = df.loc[0, "trinstructions_content"]
        return instruction_content


# Define the callback to enable/disable the button
@app.callback(
    Output("proceed_button", "disabled"),
    Input("accept_checkbox", "value")
)
def toggle_proceed_button(checked): 
    return not checked if checked is not None else True