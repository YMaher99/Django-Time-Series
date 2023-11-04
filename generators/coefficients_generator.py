import numpy as np
from sklearn.preprocessing import MinMaxScaler

from generators.abstract_time_series_generator import AbstractTimeSeriesGenerator
from configurers.django_configuration_manager import DjangoConfigurationManager
import pandas as pd
from generators.generator_helpers.data_range_generator import DataRangeGenerator
from generators.generator_helpers.missing_value_generator import MissingValueGenerator
from generators.generator_helpers.noise_generator import NoiseGenerator
from generators.generator_helpers.outlier_generator import OutlierGenerator
from generators.generator_helpers.polynomial_generator import PolynomialGenerator
from generators.generator_helpers.seasonalities_generator import SeasonalitiesGenerator
from generators.generator_helpers.cycle_generator import CycleGenerator


class CoefficientsGenerator(AbstractTimeSeriesGenerator):

    def __init__(self, config_manager: DjangoConfigurationManager):
        self.__time_series = None
        self.__date_range = None
        self.__anomaly_mask = None
        self.__config_manager = config_manager

    def generate_time_series(self) -> pd.DataFrame:
        """
            Generates a time series based on the configurations found in the config manager.

        Returns:

        (
            pd.Series: the generated time series as a dataframe
        )
        """
        self.__date_range = DataRangeGenerator(start_date=self.__config_manager.start_date,
                                               end_date=self.__config_manager.end_date,
                                               frequency=self.__config_manager.frequency).run()

        self.__time_series = PolynomialGenerator(date_range=self.__date_range,
                                                 coefficients_list=self.__config_manager.trend_coefficients).run()

        self.__time_series = SeasonalitiesGenerator(time_series=self.__time_series,
                                                    date_range=self.__date_range,
                                                    seasonalities=self.__config_manager.seasonalities,
                                                    data_type=self.__config_manager.data_type).run()
        self.__time_series = CycleGenerator(time_series=self.__time_series,
                                            date_range=self.__date_range,
                                            amplitude=self.__config_manager.cycle_amplitude,
                                            frequency=self.__config_manager.cycle_frequency,
                                            data_type=self.__config_manager.data_type).run()

        scaler = MinMaxScaler(feature_range=(-1, 1))
        self.__time_series = scaler.fit_transform(self.__time_series.values.reshape(-1, 1))

        self.__time_series = NoiseGenerator(time_series=self.__time_series,
                                            noise_level=self.__config_manager.noise_level).run()

        self.__time_series, self.__anomaly_mask = OutlierGenerator(time_series=self.__time_series,
                                                                   percentage_outliers=self.__config_manager.percentage_outliers).run()
        self.__time_series = MissingValueGenerator(time_series=self.__time_series,
                                                   missing_percentage=self.__config_manager.missing_percentage).run()

        return pd.DataFrame({'value': self.__time_series,
                             'timestamp': self.__date_range,
                             'anomaly': self.__anomaly_mask})

