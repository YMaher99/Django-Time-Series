from data_producer import DataProducer
import pandas as pd
from configurers.configuration_manager import ConfigurationManager


class CSVDataProducer(DataProducer):
    def produce_data(self, time_series_df, config_manager: ConfigurationManager, filename: str = None) -> None:
        """
            Generates a .csv file containing the time series data
        Args:
            time_series_df (pandas.Dataframe): the time series to be saved to file.
            config_manager (ConfigurationManager): the configuration manager containing the configs that generated the time series.
            filename (str): the name of the .csv file to be created.

        """
        time_series_df.to_csv(f"./sample_datasets/{filename}.csv",
                              encoding='utf-8', index=False)
        self._metadata.append({'id': str(filename)})
        for attr_name, attr_value in config_manager.__dict__.items():
            self._metadata[-1][attr_name] = attr_value

    def generate_metadata_file(self):
        """
            Generates a .csv file containing the metadata of all the generated time series
        """
        pd.DataFrame.from_records(self._metadata).to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
