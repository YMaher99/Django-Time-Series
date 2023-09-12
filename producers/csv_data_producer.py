import numpy as np
from data_producer import DataProducer
import pandas as pd
from configuration_manager import ConfigurationManager


class CSVDataProducer(DataProducer):
    def produce_data(self, time_series: pd.Series, date_range: pd.DatetimeIndex,
                     anomaly_mask: np.ndarray, config_manager: ConfigurationManager, filename: str = None) -> None:
        """
            Generates a .csv file containing the time series data
        Args:
            time_series (pandas.Series): the time series to be saved to file.
            date_range (pandas.DatetimeIndex): the timestamps of the data points in the time series.
            anomaly_mask (np.ndarray): indicates whether each point is an anomaly or not.
            config_manager (ConfigurationManager): the configuration manager containing the configs that generated the time series.
            filename (str): the name of the .csv file to be created.

        """
        df = pd.DataFrame({'value': time_series, 'timestamp': date_range, 'anomaly': anomaly_mask})
        df.to_csv(f"./sample_datasets/{filename}.csv", encoding='utf-8', index=False)
        self._metadata.append({'id': str(filename),
                               'data_type': config_manager.data_type,
                               'daily_seasonality': config_manager.daily_seasonality,
                               'weekly_seasonality': config_manager.weekly_seasonality,
                               'noise': config_manager.noise_level,
                               'trend': config_manager.trend_level,
                               'cyclic_period (3 months)': config_manager.cyclic_period,
                               'data_size': config_manager.duration,
                               'percentage_outliers': config_manager.percentage_outliers,
                               'percentage_missing': 0.05,
                               'freq': config_manager.frequency})

    def generate_metadata_file(self):
        """
            Generates a .csv file containing the metadata of all the generated time series
        """
        pd.DataFrame.from_records(self._metadata).to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
