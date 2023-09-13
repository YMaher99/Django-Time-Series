from datetime import timedelta

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from abstract_time_series_generator import AbstractTimeSeriesGenerator
from configurers.django_configuration_manager import DjangoConfigurationManager
import pandas as pd


class CoefficientsGenerator(AbstractTimeSeriesGenerator):

    def __init__(self, config_manager: DjangoConfigurationManager):
        self.__time_series = None
        self.__date_range = None
        self.__anomaly_mask = None
        self.__config_manager = config_manager

    def generate_time_series(self):
        self.__generate_data_range()
        self.__generate_polynomial()
        self.__add_seasonality()
        self.__add_cycles()

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.__time_series = scaler.fit_transform(self.__time_series.values.reshape(-1, 1))
        self.__add_noise()
        self.__time_series, self.__anomaly_mask = self.__add_outliers()
        self.__add_missing_values()
        return pd.DataFrame({'value': self.__time_series,
                             'timestamp': self.__date_range,
                             'anomaly': self.__anomaly_mask})

    def __generate_data_range(self) -> None:
        """
            generate the DatetimeIndex to be used in the time series generation
        """
        date_rng = pd.date_range(start=self.__config_manager.start_date,
                                 end=self.__config_manager.end_date,
                                 freq=self.__config_manager.frequency)
        self.__time_series = date_rng
        self.__date_range = date_rng.copy(deep=True)

    def __generate_polynomial(self):
        self.__time_series = pd.Series(np.polyval(self.__config_manager.trend_coefficients,
                                                  np.arange(self.__date_range)))

    def __add_seasonality(self):
        for seasonality in self.__config_manager.seasonalities:
            if seasonality.frequency == seasonality.DAILY:
                frequency = 2 * np.pi / len(self.__date_range)
            elif seasonality.frequency == seasonality.WEEKLY:
                frequency = 2 * np.pi / (len(self.__date_range) / 7)
            elif seasonality.frequency == seasonality.MONTHLY:
                frequency = 2 * np.pi / (len(self.__date_range) / 30)
            else:
                raise ValueError("Invalid Frequency")

            seasonality_component = (seasonality.amplitude *
                                     np.cos(seasonality.multiplier * frequency * np.arange(
                                         len(self.__date_range)) + seasonality.phase_shift))
            if self.__config_manager.data_type == "additive":
                self.__time_series += pd.Series(seasonality_component)
            elif self.__config_manager.data_type == "multiplicative":
                self.__time_series *= pd.Series(seasonality_component)

    def __add_cycles(self):
        cycle_component = 1 if self.__config_manager.data_type == 'multiplicative' else 0
        cycle_component += (self.__config_manager.cycle_amplitude *
                            np.sin(2 * np.pi * self.__config_manager.cycle_frequency *
                                   np.arange(len(self.__date_range))))
        if self.__config_manager.data_type == "additive":
            self.__time_series += pd.Series(cycle_component)
        elif self.__config_manager.data_type == "multiplicative":
            self.__time_series *= pd.Series(cycle_component)

    def __add_noise(self):
        noise_level = self.__config_manager.noise_level/100.0
        noise = np.zeros_like(self.__time_series)
        for i in range(len(self.__time_series)):
            noise[i] = np.random.normal(0, abs(self.__time_series[i]) * noise_level) if noise_level > 0 else 0
        self.__time_series = pd.Series((self.__time_series + noise)[:, 0])

    def __add_outliers(self):
        num_outliers = int(len(self.__time_series) * self.__config_manager.percentage_outliers)
        outlier_indices = np.random.choice(len(self.__time_series), num_outliers, replace=False)
        data_with_outliers = self.__time_series.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask

    def __add_missing_values(self):
        num_missing = int(len(self.__time_series) * self.__config_manager.missing_percentage)
        missing_indices = np.random.choice(len(self.__time_series), size=num_missing, replace=False)

        data_with_missing = self.__time_series.copy()
        data_with_missing[missing_indices] = np.nan

        self.__time_series = data_with_missing

