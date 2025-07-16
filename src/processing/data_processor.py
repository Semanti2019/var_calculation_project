import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')
class DataProcessor:

    @staticmethod
    def gen_time_series(df: pd.DataFrame) -> pd.DataFrame:
        """
        Utility function to generate timeseries dataframe from assignment data
        :param df:
        :return: dataframe
        """
        # df['date'] = df.date.apply(dt.datetime.strptime, args=['%d/%m/%Y'])
        df['date'] =pd.to_datetime(df['date'],format = '%d/%m/%Y')
        df.set_index('date', drop=True, inplace=True)
        return df
    @staticmethod
    def _add_shifted_time_column(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a new column with dates shifted backward
        :param df: instrument timeseries
        :return: instrument_timeseries dataframe with shifted column
        """
        df['time_shift'] = df[df.columns[0]].shift(-1)

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




