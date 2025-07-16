from src.risk_model.var_model import PortfolioVaRCalculator
from src.returns.return_calculator import ReturnCalculator
from src.ingestion.data_loader import DataLoader
from src.config.config import ConfigRiskModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')

if __name__ == "__main__":
    df_source = DataLoader.read_csv(ConfigRiskModel.LANDING_PATH/ConfigRiskModel.FILE_NAME)
    # date_validation_result = ValidateInput.date_validation(df_source)
    # column_validation_result = ValidateInput.no_of_column_validation(df_source)
    # currency_value_validation = ValidateInput.is_null_or_negative_validation(df_source)
    # try:
    #     if date_validation_result[0] & column_validation_result & currency_value_validation:
    #         logger.info("File moved")
    # except PermissionError as pe:
    #     logger.error(f"permission denied {pe}")
    # except FileNotFoundError as fe:
    #     logger.error(f"file not found error {fe}")
    # except Exception as e:
    #     logger.error(f"unexpected error {e}")
    ccy1_df = df_source[['ccy-1']].copy()
    ccy2_df = df_source[['ccy-2']].copy()
    obj = PortfolioVaRCalculator.calculate_var([(ccy1_df,ConfigRiskModel.HORIZON_DAYS,ConfigRiskModel.PORTFOLIO_VALUE["ccy-1"],ReturnCalculator.log_shift),(ccy2_df,ConfigRiskModel.HORIZON_DAYS,ConfigRiskModel.PORTFOLIO_VALUE["ccy-2"],ReturnCalculator.log_shift)])
    print(obj)