from datetime import timedelta
from abstract_time_series_generator import AbstractTimeSeriesGenerator
from configurers.configuration_manager import ConfigurationManager
import pandas as pd


class CoefficientsGenerator(AbstractTimeSeriesGenerator):

    def __init__(self, config_manager: ConfigurationManager):
        self.__time_series = None
        self.__date_range = None
        self.__anomaly_mask = None
        self.__config_manager = config_manager

    def generate_time_series(self):
        pass

    def __generate_data_range(self) -> None:
        """
            generate the DatetimeIndex to be used in the time series generation
        """
        date_rng = pd.date_range(start=self.__config_manager.start_date,
                                 end=self.__config_manager.start_date + timedelta(days=self.__config_manager.duration),
                                 freq=self.__config_manager.frequency)
        self.__time_series = date_rng
        self.__date_range = date_rng.copy(deep=True)
