import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')
class DataProcessor:
    try:
        @staticmethod
        def _add_shifted_time_column(df: pd.DataFrame) -> pd.DataFrame:
            """
            Adds a new column with dates shifted backward
            :param df: instrument timeseries
            :return: instrument_timeseries dataframe with shifted column
            """
            if df.empty or df.shape[1] == 0:
                raise ValueError("Input dataframe cannot be empty")
            df['time_shift'] = df[df.columns[0]].shift(-1)
            df.dropna(inplace=True)
            return df

        @staticmethod
        def add_shifted_time_column_processing(df: pd.DataFrame)->pd.DataFrame:
            """
            processing the data
            :param df:
            :return: df
            """
            processed_df = DataProcessor._add_shifted_time_column(df)
            return processed_df
    except ValueError as ve:
        print("Value error in DF")




