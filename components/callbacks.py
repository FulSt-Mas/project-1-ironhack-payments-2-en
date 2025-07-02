# components/callbacks.py
from dash import Input, Output
import plotly.express as px
import pandas as pd

class CallbackManager:
    def register_callbacks(self, app, df_clean):
        """
        Register callbacks for the Dash application.

        Args:
            app (Dash): The Dash application instance.
            df_clean (DataFrame): Cleaned DataFrame containing data from the merged CSV files.
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
            # Convert necessary datetime columns
            df_clean['created_at_x'] = pd.to_datetime(df_clean['created_at_x'])
            df_clean['updated_at_x'] = pd.to_datetime(df_clean['updated_at_x'])

            if selected_kpi == 'kpi1':
                # At this stage, ensure that 'Cohort_by_month' is already derived from 'created_at_x'

                # Filter for cohorts from June 2020 onwards
                df_filtered = df_clean[df_clean['Cohort_by_month'] >= '2020-06']

                # Monthly usage analysis based on 'Cohort_by_month'
                # Since you wish to visualize and group by month while keeping May and November, you need not exclude them
                monthly_usage = df_filtered['Cohort_by_month'].value_counts().sort_index()
                monthly_usage_df = monthly_usage.reset_index()
                monthly_usage_df.columns = ['Cohort_by_month', 'count']
                monthly_usage_df['Cohort_by_month'] = monthly_usage_df['Cohort_by_month'].astype(str)

                # Create a bar plot
                fig = px.bar(monthly_usage_df, x='Cohort_by_month', y='count', title='Frequency of Service Usage Over Time From June 2020 Onwards')

                # Add a trendline (as a line plot)
                fig.add_scatter(x=monthly_usage_df['Cohort_by_month'], y=monthly_usage_df['count'], mode='lines', name='Trendline')

                return fig

            #     return fig
            elif selected_kpi == 'kpi2':
                # Use the pre-existing 'Cohort_by_month' rather than creating a new one
                category_month_counts = df_clean.groupby(['Cohort_by_month', 'category']).size().reset_index(name='Incident Count')

                # Convert the cohort month to string for plotting
                category_month_counts['Cohort_by_month'] = category_month_counts['Cohort_by_month'].astype(str)

                # Create box plots for each category and month
                fig = px.bar(category_month_counts, x='Cohort_by_month', y='Incident Count', color='category', barmode='group',
                            title='Incident Rate by Category and Month')

                # Add trend lines for each category
                for category in category_month_counts['category'].unique():
                    category_data = category_month_counts[category_month_counts['category'] == category]
                    fig.add_scatter(x=category_data['Cohort_by_month'], y=category_data['Incident Count'], mode='lines', name=f'{category} Trend')

                return fig

            elif selected_kpi == 'kpi3':
                # Use the pre-existing 'Cohort_by_month' field to filter and group data
                # No need to reconvert or add a new 'cohort_month' since it's available

                # Filter to include only May to October across all years
                df_filtered = df_clean[df_clean['Cohort_by_month'].dt.month.isin([5, 6, 7, 8, 9, 10])]

                # Group by the cohort months and calculate total revenue
                revenue_by_cohort = df_filtered.groupby('Cohort_by_month')['total_amount'].sum().reset_index()
                revenue_by_cohort.columns = ['Cohort_by_month', 'total_amount']

                # Convert the cohort month to string for plotting purposes
                revenue_by_cohort['Cohort_by_month'] = revenue_by_cohort['Cohort_by_month'].astype(str)

                # Create the plot
                fig = px.bar(revenue_by_cohort, x='Cohort_by_month', y='total_amount', title='Total Revenue by Cohort (May to October)')

                # Add a trend line
                fig.add_scatter(x=revenue_by_cohort['Cohort_by_month'], y=revenue_by_cohort['total_amount'], mode='lines', name='Trendline')
                fig.update_layout(xaxis_tickangle=-45)

                return fig


            elif selected_kpi == 'kpi4':
                # Average Processing Time
                df_clean['processing_time_days'] = (df_clean['updated_at_x'] - df_clean['created_at_x']).dt.days
                average_processing_time = df_clean['processing_time_days'].mean()
                fig = px.histogram(df_clean, x='processing_time_days', nbins=20, title=f'Average Processing Time: {average_processing_time:.2f} days', labels={'processing_time_days': 'Processing Time (Days)'})
                return fig
            else:
                return px.bar(title=f"Placeholder for {selected_kpi}")
