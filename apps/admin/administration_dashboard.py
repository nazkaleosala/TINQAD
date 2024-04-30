import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go

from apps import commonmodules as cm
from app import app
from apps import dbconnect as db
from datetime import datetime




def generate_pie_and_bar_chart():
    # Fetch data from the database for the pie chart
    pie_sql = """
        SELECT main_expense_name, SUM(exp_amount) AS total_amount
        FROM adminteam.expenses AS e
        LEFT JOIN adminteam.main_expenses AS me ON e.main_expense_id = me.main_expense_id
        GROUP BY main_expense_name
    """
    pie_df = db.querydatafromdatabase(pie_sql, (), ['main_expense_name', 'total_amount'])

    if pie_df.empty:
        pie_chart = html.Div("No data available for the pie chart")
    else:
        # Set custom legend labels
        custom_legend_labels = {
            "Maintenance and Other Operating Expenses (MOOE)": "MOOE",
            "Training & Workshop Expenses (External)": "Training",
            "Equipment Outlay": "Equipment"
        }
        # Map custom legend labels to main expense names
        pie_df['legend_labels'] = pie_df['main_expense_name'].map(custom_legend_labels)

        # Define custom colors
        custom_colors = ['#39B54A', '#F8B237', '#D37157']

        pie_fig = go.Figure(data=[go.Pie(
            labels=pie_df['legend_labels'],
            values=pie_df['total_amount'],
            marker=dict(colors=custom_colors)
        )])
        pie_fig.update_layout(title='Current Month')
        pie_chart = dcc.Graph(figure=pie_fig)

    # Fetch data from the database for the bar chart
    bar_sql = """
        SELECT 
            TO_CHAR(exp_date, 'Month') AS month,
            SUM(exp_amount) AS total_amount
        FROM adminteam.expenses
        GROUP BY TO_CHAR(exp_date, 'Month')
        ORDER BY TO_DATE(TO_CHAR(exp_date, 'Month'), 'Month')
    """
    bar_df = db.querydatafromdatabase(bar_sql, (), ['month', 'total_amount'])

    if bar_df.empty:
        bar_chart = html.Div("No data available for the bar chart")
    else:
        bar_fig = go.Figure([go.Bar(x=bar_df['month'], y=bar_df['total_amount'])])
        bar_fig.update_layout(title='Monthly Expenses', xaxis_title='Month', yaxis_title='Expenses')
        bar_chart = dcc.Graph(figure=bar_fig)

    return dbc.Row(
        [
            dbc.Col(pie_chart, width=6),  # Equal width for both charts
            dbc.Col(bar_chart, width=6)   # Equal width for both charts
        ]
    )


# Assuming commonmodules has a function to generate card-like structures
def generate_card(header, body):
    card = dbc.Card(
        [
            dbc.CardHeader(header),
            dbc.CardBody(
                [
                    html.P(body, className="card-text"),
                ]
            ),
        ],
    )
    return card

def get_main_expenses():
    df = db.querydatafromdatabase("SELECT * FROM adminteam.main_expenses", (), ['main_expense_id', 'main_expense_name'])
    main_expenses = df.to_records(index=False).tolist()
    return main_expenses

def get_sub_expenses(main_expense_id):
    df = db.querydatafromdatabase("SELECT * FROM adminteam.sub_expenses WHERE main_expense_id = %s", (main_expense_id,), ['sub_expense_id', 'sub_expense_name', 'main_expense_id'])
    sub_expenses = df.to_records(index=False).tolist()
    return sub_expenses

def populate_accordion():
    main_expenses = get_main_expenses()
    accordion_items = []

    for main_expense in main_expenses:
        main_expense_id, main_expense_name = main_expense
        
        sub_expenses = get_sub_expenses(main_expense_id)
        sub_items = []

        for sub_expense in sub_expenses:
            sub_expense_id, sub_expense_name, _ = sub_expense
            sub_items.append(html.P(sub_expense_name))

        accordion_item = dbc.AccordionItem(
            sub_items,
            title=main_expense_name,
        )
        accordion_items.append(accordion_item)

    return html.Div(dbc.Accordion(accordion_items))

expensetypes = populate_accordion()

def get_current_month():
    # Return the current month's name, e.g., "April".
    return datetime.now().strftime("%B")

def get_year_range():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return f"{previous_year}-{current_year}"


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
                        html.H1("ADMIN DASHBOARD"),
                        html.Hr(),
                        
                        dbc.Row(
                            [
                                # Accounts Card
                                dbc.Col(
                                    generate_card(html.P(html.Strong(f"ACCOUNTS {get_year_range()}")), ""),
                                    width=6
                                ),
                                # Budget Card
                                dbc.Col(
                                    generate_card(
                                        html.P(
                                            [
                                                html.Span("BUDGET ", style={'font-weight': 'bold'}), 
                                                html.Span(get_current_month())  
                                            ]
                                        ),
                                        body=""  # You were missing the 'body' argument here
                                    ), 
                                    width=6
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Spending Overview
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H3("SPENDING OVERVIEW", className="mb-3"),
                                        generate_pie_and_bar_chart()
                                    ]
                                )
                            ]
                        ),
                        # Add the maintenance and other expenses section
                        dbc.Row(
                            [
                                dbc.Col(
                                    expensetypes,
                                    width=12
                                )
                            ]
                        ),
                    ],
                    width=9,
                    style={'marginLeft': '15px'}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    cm.generate_footer(), width={"size": 12, "offset": 0}
                ),
            ]
        )
    ]
)
