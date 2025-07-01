# app.py
import dash
from components.layout import LayoutCreator
from components.callbacks import CallbackManager
from utils.dataloader import KPILoader


# def initialize_app():
    # Load the data
kpi_loader = KPILoader('../project_dataset/extract - fees - data analyst.csv',
                           '../project_dataset/extract - cash request - data analyst.csv')
df1, df2 = kpi_loader.load_data()

    # Create the app
app = dash.Dash(__name__)
app.title = "IronHack Payments KPI Dashboard"

    # Set layout
layout_creator = LayoutCreator()
app.layout = layout_creator.create_layout()

    # Register callbacks
callback_manager = CallbackManager()
callback_manager.register_callbacks(app, df1, df2)

    # return app
server = app.server 
if __name__ == '__main__':
    # app = initialize_app()
    app.run(debug=True)

    # fixing the function bug with andre feedback:
    # app = initialize_app()
