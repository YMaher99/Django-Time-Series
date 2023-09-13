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

    def worker_method_run_sim(self):
        """
        runs a simulator generating its datasets
        """
        while (self.config_manager.current_dataset_num < len(self.config_manager.datasets)-1 and
               not self._stop_event.is_set()):
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
        """
            runs worker_method_run_sim in a separate thread
        """
        thread = threading.Thread(target=self.worker_method_run_sim())
        thread.start()
        thread.join()

    def stop_simulator(self):
        """
            stops a running simulator
        """
        self._stop_event.set()
