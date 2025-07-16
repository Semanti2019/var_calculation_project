import unittest
import pandas as pd
import numpy as np
from typing import List, Tuple
from src.returns.return_calculator import ReturnCalculator
from unittest.mock import patch


def mock_shift_function(time0_value, time1_value, horizon_days):
    return np.exp(np.log(time1_value / time0_value) * np.sqrt(horizon_days)) - 1


class TestReturnCalculator(unittest.TestCase):

    def setUp(self):
        # Create mock daily price series (3 days)
        dates = pd.date_range(start='2020-01-01', periods=3, freq='D')
        prices_0 = [105.0,102.0,100.0] # linear increase
        prices_1 = [100.0,98.0,96.0]
        self.df = pd.DataFrame({'price_t0': prices_0,'price_t1': prices_1}, index=dates)
        self.horizon_days = 1.0
        # self.df['shifted_change'] = self.df['shifted_change'].pct_change().fillna(0) # dummy shift return
        self.portfolio_value = 1000000

    def test_valid_log_shift(self):
        result_log_shift = ReturnCalculator.log_shift(100.0,110.0,10.0)
        expected_log_shift = np.exp(np.log(110.0 / 100.0) * np.sqrt(10.0)) - 1
        self.assertAlmostEqual(result_log_shift,expected_log_shift)

    def test_log_shift_invalid_timeseries(self):
        # result_log_shift = ReturnCalculator.log_shift(0.0,110.0,10.0)
        # expected_log_shift = np.exp(np.log(110.0 / 0.0) * np.sqrt(10.0)) - 1
        with self.assertRaises(ZeroDivisionError) :
            ReturnCalculator.log_shift(0.0,110.0,10.0)
        with self.assertRaises(ValueError) :
            ReturnCalculator.log_shift(100.0,0.0,10.0)
        with self.assertRaises(ValueError) :
            ReturnCalculator.log_shift(100.0,-110.0,10.0)

    def test_calculate_shift_return_valid(self):
        shift_result_df = ReturnCalculator._calculate_shift_return(self.df.copy(),horizon_days=self.horizon_days,shift_function=mock_shift_function)
        # expected_shift_result_df = [mock_shift_function(102.0,100.0,1.0),mock_shift_function(105.0,102.0,1.0),mock_shift_function(107,105,1.0),np.nan]
        self.assertFalse(np.isnan(shift_result_df['shifted_change'].iloc[-1]))

    def test_calculate_shift_return_empty_df(self):
        empty_df =  pd.DataFrame()
        with self.assertRaises(ValueError):
            ReturnCalculator._calculate_shift_return(df = empty_df ,horizon_days=self.horizon_days,shift_function=mock_shift_function )


if __name__ == '__main__':
    unittest.main()