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








form = dbc.Form(
    [
         
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree Program Title ", 
                         html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_deg_prog_id", type="number"),
                    width=5,
                ),
                 
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Cluster ", 
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_cluster_id", type="number"),
                    width=5,
                ),
                 
            ],
            className="mb-2",
        ),
        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Assessment Title ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_title", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                     "Date ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dbc.Input(type="date", id='arep_currentdate' ),
                            width=4,
                ),
            ],
            className="mb-2",
        ),
  

        dbc.Row(
            [
                dbc.Label(
                    [
                     "Approved EQA Type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_approv_eqa',
                        placeholder="Select EQA Type",
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "To be Assessed by ",
                        html.Span("*", style={"color": "#F8B237"})
                    ], 
                    width=4),
                dbc.Col(
                    dbc.Select(
                        id="arep_assessedby",
                        options=[
                            {"label":"Engineering Accreditation Commission","value":"Engineering Accreditation Commission"},
                            {"label":"International Accreditation","value":"International Accreditation"},
                            {"label":"Local Accreditation","value":"Local Accreditation"},
                        ],
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ), 

                
                
                # with disabled input
                dbc.Row(
                    [
                        dbc.Label(
                            [
                                "Is there a scheduled assessment date? ",
                                html.Span("*", style={"color": "#F8B237"})
                            ], 
                            width=4),
                        dbc.Col(
                            dbc.RadioItems(
                                id="arep_qscheddate",
                                options=[
                                    {"label":"Yes","value":"Yes"},
                                    {"label":"No","value":"No"},
                                ],
                                inline=True,
                            ),
                        ),
                    ],
                    className="mb-1",
                ),
                # Additional field for"Scheduled Assessment Date"
                dbc.Row(
                    [
                        dbc.Col(dbc.Label(
                            [
                                "Scheduled Assessment Date ",
                                html.Span("*", style={"color": "#F8B237"})
                            ],  
                        ), width=4),
                        dbc.Col(
                            dbc.Input(type="date", id='arep_sched_assessdate', disabled=True),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                    id="scheduled-assessment-date-field"
                ),

        dbc.Row(
            [
                dbc.Label(
                    [
                      "Report type ",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_report_type',
                        placeholder="Select Report Type",
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Link ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_link", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "PDF File ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4),
                dbc.Col(
                    dbc.Input(id="arep_pdf", type="text"),
                    width=5,
                ),
            ],
            className="mb-2",
        ),

        
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Check Status ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],  
                    width=4),
                 
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_checkstatus',
                        placeholder="Select Status",
                        options=[
                            {"label":"For Checking","value":"For Checking"},
                            {"label":"Already Checked","value":"Already Checked"},
                            ],
                    ),
                    width=4,
                ),
                
            ],
            className="mb-2", 
        ), 



        # Additional fields for"Already Checked" option
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Label(
                            [
                                "Date to be Reviewed ",
                                html.Span("*", style={"color": "#F8B237"})
                            ],
                            width=4),
                        dbc.Col(
                            dbc.Input(type="date", id='arep_datereviewed', disabled=True),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                ),
                dbc.Row(
                    [
                        dbc.Label(
                            [
                               "Review Status ",
                                html.Span("*", style={"color":"#F8B237"})
                            ],
                            width=4
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='arep_review_status',
                                placeholder="Select Review Status",
                                disabled=True,
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-2",
                ),

                dbc.Row(
                    [
                        dbc.Label(
                            [
                               "Notes ",
                               html.Span("*", style={"color": "#F8B237"})
                            ],
                            width=4
                        ),
                        dbc.Col(
                            dbc.Textarea(id='arep_notes', placeholder="Add notes", disabled=True),
                            width=8,
                        ),
                    ],
                    className="mb-2",
                ),

                dbc.Row(
                    [
                        dbc.Label(
                            [
                                "SAR Score ",
                                html.Span("*", style={"color": "#F8B237"})
                            ],
                            width=4),
                        dbc.Col(
                            dbc.Input(id="arep_sarscore", type="number", disabled=True),
                            width=3,
                        ),
                    ],
                    className="mb-2",
                ),
            ],
            className="mb-1",
            id='already-checked-fields'
        ),

 
         

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Ready for presenting to QAO? ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    dbc.RadioItems(
                        id="arep_qqaopresent",
                        options=[
                            {"label":"Yes","value":"Yes"},
                            {"label":"No","value":"No"},
                            ],
                            inline=True,  
                        ),
                ),
            ],
            className="mb-2", 
        ), 




        # Additional fields for"Ready for presenting to QAO?" option
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Date to be presented to QAO ",
                                        html.Span("*", style={"color": "#F8B237"})
                                    ],
                                    width=4 ,
                                    style={"margin-right":"18px"},),
                                dbc.Col(
                                    dbc.Input(type="date", id='arep_presdate'),
                                    width=4
                                ),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Mode of EQA Assessment ",
                                        html.Span("*", style={"color": "#F8B237"}) 
                                    ],
                                    width=4,
                                    style={"margin-right":"18px"},
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='arep_mode_eqa_assess',
                                        placeholder="Select Mode",
                                    ),
                                    width=4, 
                                ),
                            ],
                            className="mb-2",
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Label(
                                    [
                                        "Specific EQA Assessment ",
                                        html.Span("*", style={"color": "#F8B237"}) 
                                    ],
                                    width=4,
                                    style={"margin-right":"18px"},
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='arep_spec_eqa_assess',
                                        placeholder="Select EQA",
                                    ),
                                    width=6, 
                                ),
                            ],
                            className="mb-2",
                        ),
                    ]
                )
            ],
            className="mb-4",
            style={"display":"block"},  # Initially hide the fields
            id="ready-for-qao-fields"
        ),
        
    
        
 
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
                 dbc.Col(
                    dbc.Button("Register Assessment", color="primary", className="me-3", id="save_button", n_clicks=0),
                    width="auto"
                ),
            ],
            className="mb-2",
            justify="end",
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(className="bg-success"),
                dbc.ModalBody(
                    html.H4('New assessment report added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                      "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='arep_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
         
    ]
)






