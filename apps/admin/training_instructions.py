import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, Input, Output, State, callback_context
from dash.exceptions import PreventUpdate
import psycopg2
import os

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
from dash.dash_table.Format import Group









layout = html.Div(
    [
        dbc.Row(
            [
                # Navbar
                dbc.Col(
                    cm.generate_navbar(),
                    width=2,
                    style={"paddingRight": 0},
                ),
                
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
                                        id="trinstructions_content",
                                        style={
                                            "border": "1px solid #ccc",
                                            "padding": "10px",
                                            "borderRadius": "5px",
                                            "minHeight": "150px",
                                            "overflowY": "auto",
                                            "white-space": "pre-wrap",
                                        },
                                        contentEditable=False,
                                    ),
                                    html.Br(),
                                    html.Div(
                                        [
                                            dbc.Button("Edit", id="edit_button", n_clicks=0, color="link"),
                                            dbc.Button("Proceed", id="proceed_button", color="primary", href="/training/training_documents"),
                                            dbc.Button("Save", id="save_button", n_clicks=0, style={"display": "none"}),
                                            dbc.Button("Cancel", id="cancel_button", n_clicks=0, style={"display": "none"}),
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
        # Footer
        dbc.Row(
            [
                dbc.Col(cm.generate_footer(), width=12),
            ],
        ),
    ],
)

 
 
@app.callback(
    Output("trinstructions_content", "children"),
    [Input("url", "pathname")],   
)
def fetch_instructions(pathname):
    if pathname != "/training_documents":
        raise PreventUpdate

    try:
        sql = """
        SELECT trinstructions_content
        FROM adminteam.training_instructions
        ORDER BY trinstructions_id DESC
        LIMIT 1;
        """
        values = ()
        dfcolumns = ["trinstructions_content"]  # expected column name

        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.empty:
            return ["No training instructions available."]

        # Retrieve the training instruction content
        instruction_content = df.loc[0, "trinstructions_content"]

        return [html.Div(instruction_content, contentEditable=False)]
   
    except Exception as e:
        return [html.Div(f"Error retrieving training instructions: {str(e)}")]