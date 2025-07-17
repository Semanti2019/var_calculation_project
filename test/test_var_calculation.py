import unittest
import pandas as pd
import numpy as np
from typing import List, Tuple
from src.risk_model.var_model import VaRCalculator
from unittest.mock import patch


def mock_shift_function(t0, t1, horizon_days):
    return np.exp(np.log(t1 / t0) * np.sqrt(horizon_days)) - 1


class TestVaRCalculation(unittest.TestCase):

    def setUp(self):
        # Create mock daily price series (10 days)
        dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
        prices = [100.0 + i for i in range(10)]  # linear increase
        df = pd.DataFrame({'ccy_1': prices}, index=dates)
        df['shifted_change'] = df['ccy_1'].pct_change().fillna(0)  # dummy shift return
        df.dropna()
        self.df = df[df['shifted_change'] != 0.0]

        self.horizon_days = 9
        self.portfolio_value = 1000000
        self.valid_config: List[Tuple[pd.DataFrame, float, float, callable]] = [
            (self.df[['ccy_1']], self.horizon_days, self.portfolio_value,
             lambda time0_value, time1_value, horizon_days: 9)
        ]

    def test_valid_var_calculation(self):
        result = VaRCalculator.calculate_var(self.valid_config)
        self.assertIsInstance(result, float)

    def test_empty_dataframe(self):
        config = [
            (pd.DataFrame(), self.horizon_days, self.portfolio_value,
             lambda time0_value, time1_value, horizon_days: 0.01)
        ]
        with self.assertRaises(TypeError):
            VaRCalculator.calculate_var(config)

    def test_missing_column_config(self):
        df = self.df.drop(columns=['ccy_1'])
        config = [(self.horizon_days, self.portfolio_value, lambda time0_value, time1_value, horizon_days: 0.01)]
        with self.assertRaises(ValueError) as ve:
            VaRCalculator.calculate_var(config)
            # assert ke.msg == KeyError.args.

    def test_invalid_config_type(self):
        config = ['not_a_tuple']
        with self.assertRaises(ValueError):
            VaRCalculator.calculate_var(config)

    def test_single_value_series(self):
        df = pd.DataFrame({'ccy_1': [100]}, index=[pd.Timestamp('2020-01-01')])
        config = [(df, self.horizon_days, self.portfolio_value, lambda time0_value, time1_value, horizon_days: 0.01)]
        with self.assertRaises(ValueError):
            VaRCalculator.calculate_var(config)

    @patch('src.returns.return_calculator.ReturnCalculator._calculate_shift_return', autospec=True)
    def test_nan_in_shifted_column(self, mock_shift_return):
        df = self.df.copy()
        df['shifted_change'] = [np.nan] * len(df)
        df['pnl_vector'] = [0.0] * len(df)
        mock_shift_return.return_value = df
        config = [(df, self.horizon_days, self.portfolio_value, lambda time0_value, time1_value, horizon_days: 0.01)]
        with self.assertRaises(ValueError):
            VaRCalculator.calculate_var(config)


if __name__ == '__main__':
    unittest.main()
