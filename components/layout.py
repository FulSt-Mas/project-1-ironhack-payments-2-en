# components/layout.py
from dash import dcc, html

class LayoutCreator:
    def create_layout(self):
        """
        Create the layout for the Dash application.

        Returns:
            layout (html.Div): The layout of the Dash application.
        """
        layout = html.Div([
            html.H1("IronHack Payments KPI Dashboard", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='kpi-dropdown',
                options=[
                    {'label': 'Frequency of Service Usage over time', 'value': 'kpi1'},
                    {'label': 'Incident Rate by category', 'value': 'kpi2'},
                    {'label': 'Revenue by cohort', 'value': 'kpi3'},
                    {'label': 'Average processing time', 'value': 'kpi4'}
                ],
                value='kpi1'
            ),
            dcc.Graph(id='kpi-graph')
        ])
        return layout
git 
