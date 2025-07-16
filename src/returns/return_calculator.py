import pandas as pd
import numpy as np
import logging
from typing import Callable

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')


class ReturnCalculator:
    @staticmethod
    def log_shift(time0_value: float, time1_value: float, horizon_days: float) -> float|None:
        """
        Used to calculate a log return for an instrument based on single day data. sqrt(horizon) is then used to estimate
        the N day expectation of this return
        :param time0_value: value at start of the period
        :param time1_value: value at the end of the period
        :param horizon_days: days to estimate return for based on single day of data
        :return: float shift amount
        """
        try:
            if time0_value < 0 or time1_value <= 0:
                raise ValueError("time0_value or time1_value is 0 or negative")
            if time0_value == 0.0:
                raise ZeroDivisionError("Cannot be divided by zero")
            return np.exp(np.log(time1_value / time0_value) * np.sqrt(horizon_days)) - 1
            # return np.exp(np.log(time1_value / time0_value) ) - 1
        except FloatingPointError as fpe:
            logger.error(f"Floating point error during log calculation {fpe}")
        except ZeroDivisionError as zdo:
            logger.error(f"Division by zero in log calculation {zdo}")
            raise
        except ValueError as ve:
            logger.error(f"Value error {ve}")
            raise
        except Exception as e:
            logger.error(f"unexpected error {e}")
            raise


    @staticmethod
    def _calculate_shift_return(df: pd.DataFrame, horizon_days: float, shift_function: Callable) -> pd.DataFrame:
        """
        Applies the shift logic over all rows of the instrument timeseries
        :param df: instrument times series dataframe
        :param horizon_days: days for which the return should be estimated
        :param shift_function: the python callable used to calculate the shift
        :return: instrument time series dataframe with new 'shifted_change' column
        """
        try:
        # the shifted value (row.iloc[1]) corresponds to the previous day's value
            df['shifted_change'] = df.apply(lambda row: shift_function(time0_value=row.iloc[1],
                                                                   time1_value=row.iloc[0],
                                                                   horizon_days=horizon_days), axis=1)
            return df
        except Exception as e:
            logger.error(f"Error while applying shift function: {e}")
            raise


    @staticmethod
    def calculate_return(df: pd.DataFrame, horizon_days: float, shift_function: Callable) -> pd.DataFrame:

      return ReturnCalculator._calculate_shift_return(df,horizon_days,shift_function)

