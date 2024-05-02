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
                    dcc.Dropdown(
                        id='sarep_degree_programs_id', 
                    ),
                    width=8,
                ),
                 
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "College", 
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=4),
                dbc.Col(
                    html.P(id="sarep_college_text"),
                    width=6,
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
                    dbc.Input(id="sarep_title", type="text"),
                    width=8,
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
                    dbc.Input(type="date", id='sarep_currentdate' ),
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
                        id='sarep_approv_eqa',
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
                        id="sarep_assessedby", 
                        placeholder="Select Accreditation Body",
                    ),
                    width=8,
                ),
            ],
            className="mb-2",
        ), 

          
                # with disabled input
                dbc.Row(
                    [
                        dbc.Label(
                            [
                                "Set SAR assessment date? ",
                                html.Span("*", style={"color": "#F8B237"})
                            ], 
                            width=4),
                        dbc.Col(
                            dbc.RadioItems(
                                id="sarep_qscheddate",
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
                                "Scheduled SAR Assessment Date ",
                                html.Span("*", style={"color": "#F8B237"})
                            ],  
                        ), width=4),
                        dbc.Col(
                            dbc.Input(type="date", id='sarep_sched_assessdate', disabled=True),
                            width=4,
                        ),
                    ],
                    className="mb-2",
                    id="scheduled-sar-date-field"
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
                    dbc.Input(id="sarep_link", type="text"),
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
                    dbc.Input(id="sarep_pdf", type="text"),
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
                        id='sarep_checkstatus',
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
                                "Date Reviewed ",
                                html.Span("*", style={"color": "#F8B237"})
                            ],
                            width=4),
                        dbc.Col(
                            dbc.Input(type="date", id='sarep_datereviewed', disabled=True),
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
                                id='sarep_review_status',
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
                            dbc.Textarea(id='sarep_notes', placeholder="Add notes", disabled=True),
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
                            dbc.Input(id="sarep_sarscore", type="number", disabled=True),
                            width=3,
                        ),
                    ],
                    className="mb-2",
                ),
            ],
            className="mb-1",
            id='already-checked'
        ),
 
 
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Cancel", color="secondary", id="cancel_button", n_clicks=0),
                    width="auto"
                ),
                 dbc.Col(
                    dbc.Button("Register SAR", color="primary", className="me-3", id="save_button", n_clicks=0),
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
                    html.H4('New Self Assessment Report added.'),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                      "Proceed", id='proceed_button', className='ml-auto'
                    ), 
                )
                 
            ],
            centered=True,
            id='sarep_successmodal',
            backdrop=True,   
            className="modal-success"  
        ),
         
    ]
)







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
                        html.H1("ADD NEW SAR"),
                        html.Hr(),
                        dbc.Alert(id='sarep_alert', is_open=False), # For feedback purpose
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
        Output('sarep_alert', 'color'),
        Output('sarep_alert', 'children'),
        Output('sarep_alert', 'is_open'),
        Output('sarep_successmodal', 'is_open')
    ],
    [
        Input('save_button', 'n_clicks')
    ],
    [
        State('sarep_degree_programs_id', 'value'), 
        State('sarep_title', 'value'),
        State('sarep_currentdate', 'value'),
        State('sarep_approv_eqa', 'value'),
        State('sarep_assessedby', 'value'),
        State('sarep_qscheddate', 'value'),
        State('sarep_sched_assessdate', 'value'),
        State('sarep_link', 'value'),
        State('sarep_pdf', 'value'),
        State('sarep_checkstatus', 'value'),
        State('sarep_datereviewed', 'value'),
        State('sarep_review_status', 'value'),
        State('sarep_notes', 'value'),
        State('sarep_sarscore', 'value'),
        
    ]
)
 
