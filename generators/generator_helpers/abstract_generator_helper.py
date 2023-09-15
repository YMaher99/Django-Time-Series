from abc import ABC, abstractmethod


class AbstractGeneratorHelper(ABC):

    @abstractmethod
    def run(self):
        pass
