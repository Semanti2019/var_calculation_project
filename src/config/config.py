from pathlib import Path
class ConfigRiskModel:
    #File paths
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    LANDING_PATH = PROJECT_ROOT/Path("data/data_var_calculation")
    FILE_NAME = "ccy_rates.txt"
    #Portfolio parameters
    HORIZON_DAYS = 260
    REQUIRED_COLUMNS = {"ccy-1", "ccy-2"}
    PORTFOLIO_VALUE = {"ccy-1":153084.81,"ccy-2":95891.51}
    #Date parsing
    DATE_FORMAT = "%d/%m/%Y"

