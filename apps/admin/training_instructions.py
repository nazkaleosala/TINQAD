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


# Define the initial content of the instructions
initial_body_content = """
Please submit original copies of the following as well. Forms will be sent by the QAO Admin Team:

- One (1) copy of the Liquidation Report Form - with wet signature of payee
- Two (2) copies of the Actual Itinerary of Travel (AIoT) - with wet signatures
- Two (2) copies of the Certificate of Travel Completed (CTC) - with wet signatures
- Original Copies of Boarding Passes (for trainings which required local and international flights)
- For Grab/taxi expenses below PhP 300, please also submit the physical copy of the Reimbursement Expense Receipt - with wet signatures
- Any other Official Receipt that are not digitally issued

You may submit the following documents to our office:
UPD Quality Assurance Office
Room 411-412 National Engineering Center (Juinio Hall)
Osmeña Ave., cor. Agoncillo St., UP Diliman, Quezon City

We recommend bringing a 'receiving copy' as well for proper accountability. Once you have submitted all the digital and physical documents, you may upload a 'receiving copy' in this form as well. You may 'edit your responses' to this form to do so.

For further inquiries, you may reach us through:
qao_admin.upd@up.edu.ph
02 8981 8500 loc 2092
"""

layout = html.Div(
    [
        dbc.Row(
            [
                # Navbar
                dbc.Col(
                    cm.generate_navbar(),
                    width=2,
                    style={"paddingRight": 0}
                ),
                # Instructions box, directly beside the navbar
                dbc.Col(
                    dbc.Card(
                        id="instructions-card",
                        children=[
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.H4("Training Document Submission Reminders", className="card-title",  style={"font-size": "32px"}),
                                            html.Hr(),
                                            html.Div(
                                                id="body-div",
                                                children=initial_body_content,
                                                style={
                                                    "border": "1px solid #ccc", 
                                                    "padding": "10px", 
                                                    "borderRadius": "5px", 
                                                    "minHeight": "150px",
                                                    "overflowY": "auto",
                                                    "white-space": "pre-wrap"
                                                },
                                                contentEditable=False,
                                            )
                                        ]
                                    ),
                                    html.Div(style={"margin-top": "10px"}),
                                    html.Div(
                                        [
                                            dbc.Button("Edit", color="link", id="edit-button", n_clicks=0, style={"border": "none", "background-color": "transparent", "color": "blue", "text-decoration": "underline", "padding": 0, "margin": 0}),
                                            dbc.Button("Proceed", color="primary", id="proceed-button", href="/training/training_documents", style={"display": "inline-block"}),
                                            dbc.Button("Save", color="success", id="save-button", n_clicks=0, style={"display": "none"}),
                                            dbc.Button("Cancel", color="danger", id="cancel-button", n_clicks=0, style={"display": "none"}),
                                        ],
                                        style={"display": "flex", "justifyContent": "flex-end", "gap": "10px"},
                                    )
                                ]
                            )
                        ],
                        style={"marginBottom": "10px"}
                    ),
                    width=8
                ),
            ]
        ),
        html.Div(style={"margin-top": "20px"}),
        # Footer
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width=12
                ),
            ]
        )
    ]
)

@app.callback(
    [Output("body-div", "children"),  # Update body content
     Output("body-div", "contentEditable"),  # Toggle contentEditable property
     Output("edit-button", "style"),  # Toggle visibility of buttons
     Output("proceed-button", "style"),
     Output("save-button", "style"),
     Output("cancel-button", "style")],
    [Input("edit-button", "n_clicks"),
     Input("save-button", "n_clicks"),
     Input("cancel-button", "n_clicks")],
    [State("body-div", "children"),  # Current body content
     State("body-div", "contentEditable")],  # Current contentEditable property
    prevent_initial_call=True
)
def update_body_content(edit_clicks, save_clicks, cancel_clicks, current_content, current_editable):
    ctx = dash.callback_context

    if not ctx.triggered:
        # Default state: Edit and Proceed are visible, Save and Cancel are hidden
        return current_content, current_editable, {"display": "inline-block"}, {"display": "inline-block"}, {"display": "none"}, {"display": "none"}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "edit-button":
        # Toggle contentEditable property
        return current_content, not current_editable, {"display": "none"}, {"display": "none"}, {"display": "inline-block"}, {"display": "inline-block"}
    elif button_id == "save-button":
        # Update body content with edited text
        return current_content, False, {"display": "inline-block"}, {"display": "inline-block"}, {"display": "none"}, {"display": "none"}
    elif button_id == "cancel-button":
        # Revert any changes made by returning the original content
        return initial_body_content, False, {"display": "inline-block"}, {"display": "inline-block"}, {"display": "none"}, {"display": "none"}