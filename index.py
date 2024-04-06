from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import webbrowser

from app import app
from apps import commonmodules as cm
from apps import home


from apps.maindashboard import homepage, user_profile, register_user, search_users, about_TINQAD
from apps.admin import administration_dashboard, record_expenses, training_instructions, training_documents,  generate_report
from apps.iqa import iqa_dashboard, acad_heads_directory, iaads_reports, acadheads_profile
from apps.eqa import eqa_dashboard, assessment_reports, assessment_details, accreditation_tracker, program_list, program_details
from apps.km import km_dashboard, THEworld_rankings, SDGimpact_rankings, QSworld_rankings, SDG_submission, SDG_revision
from apps.qaofficers import qa_directory, qa_officers, training_list, qaofficers_profile


CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
        html.Link(rel='icon', href='/assets/TINQAD.png')
    ]
)


@app.callback(
    [
        Output('page-content', 'children')
    ],
    [
        Input('url', 'pathname')
    ]
)
def displaypage (pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if pathname == '/' or pathname == '/home':
                returnlayout = home.layout

            #maindashboard
            elif pathname == '/homepage':
                returnlayout = homepage.layout
            elif pathname == '/profile':
                returnlayout = user_profile.layout  
            elif pathname == '/register_user':
                returnlayout = register_user.layout
            elif pathname == '/search_users':
                returnlayout = search_users.layout
            elif pathname == '/About_TINQAD':
                returnlayout = about_TINQAD.layout

            #admin
            elif pathname == '/administration_dashboard':
                returnlayout = administration_dashboard.layout
            elif pathname == '/record_expenses':
                returnlayout = record_expenses.layout
            elif pathname == '/training_documents':
                returnlayout = training_instructions.layout
            elif pathname == '/training/training_documents':
                returnlayout = training_documents.layout
            elif pathname == '/generate_report':
                returnlayout = generate_report.layout
                
            #IQA
            elif pathname == '/iqa_dashboard':
                returnlayout = iqa_dashboard.layout
            elif pathname == '/iaads_reports':
                returnlayout = iaads_reports.layout  
            elif pathname == '/acad_heads_directory':
                returnlayout = acad_heads_directory.layout
            elif pathname == '/acadheadsdirectory/acadheads_profile':
                returnlayout = acadheads_profile.layout
            
            
            #EQA
            elif pathname == '/eqa_dashboard':
                returnlayout = eqa_dashboard.layout
            elif pathname == '/assessment_reports':
                returnlayout = assessment_reports.layout
            elif pathname == '/assessmentreports/assessment_details':
                returnlayout = assessment_details.layout
            elif pathname == '/accreditation_tracker':
                returnlayout = accreditation_tracker.layout
            elif pathname == '/program_list':
                returnlayout = program_list.layout
            elif pathname == '/programlist/program_details':
                returnlayout = program_details.layout

            #KM
            elif pathname == '/km_dashboard':
                returnlayout = km_dashboard.layout 
            elif pathname == '/THEworld_rankings':
                returnlayout = THEworld_rankings.layout 
            elif pathname == '/SDGimpact_rankings':
                returnlayout = SDGimpact_rankings.layout 
            elif pathname == '/SDGimpactrankings/SDG_submission':
                returnlayout = SDG_submission.layout 
            elif pathname == '/SDGimpactrankings/SDG_revision':
                returnlayout = SDG_revision.layout 


                
            elif pathname == '/QSworld_rankings':
                returnlayout = QSworld_rankings.layout 

            
            #QA Officers 
            elif pathname == '/qa_officers':
                returnlayout = qa_officers.layout
            elif pathname == '/QAOfficers/qaofficers_profile':
                returnlayout = qaofficers_profile.layout
            elif pathname == '/qa_directory':
                returnlayout = qa_directory.layout
            elif pathname == '/qa_directory/qaofficers_profile':
                returnlayout = qaofficers_profile.layout
            elif pathname == '/training_list':
                returnlayout = training_list.layout

            else:
                returnlayout = 'error404'
    
            return [returnlayout]
    
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
