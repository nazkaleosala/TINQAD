import dash
import dash_bootstrap_components as dbc
from dash import dash, html, dcc, Input, Output, State

from dash.exceptions import PreventUpdate

import webbrowser 
from urllib.parse import urlparse, parse_qs

from app import app
from apps import commonmodules as cm
from apps import home
from apps import blankpage  

from apps.maindashboard import homepage, user_profile, register_user, search_users, password, about_TINQAD
from apps.admin import administration_dashboard, expensetype_add, record_expenses, training_instructions, training_documents, add_expenses, training_record, viewexpense_list, viewtraining_list
from apps.iqa import iqa_dashboard, more_details, acad_heads_directory, acadheads_profile
from apps.eqa import eqa_dashboard, assessment_reports, assessment_details, accreditation_tracker, program_list, program_details, sar_details
from apps.km import km_dashboard, SDGimpact_rankings, SDG_submission, SDG_revision, add_criteria, SDG_evidencelist
from apps.qaofficers import qa_directory, qaofficers_profile, training_details, view_list, qa_dashboard

 
CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),

        # LOGIN DATA
        # 1) current_user_id -- stores user_id
        dcc.Store(id='sessionlogout', data = True, storage_type='local'),
        dcc.Store(id='currentuserid', data=-1, storage_type='local'),
        
        # 2) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=0, storage_type='local'),
        
        # Page mode and user id for viewing for those that have any
        dcc.Store(id='page_mode', data=-1, storage_type='memory'),
        dcc.Store(id='view_id', data=-1, storage_type='memory'),

        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
        html.Link(rel='icon', href='/assets/icons/TINQAD.png')
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
        State('url', 'search')
    ]
)
def displaypage(pathname, sessionlogout, user_id, accesstype, search):
    mode = None
    parsed = urlparse(search)
    if parse_qs(parsed.query):
        mode = parse_qs(parsed.query)['mode'][0] 
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url': 
            if pathname == '/' or pathname == '/home' or pathname == '/logout':
                returnlayout = home.layout
            elif user_id != -1:
                if accesstype >= 1:
                    
                    # Main Dashboard 
                    if pathname == '/homepage':
                        returnlayout = homepage.layout
                    elif pathname == '/profile':
                        returnlayout = user_profile.layout  
                    elif pathname == '/register_user':
                        returnlayout = register_user.layout
                    elif pathname == '/search_users':
                        returnlayout = search_users.layout
                    elif pathname == '/password':
                        returnlayout = password.layout
                    elif pathname == '/About_TINQAD':
                        returnlayout = about_TINQAD.layout
                    
                    #admin
                    elif pathname == '/administration_dashboard':
                        returnlayout = administration_dashboard.layout
                    elif pathname == '/record_expenses':
                        returnlayout = record_expenses.layout
                    elif pathname == '/record_expenses/add_expense':
                        returnlayout = add_expenses.layout
                    elif pathname == '/expense_list':
                        returnlayout = viewexpense_list.layout
                    elif pathname == '/expense_list/add_expensetype':
                        returnlayout = expensetype_add.layout
                    elif pathname == '/training_instructions':
                        returnlayout = training_instructions.layout
                    elif pathname == '/training_documents':
                        returnlayout = training_documents.layout
                    elif pathname == '/training_record':
                        returnlayout = training_record.layout
                    elif pathname == '/training_record/mode=view':
                        returnlayout = viewtraining_list.layout
                        
                        
                    #IQA
                    elif pathname == '/iqa_dashboard':
                        returnlayout = iqa_dashboard.layout
                    elif pathname == '/dashboard/more_details':
                        returnlayout = more_details.layout  
                    elif pathname == '/acad_heads_directory':
                        returnlayout = acad_heads_directory.layout
                    elif pathname == '/acadheads_profile':
                        returnlayout = acadheads_profile.layout
                    
                    
                    #EQA
                    elif pathname == '/eqa_dashboard':
                        returnlayout = eqa_dashboard.layout
                    elif pathname == '/assessment_reports':
                        returnlayout = assessment_reports.layout
                    elif pathname == '/assessmentreports/assessment_details':
                        returnlayout = assessment_details.layout
                    elif pathname == '/assessmentreports/sar_details':
                        returnlayout = sar_details.layout
                    elif pathname == '/assessment_tracker':
                        returnlayout = accreditation_tracker.layout
                    elif pathname == '/program_list':
                        returnlayout = program_list.layout
                    elif pathname == '/program_details':
                        returnlayout = program_details.layout

                    #KM
                    elif pathname == '/km_dashboard':
                        returnlayout = km_dashboard.layout 
                    elif pathname == '/add_criteria':
                        returnlayout = add_criteria.layout 
                    #elif pathname == '/THEworld_rankings':
                        #returnlayout = THEworld_rankings.layout 
                    elif pathname == '/SDGimpact_rankings':
                        returnlayout = SDGimpact_rankings.layout 
                    elif pathname == '/SDGimpactrankings/SDG_submission':
                        returnlayout = SDG_submission.layout 
                    elif pathname == '/SDGimpactrankings/SDG_revision':
                        returnlayout = SDG_revision.layout 
                    elif pathname == '/SDG_evidencelist':
                        returnlayout = SDG_evidencelist.layout 
                    #elif pathname == '/QSworld_rankings':
                        #returnlayout = QSworld_rankings.layout 

                    
                    #QA Officers 
                    elif pathname == '/QAOfficers_dashboard':
                        returnlayout = qa_dashboard.layout
                    elif pathname == '/qaofficers_profile':
                        returnlayout = qaofficers_profile.layout  
                    elif pathname == '/QAOfficers/addtraining':
                        returnlayout = training_details.layout
                    elif pathname == '/QAOfficers/datalist':
                        returnlayout = view_list.layout
                    elif pathname == '/QAOfficers_directory':
                        returnlayout = qa_directory.layout

                    else:
                        returnlayout = blankpage.layout
                
                elif accesstype == 2:
                    if pathname == '/homepage':
                        returnlayout = homepage.layout
                    elif pathname == '/profile':
                        returnlayout = user_profile.layout  
                    elif pathname == '/register_user':
                        returnlayout = register_user.layout
                    elif pathname == '/search_users':
                        returnlayout = search_users.layout
                    elif pathname == '/password':
                        returnlayout = password.layout
                    elif pathname == '/About_TINQAD':
                        returnlayout = about_TINQAD.layout
                    else:
                        returnlayout = blankpage.layout
                else:
                    returnlayout = blankpage.layout
            
            else:
                returnlayout = blankpage.layout
             
            logout_conditions = [
                pathname in ['/', '/logout'],
                user_id == -1,
                not user_id
            ]
            sessionlogout = any(logout_conditions)
        
        else:
            raise PreventUpdate
        return [returnlayout, sessionlogout ]
    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)