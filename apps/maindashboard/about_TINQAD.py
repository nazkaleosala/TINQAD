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




def create_card(name, image_url, description, linkedin_url): 
    return dbc.Card(
        [
            dbc.CardImg(src=image_url, top=True, style={'object-fit': 'cover', 'display': 'block', 'width': '100%', 'height': 'auto'}),
            dbc.CardBody(
                [
                    html.H6(name, className="card-title", style={'fontWeight': 'bold'}), 
                    html.P(description, className="card-text "),
                    html.A(
                        html.Img(
                            src=app.get_asset_url('linkedinicon1.png'),
                            style={'height': '1.5em', 'width': 'auto', 'margin-top': '0.5em'}
                        ),
                        href=linkedin_url,
                        target="_blank"
                    ),
                ]
            ),
        ],
        className="mb-3",
    )

 
cards = [
    create_card("Naomi Takagaki", 
                app.get_asset_url('takagaki1.png'),  
                """
                Project Manager and Lead Developer
                                            """,
                "https://www.linkedin.com/in/naomi-takagaki-4456aa266/"),
    create_card("Nazka Leosala", 
                app.get_asset_url('leosala1.png'), 
                """
                Main Programmer and Backend Developer
                                            """,
                "https://www.linkedin.com/in/nazka-leosala-b4ab012b8/"),
    create_card("Ma. Roxette Rojas", 
                app.get_asset_url('rojas1.png'), 
                """
                Systems Designer and Frontend Developer
                                            """, 
                
                "https://www.linkedin.com/in/maroxetterojas/"),
    create_card("Ma. Lourdes Isabelle Tinaza", 
                app.get_asset_url('tinaza1.png'), 
                """
                Instructional Designer and Database Developer
                                            """,
                "https://www.linkedin.com/in/ma-lourdes-isabelle-tinaza/"),
] 

card_columns = [dbc.Col(card, xs=12, sm=6, md=6, lg=3, xl=3) for card in cards]






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
                        html.H1("ABOUT US", style={'textAlign': 'center'}),
                        html.Br(),  
                        html.P(
                            [
                                html.Span("TINQAD", style={'fontWeight': 'bold'}),
                                """ or the """,
                                html.Span("Total Integrated Network for Quality Assurance and Development", style={'fontWeight': 'bold'}),
                                """ is a centralized platform 
                                designed to streamline the monitoring operations of the Quality Assurance Office (QAO) 
                                at the University of the Philippines Diliman (UPD). The name is a play on the Tagalog word 
                                """,
                                html.Span("tingkád", style={'fontStyle': 'italic'}),
                                """ meaning “brilliance,” TINQAD is designed to assist the QAO in 
                                polishing and continuously improving the various sectors within UPD. An all-in-one platform that 
                                makes documentation, task tracking, and data analysis easier than ever.
                                """
                            ], style={'textAlign': 'justify'}
                        ), 

                        html.Br(),             
                        html.Img(src=app.get_asset_url('QAOTeam.jpg'), style={'height': '50px'}),
                          
                        html.Div(
                            [
                                  
                                html.Br(),
                                html.H4("Streamlining Quality Assurance with Data-Driven Solutions ", style={'textAlign': 'center'}),
                                 
                                html.P("""
                                       TINQAD stands as a testament to our dedication to quality. 
                                       By offering a streamlined, integrated system, we ensure 
                                       that each department within UPD operates at its highest potential. 
                                       Our tools and analytics are designed to maintain and elevate the quality 
                                       of services provided by the university.
                                            """ , style={'textAlign': 'justify'}), 
  
                                html.Br(),
                                html.Br(),
                            ],
                        ),

                        html.Div(
                            [
                                html.P(
                                    """• • •""",
                                    style = {'text-align' : 'center'}
                                ),
                                html.H4("The Development Team", style={'textAlign': 'center'}),
                                html.P(
                                    [
                                        "TINQAD is a project in IE 194 and 195 (Capstone I and II) by BS Industrial Engineering students at the ",
                                        html.A(html.B("Industrial Engineering and Operations Research Department (IEORD)"), href = 'https://ieor.engg.upd.edu.ph'),
                                        " of the University of the Philippines College of Engineering in Diliman, Quezon City. The project team is composed of:"
                                    ]
                                ),
                                 
                                dbc.Container(
                                    dbc.Row(
                                        card_columns,
                                        justify="start"
                                    ),
                                    fluid=True
                                )
                            ],
                        ),

                        html.Div(
                            [
                                html.P(
                                [
                                    "This project was made possible through the guidance and instruction of ",
                                    html.B( "Erickson Llaguno"),
                                    " and ",
                                    html.B( "Leslie Gopalan"),
                                    ", Senior Lecturers at the UPD IEORD."
                                    
                                ]),
                                html.Br(),
                                html.Br(),
                            ]
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