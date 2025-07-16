import unittest
import pandas as pd
from src.ingestion.data_loader import DataLoader
from unittest.mock import patch



class TestDataLoader(unittest.TestCase):

    @patch('src.ingestion.data_loader.os.path.isfile',autospec=True)
    def test_file_not_found(self,mock_isfile):
        mock_isfile.return_value = False
        with self.assertRaises(FileNotFoundError) :
            DataLoader.read_csv("ccy_rates.txt")

    @patch('src.ingestion.data_loader.os.path.isfile',autospec=True)
    @patch('src.ingestion.data_loader.pd.read_csv',autospec=True)
    @patch('src.ingestion.data_loader.ValidateInput.date_validation',autospec=True)
    def test_file_successfully_loaded(self,mock_validate,mock_read_csv,mock_isfile):
        df = pd.DataFrame({'date': ['01/01/2020', '02/01/2020'], 'value': [100, 200]})
        mock_read_csv.return_value = df
        mock_validate.return_value = (True, None)
        result = DataLoader.read_csv('ccy_rates.txt')
        self.assertTrue('date' in result.index.names)
        self.assertTrue('value' in result.columns)

if __name__ == '__main__':
    unittest.main()