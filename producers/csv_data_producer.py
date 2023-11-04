from producers.data_producer import DataProducer
import pandas as pd
from configurers.django_configuration_manager import DjangoConfigurationManager


class CSVDataProducer(DataProducer):

    def produce_data(self, time_series_df):
        """
            Generates a .csv file containing the time series data
        Args:
            time_series_df (pandas.Dataframe): the time series to be saved to file.
        """

        time_series_df.to_csv(f"./sample_datasets/{str(self.config_manager.current_dataset_num)}.csv",
                              encoding='utf-8', index=False)
        return True

    def add_metadata(self):
        self._metadata.append({'id': str(self.config_manager.current_dataset_num),
                               'start_date': self.config_manager.start_date,
                               'end_date': self.config_manager.end_date,
                               'data_type': self.config_manager.data_type,
                               'frequency': self.config_manager.frequency,
                               'noise_level': self.config_manager.data_type,
                               'trend_coefficients': self.config_manager.trend_coefficients,
                               'missing_percentage': self.config_manager.missing_percentage,
                               'outliers_percentage': self.config_manager.percentage_outliers,
                               'cycle_amplitude': self.config_manager.cycle_amplitude,
                               'cycle_frequency': self.config_manager.cycle_frequency,
                               })

        for idx, seasonality in enumerate(self.config_manager.seasonalities):
            self.metadata[-1][f'seasonality_frequency_{idx}'] = seasonality.frequency
            self.metadata[-1][f'seasonality_amplitude_{idx}'] = seasonality.amplitude
            self.metadata[-1][f'seasonality_phase_shift_{idx}'] = seasonality.phase_shift
            self.metadata[-1][f'seasonality_multiplier_{idx}'] = seasonality.multiplier

    def generate_metadata_file(self):
        """
            Generates a .csv file containing the metadata of all the generated time series
        """
        pd.DataFrame.from_records(self._metadata).to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
