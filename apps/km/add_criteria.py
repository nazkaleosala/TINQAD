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
from calendar import month_name


 



  


# Form layout with improvements
form = dbc.Form(
    [
        # SDG Number Selector
        dbc.Row(
            [
                dbc.Label(
                    ["SDG # ", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Select(
                        id="sdgcriteria_number",
                        options=[{"label": "Goal 1: No Poverty", "value": "1"}],
                        placeholder="Enter SDG #",
                    ),
                    width=8,
                ),
            ],
            className="mb-1",
        ),
        
        # Criteria Code Input
        dbc.Row(
            [
                dbc.Label(
                    ["Criteria Code ", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Input(
                        id="sdgcriteria_code",
                        placeholder="e.g. SDG 2.0.0",
                        type="text",
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        
        # Description Textarea
        dbc.Row(
            [
                dbc.Label(
                    ["Description ", html.Span("*", style={"color": "#F8B237"})],
                    width=4,
                ),
                dbc.Col(
                    dbc.Textarea(
                        id="sdgcriteria_description",
                        placeholder="Enter Description",
                        style={"height": "80px"},
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ),
        
        html.Br(),
        
        # Cancel and Save Buttons
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Button("Save", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto",
                ),
            ],
            className="mb-2",
            justify="end",
        ),

        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4("Criteria added."),
                ),
                dbc.ModalFooter(
                    dbc.Button("Proceed", id="proceed_button", className="ml-auto"),
                ),
            ],
            centered=True,
            id="addcriteria_successmodal",
            backdrop=True,
            className="modal-success",
        ),
    ],
    className="g-2",
)


  
 




# Layout for the Dash app
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(cm.generate_navbar(), width=2),
                dbc.Col(
                    [
                        html.H1("PROFILE"),
                        html.Hr(),
                        html.Br(),
                        form,
                        dbc.Alert(id="addcriteria_alert", is_open=False),  # Alert for feedback
                    ],
                    width=6,
                    style={"marginLeft": "15px"},
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(),
                    width={"size": 12, "offset": 0},
                ),
            ],
        ),
    ]
)
 
@app.callback(
    [
        Output('addcriteria_alert', 'color'),
        Output('addcriteria_alert', 'children'),
        Output('addcriteria_alert', 'is_open'),
        Output('addcriteria_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('sdgcriteria_number', 'value'),
        State('sdgcriteria_code', 'value'),
        State('sdgcriteria_description', 'value'), 
    ]
) 




def add_criteria(submitbtn, sdgcriteria_number, sdgcriteria_code, sdgcriteria_description):
    if not submitbtn:
        raise PreventUpdate

    # Default values
    alert_open = False
    modal_open = False
    alert_color = ""
    alert_text = ""

    # Input validation checks
    if not sdgcriteria_number:
        alert_open = True
        alert_color = "danger"
        alert_text = "Check your inputs. Please add a Criteria number."
        return [alert_color, alert_text, alert_open, modal_open]

    if not sdgcriteria_code:
        alert_open = True
        alert_color = "danger"
        alert_text = "Check your inputs. Please add a Criteria Code."
        return [alert_color, alert_text, alert_open, modal_open]

    if not sdgcriteria_description:
        alert_open = True
        alert_color = "danger"
        alert_text = "Check your inputs. Please add a Description."
        return [alert_color, alert_text, alert_open, modal_open]

    # Insert data into the database
    try:
        sql = """
            INSERT INTO kmteam.SDGCriteria(
                sdgcriteria_number, sdgcriteria_code, sdgcriteria_description
            )
            VALUES (%s, %s, %s)
        """
        values = (sdgcriteria_number, sdgcriteria_code, sdgcriteria_description)
        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = "danger"
        alert_text = "An error occurred while saving the data."
        alert_open = True

    return [alert_color, alert_text, alert_open, modal_open]