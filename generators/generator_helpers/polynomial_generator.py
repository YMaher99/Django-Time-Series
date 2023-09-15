from generators.generator_helpers.abstract_generator_helper import AbstractGeneratorHelper
import pandas as pd
import numpy as np


class PolynomialGenerator(AbstractGeneratorHelper):

    def __init__(self, date_range: pd.DatetimeIndex, coefficients_list: list):
        self.date_range = date_range
        self.coefficients_list = coefficients_list

    def run(self):
        return pd.Series(np.polyval(self.coefficients_list,
                                    np.arange(len(self.date_range))))
