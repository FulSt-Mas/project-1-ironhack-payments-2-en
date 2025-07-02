# # utils/dataloader.py
# import pandas as pd

# class KPILoader:
#     def __init__(self, file_path1, file_path2):
#         self.file_path1 = '/Users/massih/Code/Ironhack/1_Project/project-1-ironhack-payments-2-en/project_dataset/extract_fees_data_analyst.csv'
#         self.file_path2 = '/Users/massih/Code/Ironhack/1_Project/project-1-ironhack-payments-2-en/project_dataset/extract_cash request_data analyst.csv'

#     def load_data(self):
#         """
#         Load data from CSV files.

#         Returns:
#             df1 (DataFrame): DataFrame containing data from the first CSV file.
#             df2 (DataFrame): DataFrame containing data from the second CSV file.
#         """
#         df1 = pd.read_csv(self.file_path1)
#         df2 = pd.read_csv(self.file_path2)
#         return df1, df2


# import pandas as pd

import pandas as pd

class KPILoader:
    def __init__(self, file_path1, file_path2):
        self.file_path1 = 'project_dataset/extract_fees_data_analyst.csv'
        self.file_path2 = 'project_dataset/extract_cash request_data analyst.csv'

    def load_data(self):
        """
        Load data from CSV files, merge, and clean it by removing
        entries with NaN 'cash_request_id'.

        Returns:
            df_clean (DataFrame): Merged and cleaned DataFrame.
        """
        # Load the CSV files
        df1 = pd.read_csv(self.file_path1)
        df2 = pd.read_csv(self.file_path2)

        # Merge the DataFrames
        df_ml = pd.merge(df1, df2, left_on='cash_request_id', right_on='id', how='left')

        # Handle missing values: remove where 'cash_request_id' is NaN
        df_clean = df_ml.dropna(subset=['cash_request_id'])

        # Ensure 'created_at_x' is in datetime format
        df_clean['created_at_x'] = pd.to_datetime(df_clean['created_at_x'])

        # Create the 'Cohort_by_month' column
        df_clean['Cohort_by_month'] = df_clean['created_at_x'].dt.to_period('M')

        # Filter out November entries
        df_clean = df_clean[~df_clean['Cohort_by_month'].dt.month.isin([11])]

        return df_clean
