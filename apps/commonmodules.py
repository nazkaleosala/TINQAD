from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash import callback_context

from app import app

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
                href="/home"
            )
        ),
        dbc.Col(
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Profile", href="/profile"),
                    dbc.DropdownMenuItem("🏠 Home", href="/homepage"),
                    dbc.DropdownMenuItem("🔒 Logout", href="/logout"),
                    dbc.DropdownMenuItem("🔑 Change Password", href="/change-password"),
                ],
                nav=True,
                in_navbar=True,
                label=html.Span('Hi Pika!', style={'color': 'white'}),   
                right=True,
            ),
            width="auto",
            align="end",
            style={'margin-right': '0.5in'}  
        ),
    ],
    dark=False,
    color='dark',
    style={
        'background-image': 'url(/assets/icons/red-navbar.png)',
        'background-size': '80em 4em',
        'background-position': 'center top'
    },
)




def generate_navbar():
    navbar = dbc.Navbar(
        [
            dbc.Nav(  
                [
                    
                    html.A(html.B('Home'), id='home-link', href='/homepage', className="nav-link"),  
                    html.A('Profile', id='profile-link', href='/profile', className="nav-link"),  
                    html.A('Register User', id='register-user-link', href='/register_user', className="nav-link"),  
                    html.A('Search Users', id='search-users-link', href='/search_users', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    #admin dashboard 
                    html.A(html.B('Admin'), id='admin-link', href='/administration_dashboard', className="nav-link"),  
                    html.A('Record Expenses', id='record-expenses-link', href='/record_expenses', className="nav-link"),  
                    html.A('Training Documents', id='training-documents-link', href='/training_documents', className="nav-link"),  
                    #html.A('Generate Report', id='generate-report-link', href='/generate_report', className="nav-link"), 
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    #internal qa dashboard
                    html.A(html.B('Internal QA'), id='internal-qa-link', href='/iqa_dashboard', className="nav-link"),  
                    #html.A('iAADs Reports Summary', id='iaads-reports-link', href='/iaads_reports', className="nav-link"),  
                    html.A('Acad Heads Directory', id='acad-heads-directory-link', href='/acad_heads_directory', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    
                    #external qa dashboard
                    html.A(html.B('External QA'), id='external-qa-link', href='/eqa_dashboard', className="nav-link"),  
                    html.A('Assessment Reports', id='assessment-reports-link', href='/assessment_reports', className="nav-link"),  
                    html.A('Accreditation Tracker', id='accreditation-tracker-link', href='/accreditation_tracker', className="nav-link"),  
                    html.A('Program List', id='program-list-link', href='/program_list', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ),  

                    
                    #km team dashboard
                    html.A(html.B('KM Team'), id='km-team-link', href='/km_dashboard', className="nav-link"),  
                    html.A('THE World Univ Rankings', id='the-world-univ-rankings-link', href='/THEworld_rankings', className="nav-link"),  
                    html.A('SDG Impact Rankings', id='sdg-impact-rankings-link', href='/SDGimpact_rankings', className="nav-link"),  
                    html.A('QS University Rankings', id='qs-university-rankings-link', href='/QSworld_rankings', className="nav-link"),  
                    html.A('-----------------------------------', style={'color': 'white'} ), 

                    
                    #qa officers
                    html.A(html.B('QA Officers Dashboard'), id='qa-officers-dashboard-link', href='/qa_officers', className="nav-link"), 
                    html.A('QA Officers Directory', id='qa-officers-directory-link', href='/qa_directory', className="nav-link"),  
                    html.A('QA Officers Training List', id='qa-officers-training-list-link', href='/training_list', className="nav-link")   

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
