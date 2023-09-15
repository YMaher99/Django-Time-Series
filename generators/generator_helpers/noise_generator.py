import numpy as np
import pandas as pd

from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper


class NoiseGenerator(AbstractGeneratorHelper):

    def __init__(self, time_series: pd.Series, noise_level):
        self.time_series = time_series
        self.noise_level = noise_level

    def run(self):
        """
            Adds noise to the existing time series as specified in the config manager.
        """
        noise_level = self.noise_level / 100.0
        noise = np.zeros_like(self.time_series)
        for i in range(len(self.time_series)):
            noise[i] = np.random.normal(0, abs(self.time_series[i]) * noise_level) if noise_level > 0 else 0
        return pd.Series((self.time_series + noise)[:, 0])
