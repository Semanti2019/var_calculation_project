import pandas as pd
import logging
from typing import Callable
from src.processing.data_processor import DataProcessor
from src.returns.return_calculator import ReturnCalculator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR_Calculation')

class Instrument:

    @staticmethod
    def _calculate_pnl_for_shift(df: pd.DataFrame, portfolio_value: float) -> pd.DataFrame|None:
        """
        Multiply the estimated daily return by the value of the instrument in the portfolio
        :param df: instrument time series dataframe
        :param portfolio_value: Value of the instrument in the portfolio
        :return: instrument time series dataframe with new 'pnl_vector' column
        """
        try:
            if 'shifted_change' not in df.columns or df['shifted_change'].isnull().any():
                raise ValueError("'shifted_change' column is missing or having NaN value")
            df['pnl_vector'] = df['shifted_change'] * portfolio_value
            if 'pnl_vector' not in df.columns or df['pnl_vector'].isnull().any():
                raise ValueError("'pnl_vector' is missing or contains NaN.")
            return df
        except ValueError as ve:
            print(ve)


    @staticmethod
    def _calculate_instrument_pnl_vector(instrument_timeseries: pd.DataFrame, portfolio_value: float,
                                         return_function: Callable, horizon_days: float) -> pd.DataFrame|None:
        """
        Calculates the PnL for the given portfolio given the historical returns found in the instrument time series
        :param instrument_timeseries: a dataframe with business date index containing instrument values on those days
        :param portfolio_value: Value of the instrument in the portfolio
        :param return_function: the function used to calculate the instruments return
        :param horizon_days: number of days for which we estimate the return based on the one-day return
        :return: instrument_timeseries dataframe with new 'pnl_vector' column
        """
        try:
            instrument_timeseries = DataProcessor.add_shifted_time_column_processing(instrument_timeseries)
            instrument_timeseries = ReturnCalculator.calculate_return(instrument_timeseries, horizon_days=horizon_days,
                                                                      shift_function=return_function)
            return Instrument._calculate_pnl_for_shift(df=instrument_timeseries, portfolio_value=portfolio_value)
        except ValueError as ve:
            print("'pnl_vector' is missing or contains NaN.")
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
        if 'pnl_vector' not in df_instrument_pnl_vector:
            raise TypeError("'pnl_vector' is missing or contains NaN.")
        if df_instrument_pnl_vector['pnl_vector'].isnull().any():
            raise  TypeError("Contains null or zero value")
        return df_instrument_pnl_vector