import random
import pandas as pd
import numpy as np
from datetime import timedelta
from configuration_manager import ConfigurationManager
from sklearn.preprocessing import MinMaxScaler
from abstract_time_series_generator import AbstractTimeSeriesGenerator


random.seed(22)


class TimeSeriesGenerator(AbstractTimeSeriesGenerator):

    def __init__(self, config_manager: ConfigurationManager):
        self.__time_series = None
        self.__date_range = None
        self.__anomaly_mask = None
        self.__config_manager = config_manager

    @property
    def time_series(self):
        return self.__time_series

    def __generate_data_range(self) -> None:
        """
            generate the DatetimeIndex to be used in the time series generation
        """
        date_rng = pd.date_range(start=self.__config_manager.start_date,
                                 end=self.__config_manager.start_date + timedelta(days=self.__config_manager.duration),
                                 freq=self.__config_manager.frequency)
        self.__time_series = date_rng
        self.__date_range = date_rng.copy(deep=True)

    def __add_daily_seasonality(self) -> pd.Series:
        """
            creates the daily seasonality component.

        Returns:
            (
            pd.Series: the daily seasonality component of the time series)

        """
        if self.__config_manager.daily_seasonality == "exist":  # Daily Seasonality
            seasonal_component = np.sin(2 * np.pi * self.__time_series.hour / 24)
            seasonal_component += 1 if self.__config_manager.data_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(self.__time_series.hour)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))
        return pd.Series(seasonal_component)

    def __add_weekly_seasonality(self) -> pd.Series:
        """
            creates the weekly seasonality component.

        Returns:
            (
            pd.Series: the weekly seasonality component of the time series)

        """
        if self.__config_manager.weekly_seasonality == "exist":  # Weekly Seasonality
            seasonal_component = np.sin(2 * np.pi * self.__time_series.dayofweek / 7)
            seasonal_component += 1 if self.__config_manager.data_type == 'multiplicative' else 0
        else:
            seasonal_component = np.zeros(len(self.__time_series)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))
        return pd.Series(seasonal_component)

    def __add_trend(self) -> pd.Series:
        """
            creates the trend component.

        Returns:
            (
            pd.Series: the trend component of the time series)

        """
        if self.__config_manager.trend_level == "exist":
            slope = random.choice([1, -1])
            trend_component = np.linspace(0, self.__config_manager.duration / 30 * slope, len(self.__time_series))\
                if slope == 1 else np.linspace(-1 * self.__config_manager.duration / 30, 0, len(self.__time_series))
        else:  # No Trend
            trend_component = np.zeros(len(self.__time_series)) \
                if self.__config_manager.data_type == 'additive' else np.ones(len(self.__time_series))

        return pd.Series(trend_component)

    def __add_cycles(self):
        """
            creates the cyclic component.
        Returns:
            the cyclic component of the time series
        """
        if self.__config_manager.cyclic_period == "exist":  # Quarterly
            cycle_component = 1 if self.__config_manager.data_type == 'multiplicative' else 0
            cycle_component += np.sin(2 * np.pi * (self.__time_series.quarter - 1) / 4)
        else:  # No Cyclic Periods
            cycle_component = 0 if self.__config_manager.data_type == 'additive' else 1

        return cycle_component

    def __add_noise(self) -> pd.Series:
        """
            Adds noise to the existing time series.
        Returns:
            (
            pd.Series: the time series with noise added.)
        """
        if self.__config_manager.noise_level == "small":
            noise_level = 0.1
            # noise = np.random.normal(0, 0.05, len(data))
        elif self.__config_manager.noise_level == "large":
            noise_level = 0.3
            # noise = np.random.normal(0, 0.1, len(data))
        else:  # No Noise
            noise_level = 0

        noise = np.zeros_like(self.__time_series)
        for i in range(len(self.__time_series)):
            noise[i] = np.random.normal(0, abs(self.__time_series[i]) * noise_level) if noise_level > 0 else 0
        return pd.Series((self.__time_series + noise)[:, 0])

    def __add_outliers(self) -> (pd.Series, np.ndarray):
        """
            Adds outliers to the time series
        Returns:
            (
            pd.Series: the time series with added outliers.
            np.ndarray: a mask indicating whether each point is an outlier or not.)
        """
        num_outliers = int(len(self.__time_series) * self.__config_manager.percentage_outliers)
        outlier_indices = np.random.choice(len(self.__time_series), num_outliers, replace=False)
        data_with_outliers = self.__time_series.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask

    def __add_missing_values(self, percentage_missing=0.05) -> pd.Series:
        """
            Removes some data points to simulate missing values
        Args:
            percentage_missing: the percentage of the data points to be removed

        Returns:
            (
            pd.Series: the time series with simulated missing values.)
        """
        num_missing = int(len(self.__time_series) * percentage_missing)
        missing_indices = np.random.choice(len(self.__time_series), size=num_missing, replace=False)

        data_with_missing = self.__time_series.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing

    def generate_time_series(self) -> (pd.Series, pd.DatetimeIndex, np.ndarray):
        """
            Generates a time series.

        Returns:

        (
            pd.Series: the generated time series.
            pd.DatetimeIndex: the timestamps of each data point in the time series.
            np.ndarray: indicates whether each data point is an anomaly or not.
        )
        """
        self.__generate_data_range()
        if self.__config_manager.data_type == "multiplicative":
            self.__time_series = (self.__add_daily_seasonality() * self.__add_weekly_seasonality() *
                                  self.__add_trend() * self.__add_cycles())
        else:
            self.__time_series = (self.__add_daily_seasonality() + self.__add_weekly_seasonality() +
                                  self.__add_trend() + self.__add_cycles())

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.__time_series = scaler.fit_transform(self.__time_series.values.reshape(-1, 1))
        self.__time_series = self.__add_noise()
        self.__time_series, self.__anomaly_mask = self.__add_outliers()
        self.__time_series = self.__add_missing_values()
        return self.__time_series, self.__date_range, self.__anomaly_mask
