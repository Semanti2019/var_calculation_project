import pandas as pd
from typing import Tuple
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')
class ValidateInput:
    @staticmethod
    def date_validation(df) -> Tuple[bool,dict]:
        """
        Validate a DataFrame's date column.
        :param df:
        :return: A tuple of (overall_valid,detailed_validation_dict)
        """
        result_date_validation ={
            "all_dates_parsable": False,
            "no_missing_dates": False,
            "no_future_dates": False
        }
        try:
            result_date_validation["all_dates_parsable"] = bool(pd.to_datetime(df['date'], format= "%d/%m/%Y",errors="coerce").notna().all())
            result_date_validation["no_missing_dates"] = bool(not pd.to_datetime(df['date'], format= "%d/%m/%Y",errors="coerce").isna().any())
            # Checks future dates
            result_date_validation["no_future_dates"] = bool((pd.to_datetime(df['date'], format= "%d/%m/%Y",errors="coerce") <= pd.Timestamp.today()).all())
            validation_check = all(result_date_validation.values())
            logger.info(f"Date Validation Result: {result_date_validation},{validation_check}")
            return validation_check , result_date_validation
        except Exception as e:
            print(f"Date parsing failed: {e}")
            return False,result_date_validation
    @staticmethod
    def no_of_column_validation(df)->bool|None:
        """
        Validate no of columns in dataframe.
        :param df:
        :return: bool
        """
        required_columns = ["date","Portfolio","ccy-1","ccy-2"]
        try:
            if list(df.columns) == required_columns:
                logger.info(f"Required Columns: {required_columns},Actual Columns {df.columns}")
                return True
        except:
            raise ValueError("No of columns mismatch")

    @staticmethod
    def is_null_or_negative_validation(df)-> bool|None:
        """
        Validate null and negative value for currency check
        :param df:
        :return: bool
        """
        if df[['ccy-1','ccy-2']].isnull().any().any() or (df[['ccy-1','ccy-2']] <= 0).any().any():
            logger.info("Null or Negative value in currency column")
            raise ValueError("Null or Negative value in currency column")
        logger.info("No Null or Negative value in currency column")
        return True












