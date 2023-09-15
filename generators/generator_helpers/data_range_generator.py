import pandas as pd

from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper
from datetime import datetime


class DataRangeGenerator(AbstractGeneratorHelper):

    def __init__(self, start_date: datetime, end_date: datetime, frequency):
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency

    def run(self):
        return pd.date_range(start=self.start_date,
                             end=self.end_date,
                             freq=self.frequency)
