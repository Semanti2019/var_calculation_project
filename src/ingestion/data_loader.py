import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')
class DataLoader:
    @staticmethod
    def read_csv(file_name: str) -> pd.DataFrame:
        """Utility function to generate timeseries dataframe from assignment data"""
        df = pd.read_csv(filepath_or_buffer=file_name, delimiter='\t')
        df['date'] = pd.to_datetime(df['date'],format="%d/%m/%Y")
        df.set_index('date',inplace=True)
        return df
