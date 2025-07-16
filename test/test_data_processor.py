import unittest
import pandas as pd
from src.processing.data_processor import DataProcessor



class TestDataProcessor(unittest.TestCase):

    def test_valid_add_shifted_time_column_processing(self):
        df = pd.DataFrame({'timestamp': pd.date_range(start='2020-01-01', periods=3, freq='D')})
        shifted_time_result = DataProcessor.add_shifted_time_column_processing(df)
        self.assertIn('time_shift',shifted_time_result.columns)
        self.assertEqual(len(shifted_time_result),3)
        self.assertTrue(pd.isnull(shifted_time_result['time_shift'].iloc[-1]))

    def test_valid_add_shifted_time_column_processing_empty_df(self):
        df = pd.DataFrame()
        with self.assertRaises(ValueError) :
            DataProcessor.add_shifted_time_column_processing(df)

if __name__ == '__main__':
    unittest.main()