#schedule date
@app.callback(
    Output('scheduled-assessment-date-field', 'children'),
    [Input('arep_qscheddate', 'value')]
)
def update_scheduled_assessment_date_field(value):
    if value =="Yes":
        input_width = 4  # Set width to 4 when"Yes" is selected
        disabled = False  # Enable input field
    else:
        input_width = 4  # Set width to 0 when"No" is selected
        disabled = True  # Disable input field

    return [
        dbc.Col(dbc.Label("Scheduled Assessment Date"), width=4),
        dbc.Col(
            dbc.Input(type="date", id='arep_sched_assessdate', disabled=disabled),
            width=input_width,
        )
    ]



#check status
@app.callback(
    Output('already-checked-fields', 'children'),
    [Input('arep_checkstatus', 'value')]
)
def toggle_fields(check_status):
    if check_status =="Already Checked":
        disabled = False
    else:
        disabled = True

    return [
        dbc.Row(
            [
                dbc.Label("Date to be Reviewed", width=4,style={"margin-right":"9px"}),
                dbc.Col(
                    dbc.Input(type="date", id='arep_datereviewed', disabled=disabled),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Review Status",
                        html.Span("*", style={"color":"#F8B237"})
                    ],
                    width=4,style={"margin-right":"9px"},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='arep_review_status',
                        placeholder="Select Review Status",
                        disabled=disabled,
                    ),
                    width=6,  # Adjusted width to match the dropdown
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                       "Notes"
                    ],
                    width=4,style={"margin-right":"9px"},
                ),
                dbc.Col(
                    dbc.Textarea(id='arep_notes', placeholder="Add notes", disabled=disabled),
                    width=6,  # Adjusted width to match the dropdown
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("SAR Score", width=4 ,style={"margin-right":"9px"}),
                dbc.Col(
                    dbc.Input(id="arep_sarscore", type="number", disabled=disabled),
                    width=6,  # Adjusted width to match the dropdown
                ),
            ],
            className="mb-2",
        )
    ]





@app.callback(
    [Output('arep_presdate', 'disabled'),
     Output('arep_mode_eqa_assess', 'disabled'),
     Output('arep_spec_eqa_assess', 'disabled')],
    [Input('arep_qqaopresent', 'value')]
)
def update_qao_fields(qao_present):
    if qao_present != 'Yes':
        return True, True, True
    else:
        return False, False, False



 


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
                        html.H1("ADD NEW ASSESSMENT REPORT"),
                        html.Hr(),
                        dbc.Alert(id='arep_alert', is_open=False), # For feedback purpose
                        form, 
                    ], width=8, style={'marginLeft': '15px'}
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







