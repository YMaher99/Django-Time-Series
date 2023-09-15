import pandas as pd

from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper
import numpy as np


class SeasonalitiesGenerator(AbstractGeneratorHelper):

    def __init__(self, time_series: pd.Series, date_range: pd.DatetimeIndex, seasonalities: list, data_type):
        self.time_series = time_series
        self.date_range = date_range
        self.seasonalities = seasonalities
        self.data_type = data_type

    def run(self):
        """
            adds (daily,weekly,monthly) seasonality to the time series as found in the config manager.
        """
        for seasonality in self.seasonalities:
            if seasonality.frequency == seasonality.DAILY:
                frequency = 2 * np.pi / len(self.date_range)
            elif seasonality.frequency == seasonality.WEEKLY:
                frequency = 2 * np.pi / (len(self.date_range) / 7)
            elif seasonality.frequency == seasonality.MONTHLY:
                frequency = 2 * np.pi / (len(self.date_range) / 30)
            else:
                raise ValueError("Invalid Frequency")

            seasonality_component = (seasonality.amplitude *
                                     np.cos(seasonality.multiplier * frequency * np.arange(
                                         len(self.date_range)) + seasonality.phase_shift))
            if self.data_type == "additive":
                self.time_series += pd.Series(seasonality_component)
            elif self.data_type == "multiplicative":
                self.time_series *= pd.Series(seasonality_component)

        return self.time_series
