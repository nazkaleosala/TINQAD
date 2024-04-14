from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

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
                    
                    html.A(html.B('Home'), href='/homepage', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Profile', href='/profile', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Register User', href='/register_user', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Search Users', href='/search_users', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.Hr(),

                    #admin dashboard 
                    html.A(html.B('Admin'), href='/administration_dashboard', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Record Expenses', href='/record_expenses', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Training Documents', href='/training_documents', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Generate Report', href='/generate_report', style={'color': 'black', 'text-decoration': 'none'}), 
                    html.Hr(), 

                    #internal qa dashboard
                    html.A(html.B('Internal QA'), href='/iqa_dashboard', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('iAADs Reports Summary', href='/iaads_reports', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Acad Heads Directory', href='/acad_heads_directory', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.Hr(), 

                    
                    #external qa dashboard
                    html.A(html.B('External QA'), href='/eqa_dashboard', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Assessment Reports', href='/assessment_reports', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Accreditation Tracker', href='/accreditation_tracker', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Program List', href='/program_list', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.Hr(), 

                    
                    #km team dashboard
                    html.A(html.B('KM Team'), href='/km_dashboard', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('THE World Univ Rankings', href='/THEworld_rankings', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('SDG Impact Rankings', href='/SDGimpact_rankings', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('QS University Rankings', href='/QSworld_rankings', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.Hr(), 

                    
                    #qa officers
                    html.A(html.B('QA Officers Dashboard'), href='/qa_officers', style={'color': 'black', 'text-decoration': 'none'}), 
                    html.A('QA Officers Directory', href='/qa_directory', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('QA Officers Training List', href='/training_list', style={'color': 'black', 'text-decoration': 'none'}),  
                    html.A('Placeholder so the margin is wider', style={'color': 'white', 'text-decoration': 'none'}),  

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
                # Column for the logo
                dbc.Col(
                    html.A(
                        html.Img(
                            src="/assets/icons/qao-logo-icon1.png",
                            style={'height': '100px'}
                        ),
                        href="/home",  
                    ),
                    md=4  # Reduced size to fit in the grid
                ),
                # Column for the links
                dbc.Col(
                    [ 
                        html.Div(html.A("About TINQAD", href="/About_TINQAD", style={'color': 'white', 'text-decoration': 'none'})),
                        html.Div(html.A("QAO Website", href="https://qa.upd.edu.ph/new-qao-website/", style={'color': 'white', 'text-decoration': 'none'})),
                         
                        html.P("📧 qa.upd@up.edu.ph", className="mb-0"), 
                        html.P("📞(02) 9891-8500 local 2092", className="mb-0"),
                    ],
                    md=3  
                ),
                
                dbc.Col(
                    [
                        html.H1("TINQAD", className="fw-bold mb-0"),  # mb-0 sets the bottom margin to 0
                        html.P("The Total Integrated Network for Quality Assurance and Development © 2023-2024", className="mb-0"),
                        html.P("Homepage images provided by Wikipedia and Ralff Nestor Nacor", className="fw-lighter mb-0 fst-italic"),
                       
                    ],
                    md=4 
                ),
                
                dbc.Col(
                    html.A(
                        html.Img(
                            src="/assets/icons/arrow.png",
                            style={'height': '50px'}
                        ),
                        href="#",  
                    ), style={'text-align': 'right'}
                    
                ),
            ],
            
            className="gx-0",
        ),
        fluid=True,
        style={'background-color': '#7A0911', 'color': 'white'},
        className="py-3",
    )
    return footer