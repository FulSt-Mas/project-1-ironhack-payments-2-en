# utils/dataloader.py
import pandas as pd

class KPILoader:
    def __init__(self, file_path1, file_path2):
        self.file_path1 = '/Users/massih/Code/Ironhack/1_Project/project-1-ironhack-payments-2-en/project_dataset/extract_fees_data_analyst.csv'
        self.file_path2 = '/Users/massih/Code/Ironhack/1_Project/project-1-ironhack-payments-2-en/project_dataset/extract_cash request_data analyst.csv'

    def load_data(self):
        """
        Load data from CSV files.

        Returns:
            df1 (DataFrame): DataFrame containing data from the first CSV file.
            df2 (DataFrame): DataFrame containing data from the second CSV file.
        """
        df1 = pd.read_csv(self.file_path1)
        df2 = pd.read_csv(self.file_path2)
        return df1, df2
