from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash import callback_context
from dash.dependencies import Input, Output, State

from app import app
from apps import dbconnect as db


navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        dbc.Col(
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                [
                                    html.Img(
                                        src=app.get_asset_url('icons/logo-block.png'),
                                        style={'height': '2em'}
                                    ),
                                ],
                                className="ms-2"
                            )
                        )
                    ],
                    align="center",
                    className='g-0'
                ), 
            )
        ),
        html.Div(
            [
                dbc.Row(id = 'navbar_links')
            ], style = {'margin-right' : '12px'}
        )
    ],
    dark=False,
    color='dark',
    style={
        'background-image': 'url(/assets/icons/red-navbar.png)',
        'background-size': '80em 4em',
        'background-position': 'center top'
    },
)



 


@app.callback(
    [Output('navbar_links', 'children')],
    [Input('url', 'pathname')],
    [State('currentuserid', 'data')]
)

def navbarlinks(pathname, user_id):
    if pathname != '/' and pathname != '/home':
        sql = """
            SELECT 
                user_fname AS fname, 
                user_livedname AS livedname
            FROM maindashboard.users 
            WHERE user_id = %s
        """

        values = [user_id]
        cols = ['fname', 'livedname']
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            fname = df['fname'][0]
            livedname = df['livedname'][0]

            name = livedname if livedname else fname

            links = [
                dbc.Col(
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("👋 Profile", href="/profile"),
                            dbc.DropdownMenuItem("🏠 Home", href="/homepage"),
                            dbc.DropdownMenuItem("🔒 Logout", href="/"),
                        ],
                        label=html.B("👋 Hello, %s" % name),
                        align_end=True,
                        in_navbar=True,
                        nav=True
                    ), width='auto'
                )
            ]
            return [links]
        else:
            # Handle case where user data is not found
            return [[html.Div("Hi! Welcome")]]
    else:
        return [[]] 













def generate_navbar():
    navbar = dbc.Navbar(
        [
            dbc.Nav(  
                [
                    
                    html.A(html.B('Home'), href='/homepage', className="nav-link"),  
                    html.A('Profile', href='/profile', className="nav-link"),   
                    html.A('Search Users', href='/search_users', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    #admin dashboard 
                    html.A(html.B('Admin'),  href='/administration_dashboard', className="nav-link"),  
                    html.A('Record Expenses',  href='/record_expenses', className="nav-link"),  
                    html.A('Training Documents',  href='/training_instructions', className="nav-link"),  
                    html.A('View Training List',  href='/training_record', className="nav-link"),  
                    #html.A('Generate Report', id='generate-report-link', href='/generate_report', className="nav-link"), 
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    #internal qa dashboard
                    html.A(html.B('Internal QA'), href='/iqa_dashboard', className="nav-link"),  
                    #html.A('iAADs Reports Summary', id='iaads-reports-link', href='/iaads_reports', className="nav-link"),  
                    html.A('Academic Heads Directory',  href='/acad_heads_directory', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    
                    #external qa dashboard
                    html.A(html.B('External QA'),  href='/eqa_dashboard', className="nav-link"),  
                    html.A('Assessment Reports', href='/assessment_reports', className="nav-link"),  
                    html.A('Assessment Tracker', href='/assessment_tracker', className="nav-link"),  
                    html.A('Program List',  href='/program_list', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    
                    #km team dashboard
                    html.A(html.B('KM Team'), href='/km_dashboard', className="nav-link"),  
                    #html.A('THE World Univ Rankings', id='the-world-univ-rankings-link', href='/THEworld_rankings', className="nav-link"),  
                    html.A('SDG Impact Rankings',  href='/SDGimpact_rankings', className="nav-link"),  
                    html.A('SDG Evidence List',  href='/SDG_evidencelist', className="nav-link"),  
                    #html.A('QS University Rankings', id='qs-university-rankings-link', href='/QSworld_rankings', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ), 

                    
                    #qa officers
                    html.A(html.B('QA Officers Dashboard'), id='qa-officers-dashboard-link', href='/QAOfficers_dashboard', className="nav-link"),    
                    html.A('QA Officers Directory', id='qa-officers-directory-link', href='/QAOfficers_directory', className="nav-link"),  

                ],
                vertical=True,  # Set to True for vertical stacking
                navbar=True, 
                style = {
                    'margin-left' : '2em',
                    'margin-top' : '1em',
                    'max-height': '90vh',  # Maximum height of the navbar
                    'overflow-y': 'auto'   # Enable vertical scrolling
                },
            ),
        ],
        color="white",
        style = {
            'margin-left' : '-2em',
            'margin-top' : '-5em',
            'position' : 'auto',
        },
    )
    return navbar 




def generate_footer():
    footer = dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        html.Img(
                            src="/assets/icons/qao-logo-icon1.png",
                            style={'height': '80px','margin-left': '30px'}
                        ),
                        href="https://tinqad.edu.ph",  
                    ),
                    md=3
                ),
                dbc.Col(
                    [ 
                        html.Div(html.A("About TINQAD", href="/About_TINQAD", style={'color': 'white', 'text-decoration': 'none', 'font-size': '13px'})),
                        html.Div(html.A("QAO Website", href="https://qa.upd.edu.ph/new-qao-website/", style={'color': 'white', 'text-decoration': 'none', 'font-size': '13px'})),
                        html.P("📧 qa.upd@up.edu.ph", className="mb-0", style={'font-size': '12px', 'margin-top': '2px'}), 
                        html.P("📞(02) 9891-8500 local 2092", className="mb-0", style={'font-size': '12px', 'margin-top': '2px'}),
                    ],
                    md=3  
                ),
                dbc.Col(
                    [
                        html.H1("TINQAD", className="fw-bold mb-0", style={'font-size': '32px'}),
                        html.P("The Total Integrated Network for Quality Assurance and Development", className="mb-0", style={'font-size': '12px'}),
                        html.P("© 2023-2024 Diliman. Some rights reserved", className="mb-0", style={'font-size': '12px'}),
                        html.P("Homepage images provided by Wikipedia and Ralff Nestor Nacor", className="fw-lighter mb-0 fst-italic", style={'font-size': '12px'}),
                    ],
                    md=3 
                ),
                dbc.Col(
                    html.A(
                        html.Img(
                            src="/assets/icons/arrow.png",
                            style={'height': '50px', 'margin-bottom': '50px'}
                        ),
                        href="#",  
                    ),
                    md=1,
                    style={'display': 'flex', 'align-items': 'flex-end', 'justify-content': 'flex-end'}
                ),
            ],
            className="gx-0",
            style={'flex-wrap': 'wrap', 'justify-content': 'space-between'}
        ),
        fluid=True,
        style={'background-color': '#7A0911', 'color': 'white'},
        className="py-3",
    )
    return footer
