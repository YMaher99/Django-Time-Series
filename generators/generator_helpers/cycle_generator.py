import numpy as np
import pandas as pd

from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper


class CycleGenerator(AbstractGeneratorHelper):

    def __init__(self, time_series: pd.Series, date_range: pd.DatetimeIndex, amplitude, frequency, data_type):
        self.time_series = time_series
        self.date_range = date_range
        self.amplitude = amplitude
        self.frequency = frequency
        self.data_type = data_type

    def run(self):
        """
            adds the cyclic component specified in the config manager.
        """
        cycle_component = 1 if self.data_type == 'multiplicative' else 0
        cycle_component += (self.amplitude *
                            np.sin(2 * np.pi * self.frequency *
                                   np.arange(len(self.date_range))))
        if self.data_type == "additive":
            self.time_series += pd.Series(cycle_component)
        elif self.data_type == "multiplicative":
            self.time_series *= pd.Series(cycle_component)

        return self.time_series
