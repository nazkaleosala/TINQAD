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
                        html.H1("ABOUT TINQAD", style={'textAlign': 'center'}),
                        html.Hr(),
                        html.Div(
                            [
                                html.H2("Our Mission", style={'textAlign': 'center'}),
                                html.P("At TINQAD, we are committed to enhancing the operational excellence of the University of the Philippines Diliman (UPD). In alignment with the mission of the Quality Assurance Office (QAO), our platform is the vanguard of fostering improvements across various departments — academic, financial, administrative, and support services. Our aim is to elevate UPD's global standards of excellence through rigorous quality assessment and encouragement of continuous improvement in every sector.", style={'textAlign': 'justify'}),
                                html.Br(),
                                html.H2("Streamlining Quality Assurance with Data-Driven Solutions ", style={'textAlign': 'center'}),
                                #html.H5("Quality", style={'textAlign': 'center'}),
                                html.P("TINQAD stands as a testament to our dedication to quality. By offering a streamlined, integrated system, we ensure that each department within UPD operates at its highest potential. Our tools and analytics are designed to maintain and elevate the quality of services provided by the university.", style={'textAlign': 'justify'}),
                                #html.H5("Sectors", style={'textAlign': 'center'}),
                                html.P("Recognizing the diversity within UPD, TINQAD is tailored to meet the unique needs of different sectors. Whether it's academic excellence, financial management, administrative efficiency, or support service optimization, our platform provides bespoke solutions that resonate with each sector's specific demands.", style={'textAlign': 'justify'}),
                                #html.H5("Continuous Improvement", style={'textAlign': 'center'}),
                                html.P("At the heart of TINQAD is the ethos of never-ending enhancement. Our platform not only identifies areas for improvement but also tracks the progress over time. This enables departments to adapt, evolve, and continuously enhance their processes and services.", style={'textAlign': 'justify'}),
                                html.Br(),
                                html.H2("Our General Objective", style={'textAlign': 'center'}),
                                html.P("Our primary goal is to create a unified dashboard that acts as a nerve center for all teams within the QAO. This singular system facilitates effortless data collection, viewing, and tracking. By bringing all components under one roof, TINQAD simplifies workflows, enhances communication, and enables more efficient decision-making processes.", style={'textAlign': 'justify'}),
                                html.Br(),
                                html.Br(),
                            ],
                        ),

                        html.Div(
                            [
                                html.H3("Meet the Developers", style={'textAlign': 'center'}),
                                html.Img(
                                    src=app.get_asset_url('leosala1.png'),
                                    style = {
                                        'height' : '20em',
                                        'width' : '50%',
                                    }
                                ), 
                            ],
                        )
                    ], 
                    width=9, style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), 
                    width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)