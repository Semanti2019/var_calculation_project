import pandas as pd
import logging
from typing import Callable
from src.processing.data_processor import DataProcessor
from src.returns.return_calculator import ReturnCalculator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR_Calculation')

class Instrument:

    @staticmethod
    def _calculate_shift_return(df: pd.DataFrame, horizon_days: float, shift_function: Callable) -> pd.DataFrame:
        """
        Applies the shift logic over all rows of the instrument timeseries
        :param df: instrument times series dataframe
        :param horizon_days: days for which the return should be estimated
        :param shift_function: the python callable used to calculate the shift
        :return: instrument time series dataframe with new 'shifted_change' column
        """
        # the shifted value (row.iloc[1]) corresponds to the previous day's value
        df['shifted_change'] = df.apply(lambda row: shift_function(time0_value=row.iloc[1],
                                                                   time1_value=row.iloc[0],
                                                                   horizon_days=horizon_days), axis=1)
        return df

    @staticmethod
    def _calculate_pnl_for_shift(df: pd.DataFrame, portfolio_value: float) -> pd.DataFrame:
        """
        Multiply the estimated daily return by the value of the instrument in the portfolio
        :param df: instrument time series dataframe
        :param portfolio_value: Value of the instrument in the portfolio
        :return: instrument time series dataframe with new 'pnl_vector' column
        """
        df['pnl_vector'] = df['shifted_change'] * portfolio_value

        return df

    @staticmethod
    def _calculate_instrument_pnl_vector(instrument_timeseries: pd.DataFrame, portfolio_value: float,
                                         return_function: Callable, horizon_days: float) -> pd.DataFrame:
        """
        Calculates the PnL for the given portfolio given the historical returns found in the instrument time series
        :param instrument_timeseries: a dataframe with business date index containing instrument values on those days
        :param portfolio_value: Value of the instrument in the portfolio
        :param return_function: the function used to calculate the instruments return
        :param horizon_days: number of days for which we estimate the return based on the one-day return
        :return: instrument_timeseries dataframe with new 'pnl_vector' column
        """
        instrument_timeseries = DataProcessor.add_shifted_time_column_processing(instrument_timeseries)
        instrument_timeseries = ReturnCalculator.calculate_return(instrument_timeseries, horizon_days=horizon_days,
                                                                  shift_function=return_function)
        return Instrument._calculate_pnl_for_shift(df=instrument_timeseries, portfolio_value=portfolio_value)
    @staticmethod
    def calculate_instrument_pnl_vector(instrument_timeseries: pd.DataFrame, portfolio_value: float,
                                        return_function: Callable, horizon_days: float) -> pd.DataFrame:
        """
        Calculates the PnL for the given portfolio given the historical returns found in the instrument time series
        :param instrument_timeseries: a dataframe with business date index containing instrument values on those days
        :param portfolio_value: Value of the instrument in the portfolio
        :param return_function: the function used to calculate the instruments return
        :param horizon_days: number of days for which we estimate the return based on the one-day return
        :return: instrument_timeseries dataframe with new 'pnl_vector' column
        """
        df_instrument_pnl_vector = Instrument._calculate_instrument_pnl_vector(instrument_timeseries,portfolio_value,return_function,horizon_days)
        return df_instrument_pnl_vector