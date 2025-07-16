import os.path
import os
import pandas as pd
import logging
from src.utils.validators import ValidateInput

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')

class DataLoader:
    """
    Function to read a TSV file , parse dates and set index
    Includes validation and  exception handling
    """
    try:
        @staticmethod
        def read_csv(file_name: str) -> pd.DataFrame:
            """ Function to read data and generate timeseries dataframe from assignment data"""

            # validate file present or not
            if not os.path.isfile(file_name):
                raise FileNotFoundError(f"File not found: {file_name}")
            # Read tab separated file
            df = pd.read_csv(filepath_or_buffer=file_name, delimiter='\t')
            logger.debug("TSV file loaded successfully")
            # Validate date column is present or not
            if 'date' not in df.columns:
                raise ValueError("The date column is missing in input file")
            df['date'] = pd.to_datetime(df['date'],format="%d/%m/%Y")
            date_validation_result = ValidateInput.date_validation(df)
            if not date_validation_result[0]:
                raise ValueError("Some date value could not be parsed")
            # set date as index
            df.set_index('date',inplace=True)
            return df
    except ValueError as ve:
        logger.error(f"Value Error {ve}")
        raise
    except FileNotFoundError as fe:
        logger.error(f"file not found error {fe}")
        raise
    except Exception as e:
        logger.error(f"unexpected error {e}")
        raise
