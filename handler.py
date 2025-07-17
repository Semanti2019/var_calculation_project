from src.risk_model.var_model import VaRCalculator
from src.returns.return_calculator import ReturnCalculator
from src.ingestion.data_loader import DataLoader
from src.config.config import ConfigRiskModel
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR Calculation')


class RunHandler:
    @staticmethod
    def run_handler():
        try:
            df_source = DataLoader.read_csv(ConfigRiskModel.LANDING_PATH / ConfigRiskModel.FILE_NAME)
            if df_source.empty:
                raise ValueError("Source dataframe is empty.Ensure the file is correctly loaded")
            missing_column = ConfigRiskModel.REQUIRED_COLUMNS - set(df_source.columns)
            if missing_column:
                raise ValueError("required column is missing")
            ccy1_df = df_source[['ccy-1']].copy()
            ccy2_df = df_source[['ccy-2']].copy()
            if ConfigRiskModel.HORIZON_DAYS <= 0:
                raise ValueError("Horizon days must be a possitive number")
            calculated_var = VaRCalculator.calculate_var(
                [
                    (ccy1_df, ConfigRiskModel.HORIZON_DAYS, ConfigRiskModel.PORTFOLIO_VALUE["ccy-1"],
                     ReturnCalculator.log_shift),
                    (ccy2_df, ConfigRiskModel.HORIZON_DAYS, ConfigRiskModel.PORTFOLIO_VALUE["ccy-2"],
                     ReturnCalculator.log_shift)
                ]
            )
            logger.info("VaR calculation successful")
            print(calculated_var)
        except ValueError as ve:
            logger.error(f"Validation Error {ve}")
            raise
        except Exception as e:
            logger.error(f"unexpected error {e}")
            raise


if __name__ == '__main__':
    RunHandler.run_handler()
