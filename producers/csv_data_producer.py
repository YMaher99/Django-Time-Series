from producers.data_producer import DataProducer
import pandas as pd
from configurers.django_configuration_manager import DjangoConfigurationManager


class CSVDataProducer(DataProducer):
    def produce_data(self, time_series_df, config_manager: DjangoConfigurationManager, filename: str = None):
        """
            Generates a .csv file containing the time series data
        Args:
            time_series_df (pandas.Dataframe): the time series to be saved to file.
            config_manager (ConfigurationManager): the configuration manager containing the configs that generated the time series.
            filename (str): the name of the .csv file to be created.

        """
        time_series_df.to_csv(f"./sample_datasets/{filename}.csv",
                              encoding='utf-8', index=False)
        self._metadata.append({'id': str(filename),
                               'start_date': config_manager.start_date,
                               'end_date': config_manager.end_date,
                               'data_type': config_manager.data_type,
                               'frequency': config_manager.frequency,
                               'noise_level': config_manager.data_type,
                               'trend_coefficients': config_manager.trend_coefficients,
                               'missing_percentage': config_manager.missing_percentage,
                               'outliers_percentage': config_manager.percentage_outliers,
                               'cycle_amplitude': config_manager.cycle_amplitude,
                               'cycle_frequency': config_manager.cycle_frequency,
                               })

        for idx, seasonality in enumerate(config_manager.seasonalities):
            self.metadata[-1][f'seasonality_frequency_{idx}'] = seasonality.frequency
            self.metadata[-1][f'seasonality_amplitude_{idx}'] = seasonality.amplitude
            self.metadata[-1][f'seasonality_phase_shift_{idx}'] = seasonality.phase_shift
            self.metadata[-1][f'seasonality_multiplier_{idx}'] = seasonality.multiplier

        # for attr_name, attr_value in config_manager.__dict__.items():
        #     self._metadata[-1][attr_name] = attr_value

        return True

    
    def generate_metadata_file(self):
        """
            Generates a .csv file containing the metadata of all the generated time series
        """
        pd.DataFrame.from_records(self._metadata).to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)
