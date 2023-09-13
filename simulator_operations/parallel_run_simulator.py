import threading
from generators.abstract_time_series_generator import AbstractTimeSeriesGenerator
from producers.data_producer import DataProducer
from configurers.django_configuration_manager import DjangoConfigurationManager


class ParallelRunSimulator:

    def __init__(self, config_manager: DjangoConfigurationManager, generator: AbstractTimeSeriesGenerator,
                 producer: DataProducer):
        self.config_manager = config_manager
        self.config_manager.load_config()
        self.generator = generator
        self.producer = producer
        self._stop_event = threading.Event()

    def worker_method(self):
        while self.config_manager.current_dataset_num < len(self.config_manager.datasets)-1:
            self.config_manager.configure()
            self.config_manager.datasets[self.config_manager.current_dataset_num].status = self.config_manager.datasets[
                self.config_manager.current_dataset_num].RUNNING
            self.config_manager.datasets[self.config_manager.current_dataset_num].save()
            return_flag = self.producer.produce_data(self.generator.generate_time_series(),
                                                     self.config_manager, str(self.config_manager.current_dataset_num))
            if return_flag:
                self.config_manager.datasets[self.config_manager.current_dataset_num].status = self.config_manager.datasets[
                    self.config_manager.current_dataset_num].SUCCEEDED
                self.config_manager.datasets[self.config_manager.current_dataset_num].save()

        self.producer.generate_metadata_file()

    def run_simulator(self):
        thread = threading.Thread(target=self.worker_method())
        thread.start()

    def stop_simulator(self):
        self._stop_event.set()
