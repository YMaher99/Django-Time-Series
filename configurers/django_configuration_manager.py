from configurers.configuration_manager import ConfigurationManager
from simulator_api import models


class DjangoConfigurationManager(ConfigurationManager):

    def __init__(self, simulator: models.Simulator):
        super().__init__()
        self.__simulator = simulator
        self.__current_dataset_num = -1
        self.__datasets = list(simulator.datasets.all())

    @property
    def datasets(self):
        return self.__datasets

    @property
    def seasonalities(self):
        return self._seasonalities

    @property
    def trend_coefficients(self):
        return self._trend_coefficients

    @property
    def current_dataset_num(self):
        return self.__current_dataset_num

    @property
    def cycle_amplitude(self):
        return self._cycle_amplitude

    @property
    def missing_percentage(self):
        return self._missing_percentage

    @property
    def cycle_frequency(self):
        return self._cycle_frequency

    def load_config(self):
        self._start_date = self.__simulator.start_date
        self._end_date = self.__simulator.end_date
        self._data_type = self.__simulator.type

    def configure(self):
        if self.__current_dataset_num < len(self.__datasets):
            self._frequency = self.__datasets[self.__current_dataset_num].frequency
            self._noise_level = self.__datasets[self.__current_dataset_num].noise_level
            self._trend_coefficients = self.__datasets[self.__current_dataset_num].trend_coefficients
            self._missing_percentage = self.__datasets[self.__current_dataset_num].missing_percentage
            self._percentage_outliers = self.__datasets[self.__current_dataset_num].outlier_percentage
            self._cycle_amplitude = self.__datasets[self.__current_dataset_num].cycle_amplitude
            self._cycle_frequency = self.__datasets[self.__current_dataset_num].cycle_frequency
            self._seasonalities = list(self.__datasets[self.__current_dataset_num].seasonality_components.all())
            self.__current_dataset_num += 1

    @property
    def end_date(self):
        return self._end_date
