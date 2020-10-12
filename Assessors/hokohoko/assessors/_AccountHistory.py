#   assessors/_AccountHistory.py
#
#   Copyright 2020 Neil Bradley
#
#   This file is part of Hokohoko-Assessors.
#
#   Hokohoko is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Hokohoko is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY# without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Hokohoko.  If not, see <https://www.gnu.org/licenses/>.
#
#   ====================================================================
#
#   The AccountHistory Assessor extracts the minute-by-minute
#   performance of a predictor, per Period. Specifically, it extracts
#   the Balance and Equity information, from initial values of 0.0.
#

"""
==============
AccountHistory
==============
"""
from typing import Iterable

import numpy as np
from scipy.stats import skew, kurtosis

from hokohoko.entities import Assessor


class AccountHistory(Assessor):
    """
    Extracts the Equity and Balance histories of a Hokohoko Predictor, and
    presents them in a table, with a column for each Period.

    .. code-block::

        TODO: Make a useful interactive GUI for easy browsing.

    """

    def __init__(self, parameters):
        """
        :param parameters:  The parameters passed in by the config.
        :type parameters:   str
        """
        super().__init__(parameters)

    def analyse(self, data: Iterable) -> None:
        """
        Receives a list of period_results from the Simulator, and presents them in a user-friendly fashion.

        :param data:    A list of period_results from the process Pool.
        :type data:     Iterable[multiprocessing.pool.AsyncResult[hokohoko.entities.Account]]



        """
        results = np.array([a.get()[1].equity[-1] for a in data], dtype=np.float64)
        for i, r in enumerate(results):
            print(f"{i:03d}:{r:12.2f}")
        print("\nOverall\n-------")
        print(f"{'Average return:':20}{np.average(results):12.2f}\n"
              f"{'S.D.:':20}{np.std(results):12.2f}\n"
              f"{'Skew:':20}{skew(results):12.2f}\n"
              f"{'Kurtosis:':20}{kurtosis(results):12.2f}")
