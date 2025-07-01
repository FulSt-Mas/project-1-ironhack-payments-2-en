# components/callbacks.py
from dash import Input, Output
import plotly.express as px
import pandas as pd

class CallbackManager:
    def register_callbacks(self, app, df1, df2):
        """
        Register callbacks for the Dash application.

        Args:
            app (Dash): The Dash application instance.
            df1 (DataFrame): DataFrame containing data from the first CSV file.
            df2 (DataFrame): DataFrame containing data from the second CSV file.
        """
        @app.callback(
            Output('kpi-graph', 'figure'),
            [Input('kpi-dropdown', 'value')]
        )
        def update_graph(selected_kpi):
            """
            Update the graph based on the selected KPI.

            Args:
                selected_kpi (str): The selected KPI from the dropdown.

            Returns:
                figure (plotly.graph_objs.Figure): The Plotly figure to display.
            """
            if selected_kpi == 'kpi1':
                df2['created_at'] = pd.to_datetime(df2['created_at'])
                monthly_usage = df2['created_at'].dt.to_period('M').value_counts().sort_index()
                monthly_usage_df = monthly_usage.reset_index()
                monthly_usage_df['created_at'] = monthly_usage_df['created_at'].astype(str)
                fig = px.bar(monthly_usage_df, x='created_at', y='count', title='Frequency of Service Usage over time')
                return fig
            elif selected_kpi == 'kpi2':
                # Incident Rate by Category
                category_counts = df1['category'].value_counts().reset_index()
                category_counts.columns = ['Category', 'Incident Count']
                fig = px.bar(category_counts, x='Category', y='Incident Count', title='Incident Rate by Category')
                return fig
            elif selected_kpi == 'kpi3':
                # Revenue by Cohort
                df1['created_at'] = pd.to_datetime(df1['created_at'])
                df1['cohort_month'] = df1['created_at'].dt.to_period('M')
                revenue_by_cohort = df1.groupby('cohort_month')['total_amount'].sum().reset_index()
                revenue_by_cohort['cohort_month'] = revenue_by_cohort['cohort_month'].astype(str)
                fig = px.bar(revenue_by_cohort, x='cohort_month', y='total_amount', title='Total Revenue by Cohort Over Time')
                fig.update_layout(xaxis_tickangle=-45)
                return fig
            elif selected_kpi == 'kpi4':
                # Average Processing Time
                df2['created_at'] = pd.to_datetime(df2['created_at'])
                df2['updated_at'] = pd.to_datetime(df2['updated_at'])
                df2['processing_time_days'] = (df2['updated_at'] - df2['created_at']).dt.days
                average_processing_time = df2['processing_time_days'].mean()
                fig = px.histogram(df2, x='processing_time_days', nbins=20, title=f'Average Processing Time: {average_processing_time:.2f} days', labels={'processing_time_days': 'Processing Time (Days)'})
                return fig
            else:
                return px.bar(title=f"Placeholder for {selected_kpi}")