def record_assessment_details (submitbtn, sarep_degree_programs_id, sarep_title, sarep_currentdate, 
                               sarep_approv_eqa, sarep_assessedby, sarep_qscheddate, sarep_sched_assessdate, 
                               sarep_link, sarep_pdf, sarep_checkstatus, sarep_datereviewed, 
                               sarep_review_status, sarep_notes, sarep_sarscore):
    if not submitbtn:
        raise PreventUpdate

    alert_open = True  # Set alert_open to True by default
    modal_open = False
    alert_color = ''
    alert_text = ''

    # Input validation
    if not sarep_degree_programs_id:
        alert_color_sname = 'danger'
        alert_text_sname = 'Check your inputs. Please add a Degree Program Title.'
        return [alert_color_sname, alert_text_sname, alert_open, modal_open]
     
    # Default values
    sarep_pdf = None
 
    try:
        sql ="""
            INSERT INTO eqateam.assess_report (
                sarep_degree_programs_id, sarep_title,sarep_currentdate,
                sarep_approv_eqa,sarep_assessedby, sarep_qscheddate,
                sarep_sched_assessdate, sarep_link, sarep_pdf,
                sarep_checkstatus,sarep_datereviewed,  sarep_review_status, sarep_notes,
                sarep_sarscore, 
            )
            VALUES (%s, %s, %s, %s,
                    %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s)
           """
        values = (sarep_degree_programs_id, sarep_title,sarep_currentdate,
                sarep_approv_eqa,sarep_assessedby, sarep_qscheddate,
                sarep_sched_assessdate, sarep_link, sarep_pdf,
                sarep_checkstatus,sarep_datereviewed,  sarep_review_status, sarep_notes,
                sarep_sarscore)

        db.modifydatabase(sql, values)
        modal_open = True
    except Exception as e:
        alert_color = 'danger'
        alert_text = 'An error occurred while saving the data.'

    return [alert_color, alert_text, alert_open, modal_open]

  









# degree programs dropdown
@app.callback(
    Output('sarep_degree_programs_id', 'options'),
    Input('url', 'pathname')
)
def populate_degprog_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/sar_details':
        sql ="""
        SELECT degree_name as label, degree_id as value
        FROM public.degree_programs
       """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        degprog_types = df.to_dict('records')
        return degprog_types
    else:
        raise PreventUpdate




  
#college appear
@app.callback(
    Output('sarep_college_text', 'children'),
    [Input('sarep_degree_programs_id', 'value')]
)

def update_college_text(selected_degree_program):
    if selected_degree_program is None:
        return "No degree program selected"
    else:
        try:
            # Assuming you have a function in your db module to fetch the college based on the degree program
            college = db.get_college(selected_degree_program)
            if college:
                return college
            else:
                return "No college found for this degree program"
        except Exception as e:
            return "An error occurred while fetching the college: {}".format(str(e))


 

#eqa types dropdown
@app.callback(
    Output('sarep_approv_eqa', 'options'),
    Input('url', 'pathname')
)
def populate_approvedeqa_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/sar_details':
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


 

#review status dropdown
@app.callback(
    Output('sarep_review_status', 'options'),
    Input('url', 'pathname')
)
def populate_reviewstatus_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/assessmentreports/sar_details':
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



#schedule date
@app.callback(
    Output('scheduled-sar-date-field', 'children'),
    [Input('sarep_qscheddate', 'value')]
)
def update_scheduled_sar_date_field(value):
    if value =="Yes":
        input_width = 4  # Set width to 4 when"Yes" is selected
        disabled = False  # Enable input field
    else:
        input_width = 4  # Set width to 0 when"No" is selected
        disabled = True  # Disable input field

    return [
        dbc.Col(dbc.Label("Scheduled SAR Assessment Date"), width=4),
        dbc.Col(
            dbc.Input(type="date", id='sarep_sched_assessdate', disabled=disabled),
            width=input_width,
        )
    ]





#check status
@app.callback(
    Output('already-checked', 'children'),
    [Input('sarep_checkstatus', 'value')]
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
                    dbc.Input(type="date", id='sarep_datereviewed', disabled=disabled),
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
                        id='sarep_review_status',
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
                    dbc.Textarea(id='sarep_notes', placeholder="Add notes", disabled=disabled),
                    width=6,  # Adjusted width to match the dropdown
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label("SAR Score", width=4 ,style={"margin-right":"9px"}),
                dbc.Col(
                    dbc.Input(id="sarep_sarscore", type="number", disabled=disabled),
                    width=6,  # Adjusted width to match the dropdown
                ),
            ],
            className="mb-2",
        )
    ]


 










