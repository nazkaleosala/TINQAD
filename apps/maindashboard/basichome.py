import dash_bootstrap_components as dbc
from dash import  html, dcc 

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
from datetime import datetime 
import calendar 



def create_time_date_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(id="time", style={"font-size": "2em", "font-weight": "bold", "text-align": "center", "margin-bottom": "0"}),
                html.P(id="date", style={"text-align": "center", "margin-top": "0"}),
            ]
        ),
        className="mb-3",
        style={"backgroundColor": "#FFFFFF"}
    )

def get_month_range():
    today = datetime.today()
    # Get the first day of the current month
    start_of_month = datetime(today.year, today.month, 1)
    # Get the last day of the current month
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return start_of_month, end_of_month

   

layout = html.Div(
    [
        html.Div(  
                [
                dcc.Store(id='homeid_store', storage_type='session', data=0),
                ]
            ),
        dbc.Row(
            [
                cm.sidebar,
                html.H5(html.B("👋 Welcome!")), 
                html.Br(), 
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                create_time_date_card(),
                                dcc.Interval(
                                id="interval-component",
                                interval=1*1000,  # in milliseconds
                                n_intervals=0
                                )
                            ]
                        )
                    ],
                    className="mb-3",
                    style={"backgroundColor": "#FFFFFF"},
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

 