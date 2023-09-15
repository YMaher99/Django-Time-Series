import numpy as np
import pandas as pd
from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper


class OutlierGenerator(AbstractGeneratorHelper):

    def __init__(self, time_series: pd.Series, percentage_outliers):
        self.time_series = time_series
        self.percentage_outliers = percentage_outliers

    def run(self):
        """
            Adds outliers to the time series
        Returns:
            (
            pd.Series: the time series with added outliers.
            np.ndarray: a mask indicating whether each point is an outlier or not.)
        """
        num_outliers = int(len(self.time_series) * (self.percentage_outliers / 100))
        outlier_indices = np.random.choice(len(self.time_series), num_outliers, replace=False)
        data_with_outliers = self.time_series.copy()
        outliers = np.random.uniform(-1, 1, num_outliers)
        anomaly_mask = np.zeros(len(data_with_outliers), dtype=bool)
        if len(outliers) > 0:
            data_with_outliers[outlier_indices] = outliers
            anomaly_mask[outlier_indices] = True

        return data_with_outliers, anomaly_mask
