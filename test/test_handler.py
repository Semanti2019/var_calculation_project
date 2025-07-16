import unittest
import pandas as pd
import numpy as np
from handler import RunHandler
from unittest.mock import patch


def mock_shift_function(t0, t1, horizon_days):
    return np.exp(np.log(t1 / t0) * np.sqrt(horizon_days)) - 1


class TestHandler(unittest.TestCase):

    @patch('src.risk_model.var_model.VaRCalculator.calculate_var',autospec=True)
    @patch('src.ingestion.data_loader.DataLoader.read_csv',autospec=True)
    @patch('src.config.config',autospec=True)
    def test_successful_run(self, mock_config, mock_read_csv, mock_calculate_var):
        df = pd.DataFrame({
            'ccy-1': [1.1, 1.2, 1.3],
            'ccy-2': [0.9, 1.0, 1.1]
        })
        mock_read_csv.return_value = df
        mock_config.REQUIRED_COLUMNS = {"ccy-1", "ccy-2"}
        mock_config.HORIZON_DAYS = 10
        mock_config.PORTFOLIO_VALUE = {"ccy-1": 1000000, "ccy-2": 500000}

        result_mock = pd.DataFrame({'VaR': [1234.56]})
        mock_calculate_var.return_value = result_mock

        RunHandler.run_handler()
        mock_calculate_var.assert_called_once()

    @patch('src.ingestion.data_loader.DataLoader.read_csv',autospec=True)
    def test_empty_source_dataframe(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame()
        with self.assertRaises(ValueError) as context:
            RunHandler.run_handler()
        self.assertIn("dataframe is empty", str(context.exception))



    @patch('src.ingestion.data_loader.DataLoader.read_csv',autospec=True)
    @patch('src.config.config',autospec=True)
    def test_missing_column(self, mock_config, mock_read_csv):
        df = pd.DataFrame({'ccy-1': [1,2,3]}) # ccy-2 is missing
        mock_read_csv.return_value = df
        mock_config.REQUIRED_COLUMNS = {"ccy-1", "ccy-2"}
        with self.assertRaises(ValueError) as context:
            RunHandler.run_handler()
        self.assertIn("required column is missing", str(context.exception))

    @patch('src.ingestion.data_loader.DataLoader.read_csv',autospec=True)
    @patch('handler.ConfigRiskModel',autospec=True)
    def test_invalid_horizon_days(self, mock_config, mock_read_csv):
        df = pd.DataFrame({'ccy-1': [1,2,3],'ccy-2': [0.5,1,1.5]})
        mock_read_csv.return_value = df
        mock_config.REQUIRED_COLUMNS = {"ccy-1", "ccy-2"}
        mock_config.HORIZON_DAYS = -1
        with self.assertRaises(ValueError) as context:
            RunHandler.run_handler()
        self.assertIn("Horizon days must be a possitive number", str(context.exception))


if __name__ == '__main__':
    unittest.main()