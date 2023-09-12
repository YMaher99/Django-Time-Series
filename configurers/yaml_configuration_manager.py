import random
from datetime import datetime
from configuration_manager import ConfigurationManager
import yaml


class YAMLConfigurationManager(ConfigurationManager):

    def __init__(self):
        super().__init__()
        self.__yaml_data = None

    @property
    def yaml_data(self):
        return self.__yaml_data

    @yaml_data.setter
    def yaml_data(self, value):
        self.__yaml_data = value

    def load_config(self):
        """
            loads configuration options from config.yaml
        """
        with open("config.yaml", 'r') as file:
            self.__yaml_data = yaml.safe_load(file)

    def configure(self):
        """
            chooses the configuration to be used for the generation of a time series
        """
        self._start_date = datetime.strptime(self.__yaml_data['start_date'], "%d-%m-%Y")
        self._duration = random.choice(self.__yaml_data['data_sizes'])
        self._frequency = random.choice(self.__yaml_data['frequencies'])
        self._daily_seasonality = random.choice(self.__yaml_data['daily_seasonality_options'])
        self._weekly_seasonality = random.choice(self.__yaml_data['weekly_seasonality_options'])
        self._noise_level = random.choice(self.__yaml_data['noise_levels'])
        self._trend_level = random.choice(self.__yaml_data['trend_levels'])
        self._cyclic_period = random.choice(self.__yaml_data['cyclic_periods'])
        self._data_type = random.choice(self.__yaml_data["data_types"])
        self._percentage_outliers = random.choice(self.__yaml_data["percentage_outliers_options"])
        self._datasets_num = self.__yaml_data["datasets_num"]
