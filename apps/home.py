
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app



second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H2("LOG IN", className="card-title fw-bolder "),
            html.Br(),
            
            dbc.Label("username", html_for="username"),
            dbc.Input(type="username", id="username", ),
            
            html.Br(),
            dbc.Label("Password", html_for="password"),
            dbc.Input(type="password", id="password"),
            
            html.Br(),
            dbc.Row(
                dbc.Col(
                    dbc.Button("Log in", color="primary", className="fw-bolder", href='/homepage'),
                    width={'size': 4, 'offset': 8},  # Adjust as needed
                    className="d-flex justify-content-end"
                )
            ),
            
            html.Br(),
            html.Br(),

            html.H4("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-danger" ),
            html.P ("The Total Integrated Network for Quality Assurance and Development (TINQAD) is a centralized network that allows the singular monitoring of the Quality Assurance teams activities."),
            
            html.Br(),

            html.P("Contact Us", className= "fw-bolder " ),
            html.P("🏢4th Floor, 411-412. National Engineering Center, University of the Philippines, Diliman. "),
            html.P("📧 qa.upd@up.edu.ph"),
            html.P("📞(02) 9891-8500 local 2092"),
                             
        ]
    )
)


layout = dbc.Row(
    [
        dbc.Col(
            html.Div(
            [
                html.Img(
                    src=app.get_asset_url('bg1.png'),
                    style = {
                        'height' : '50em',
                        'width' : '100%',
                        'z-index' : '-1',
                        'mask-image' : 'linear-gradient(to bottom, rgba(0, 0, 0, 1.0) 50%, transparent 100%)'
                    }
                ),

                html.Img(src=app.get_asset_url('qao-logo-icon.png'),
                        style = {
                            'max-width': '15vw',
                            'margin': 'auto',  # Center the image horizontally
                            'display': 'block'  # Make sure it's displayed as a block element
                        },
                        ),
                html.H5("Total Integrated Network for Quality Assurance and Development", className="fw-bolder text-center"),
                html.P("Copyright © 2024. Quality Assurance Office, University of the Philippines", className="text-center"),
               
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.A("About TINQAD", href="/about-us", className="link-style"), " • ",
                                html.A("Main Website", href="https://qa.upd.edu.ph/", className="link-style"), " • ",
                                html.A("Facebook", href="https://www.facebook.com/QAODiliman", className="link-style"), " • ",
                                html.A("LinkedIn", href="https://www.linkedin.com/company/quality-assurance-office/about/", className="link-style")
                                
                            ],
                            width = "auto"
                        ),
                    ],
                    style = {'margin' : 'auto'},
                    align = 'center', justify = 'center'
                ),
                
                 

            ],
            id = 'bg',
            style = {
                'position' : 'relative',
                'margin-left' : '-2em',
                'margin-top' : '-5em',
                'max-width' : '70vw',
                'position' : 'auto',
                'overflow' : 'hidden'
            }
        ),
        ), 
        dbc.Col(
            [
                second_card,
                   
            ], width=3,)
    ]
)       

        
        