@app.callback(
    [
        Output('arep_alert', 'color'),
        Output('arep_alert', 'children'),
        Output('arep_alert', 'is_open'),
        Output('arep_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('arep_deg_prog_id', 'value'),
        State('arep_cluster_id', 'value'),
        State('arep_title', 'value'),
        State('arep_currentdate', 'value'),
        State('arep_approv_eqa', 'value'),
        State('arep_assessedby', 'value'),
        State('arep_qscheddate', 'value'),
        State('arep_sched_assessdate', 'value'),
        State('arep_report_type', 'value'),
        State('arep_link', 'value'),
        State('arep_pdf', 'value'),
        State('arep_checkstatus', 'value'),
        State('arep_datereviewed', 'value'),
        State('arep_review_status', 'value'),
        State('arep_notes', 'value'),
        State('arep_sarscore', 'value'),
        State('arep_qqaopresent', 'value'),
        State('arep_presdate', 'value'),
        State('arep_mode_eqa_assess', 'value'),
        State('arep_spec_eqa_assess', 'value')   
    ]
)
 
def record_assessment_details (submitbtn, arep_deg_prog_id, arep_cluster_id, arep_title, arep_currentdate, 
                               arep_approv_eqa, arep_assessedby, arep_qscheddate, arep_sched_assessdate, 
                               arep_report_type, arep_link, arep_pdf, arep_checkstatus, arep_datereviewed, 
                               arep_review_status, arep_notes, arep_sarscore, arep_qqaopresent, 
                            arep_presdate, arep_mode_eqa_assess, arep_spec_eqa_assess):
    if not submitbtn:
        raise PreventUpdate

    alert_open = True  # Set alert_open to True by default
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not arep_deg_prog_id:
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Degree Program Title.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
     
    # Default values
    arep_pdf = None
 
    try:
        sql ="""
            INSERT INTO eqateam.assess_report (
                arep_deg_prog_id, arep_cluster_id, arep_title,arep_currentdate,
                arep_approv_eqa,arep_assessedby, arep_qscheddate,
                arep_sched_assessdate,arep_report_type,  arep_link, arep_pdf,
                arep_checkstatus,arep_datereviewed,  arep_review_status, arep_notes,
                arep_sarscore, arep_qqaopresent, arep_presdate,
                arep_mode_eqa_assess, arep_spec_eqa_assess
            )
            VALUES (%s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s)
           """
        values = (arep_deg_prog_id, arep_cluster_id, arep_title,arep_currentdate,
                arep_approv_eqa,arep_assessedby, arep_qscheddate,
                arep_sched_assessdate,arep_report_type,  arep_link, arep_pdf,
                arep_checkstatus,arep_datereviewed,  arep_review_status, arep_notes,
                arep_sarscore, arep_qqaopresent, arep_presdate,
                arep_mode_eqa_assess, arep_spec_eqa_assess)

        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'

    return [alert_color, alert_text, alert_open, modal_open]

  











  


# degree programs dropdown
@app.callback(
    Output('arep_deg_prog_id', 'options'),
    Input('url', 'pathname')
)
def populate_degprog_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT deg_prog_name as label, deg_prog_id as value
        FROM public.deg_prog_title
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        degprog_types = df.to_dict('records')
        return degprog_types
    else:
        raise PreventUpdate



#eqa types dropdown
@app.callback(
    Output('arep_approv_eqa', 'options'),
    Input('url', 'pathname')
)
def populate_degprog_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT approv_eqa_name as label, approv_eqa_id as value
        FROM eqateam.approv_eqa
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        approvedeqa_types = df.to_dict('records')
        return approvedeqa_types
    else:
        raise PreventUpdate



#report types dropdown
@app.callback(
    Output('arep_report_type', 'options'),
    Input('url', 'pathname')
)
def populate_reporttype_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT report_type_name as label, report_type_id as value
        FROM eqateam.report_type
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        report_types = df.to_dict('records')
        return report_types
    else:
        raise PreventUpdate




#report types dropdown
@app.callback(
    Output('arep_review_status', 'options'),
    Input('url', 'pathname')
)
def populate_reviewstatus_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT review_status_name as label, review_status_id as value
        FROM eqateam.review_status
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        reviewstatus_types = df.to_dict('records')
        return reviewstatus_types
    else:
        raise PreventUpdate




#Mode of EQA Assessment dropdown
@app.callback(
    Output('arep_mode_eqa_assess', 'options'),
    Input('url', 'pathname')
)
def populate_modeeqa_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT mode_eqa_assess_name as label, mode_eqa_assess_id as value
        FROM eqateam.mode_eqa_assess
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        modeeqaassess_types = df.to_dict('records')
        return modeeqaassess_types
    else:
        raise PreventUpdate




#Specific EQA Assessment dropdown
@app.callback(
    Output('arep_spec_eqa_assess', 'options'),
    Input('url', 'pathname')
)
def populate_modeeqa_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/assessment_details':
        sql ="""
        SELECT spec_eqa_assess_name as label, spec_eqa_assess_id as value
        FROM eqateam.spec_eqa_assess
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        speceqaassess_types = df.to_dict('records')
        return speceqaassess_types
    else:
        raise PreventUpdate


