from abc import ABC, abstractmethod
from datetime import datetime


class ConfigurationManager(ABC):

    # def __init__(self):
    #     self._start_date = datetime(2021, 7, 1)
    #     self._end_date = datetime(2023, 7, 11)
    #     self._frequency = '1D'
    #     self._daily_seasonality = "no"
    #     self._weekly_seasonality = "no"
    #     self._noise_level = "small"
    #     self._trend_level = "no"
    #     self._cyclic_period = "no"
    #     self._data_type = "additive"
    #     self._percentage_outliers = 0.05
    #     self._datasets_num = 1

    @property
    def datasets_num(self):
        return self._datasets_num

    @property
    def daily_seasonality(self):
        return self._daily_seasonality

    @property
    def cyclic_period(self):
        return self._cyclic_period

    @property
    def noise_level(self):
        return self._noise_level

    @property
    def duration(self):
        return self._duration

    @property
    def start_date(self):
        return self._start_date

    @property
    def weekly_seasonality(self):
        return self._weekly_seasonality

    @property
    def frequency(self):
        return self._frequency

    @property
    def trend_level(self):
        return self._trend_level

    @property
    def percentage_outliers(self):
        return self._percentage_outliers

    @property
    def data_type(self):
        return self._data_type

    @abstractmethod
    def load_config(self):
        """
            Abstract method to load the configuration options
        """
        pass

    @abstractmethod
    def configure(self):
        """
            Abstract method to choose the configuration to be used to generate a time series
        """
        pass
