from configuration_manager import ConfigurationManager
from simulator_api import models
class DjangoConfigurationManager(ConfigurationManager):

    def __init__(self, simulator: models.Simulator):
        super().__init__()
        self.__simulator = simulator

    def load_config(self):
        pass

    def configure(self):
        pass