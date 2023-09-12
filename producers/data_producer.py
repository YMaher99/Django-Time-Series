from abc import ABC, abstractmethod
from configurers.configuration_manager import ConfigurationManager
import os


class DataProducer(ABC):

    def __init__(self):
        self._metadata = []
        if not os.path.exists('sample_datasets'):
            os.mkdir('sample_datasets')

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @abstractmethod
    def produce_data(self, time_series_df, config_manager: ConfigurationManager, filename=None):
        """
            Abstract method to produce the time series data
        Args:
            time_series: the time series to be saved to file.
            date_range: the timestamps of the data points in the time series.
            anomaly_mask: indicates whether each point is an anomaly or not.
            config_manager (ConfigurationManager): the configuration manager containing the configs that generated the time series.
            filename: the name of the file to be created, if applicable.
        """
        pass

    @abstractmethod
    def generate_metadata_file(self):
        """
            Abstract method to generate a file containing the metadata of all the generated time series
        """
        pass
