import pandas as pd
import logging
from typing import Callable, Tuple
from src.instrument.instrument_portfolio_allocation import Instrument

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('VaR_Calculation')


class VaRCalculator:
    try:
        @staticmethod
        def _calculate_99_var_from_total_pnls(total_pnl_vector: pd.Series) -> float:
            """
            Performs a .99 confidence level VaR calculation -> (0.4 * second worst PnL) + (0.6 * third worst PnL)

            Assumes total_pnl_vector contains 260 days of pnls values

            :param total_pnl_vector: the series of historical returns for the instrument in the portfolio
            :return: float VaR value
            """
            if not isinstance(total_pnl_vector, pd.Series):
                raise TypeError("Expected a pandas series for PnL vector")
            sorted_returns = total_pnl_vector.sort_values()
            return sorted_returns.iloc[1] * 0.4 + sorted_returns.iloc[2] * 0.6

        @staticmethod
        def calculate_var(calculation_config: list[Tuple[pd.DataFrame, float, float, Callable]]) -> float:
            """
            Performs a .99 confidence level VaR calculation for all instruments in a given portfolio.

            instrument time series should contain 260 days of instruments prices.

            Configured using a calculation config, e.g.:

            calculation_config = [(instrument 1 timeseries, horizon_days, instrument 1 value in portfolio,
                                   instrument 1 shift function),
                                  (instrument 2 timeseries, horizon_days, instrument 2 value in portfolio,
                                   instrument 2 shift function), ...]

            :param calculation_config: List of tuples providing data and calculation methodology
            :return: a value for VaR for the configured portfolio
            """
            if not calculation_config:
                raise ValueError("Calculation_config is empty")
            if not isinstance(calculation_config, list) and all(isinstance(item, tuple) for item in calculation_config):
                raise ValueError("Input config must be list of 4 element tuples")
            logger.info(f'Received calculation config containing {len(calculation_config)} instruments')
            for entry in calculation_config:
                if len(entry) != 4:
                    raise ValueError(f"Each config entry must be tuple of 4 elements: got {len(entry)}")
                if not isinstance(entry[0], pd.DataFrame):
                    raise TypeError("Timeseries data must be a pandas dataframe")
            portfolio_total_pnl_vector = pd.Series(index=calculation_config[0][0].index, data=0)
            for (timeseries, _horizon_days, portfolio_value, return_function) in calculation_config:
                logger.info(
                    f'calculating return pnls for instrument using N={_horizon_days}, portfolio_value={portfolio_value}'
                    f', return_function={return_function.__name__}')
                component_pnl = Instrument.calculate_instrument_pnl_vector(instrument_timeseries=timeseries,
                                                                           portfolio_value=portfolio_value,
                                                                           return_function=return_function,
                                                                           horizon_days=_horizon_days)

                if component_pnl.empty or 'pnl_vector' not in component_pnl:
                    raise ValueError("component_pnl calculation failed")
                portfolio_total_pnl_vector += component_pnl['pnl_vector']

            return VaRCalculator._calculate_99_var_from_total_pnls(total_pnl_vector=portfolio_total_pnl_vector)
    except ValueError as ve:
        logger.error(f"Value Error {ve}")
    except TypeError as te:
        logger.error(f"file not found error {te}")
    except Exception as e:
        logger.error(f"unexpected error {e}")
