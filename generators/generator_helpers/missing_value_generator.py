import numpy as np
import pandas as pd

from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper


class MissingValueGenerator(AbstractGeneratorHelper):

    def __init__(self, time_series: pd.Series, missing_percentage):
        self.time_series = time_series
        self.missing_percentage = missing_percentage

    def run(self):
        """
            Removes some data points to simulate missing values
        """
        num_missing = int(len(self.time_series) * self.missing_percentage)
        missing_indices = np.random.choice(len(self.time_series), size=num_missing, replace=False)

        data_with_missing = self.time_series.copy()
        data_with_missing[missing_indices] = np.nan

        return data_with_missing
