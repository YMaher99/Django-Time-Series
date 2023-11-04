from abc import ABC, abstractmethod
import pandas as pd


class AbstractTimeSeriesGenerator(ABC):

    @abstractmethod
    def generate_time_series(self) -> pd.DataFrame:
        """
            Abstract method to generate a time series
        """
        pass
