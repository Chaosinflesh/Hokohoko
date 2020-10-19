#   hokohoko/entities/_Position.py
#
#   Copyright 2020 Neil Bradley
#
#   This file is part of Hokohoko.
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
#   Contains the definition of Hokohoko's Position object.
#

from typing import Union

import numpy as np

from hokohoko.entities._Bar import Bar
from hokohoko.entities._Order import Order
from hokohoko.entities._Status import Status


class Position:
    """
    A Position is an Order that has been activated. It includes all the
    relevant information for assessing the effectiveness of the Order,
    for parsing with an Assessor.

    """

    def __init__(
            self,
            order: Order,
            future: Bar,
            status: Status,
            open_time: Union[int, np.int64],
            close_time: Union[int, np.int64],
            open_rate: Union[float, np.float32],
            close_rate: Union[float, np.float32],
            held_value: Union[float, np.float64],
            initial_value: Union[float, np.float64],
            final_value: Union[float, np.float64]
    ):
        """
        :param order:   The Order linked to this Position. Note: the Order may
                        not have been activated, but will still be listed.
        :type order:    hokohoko.entities.Order

        :param future:  The future Bar this Order was active during.
        :type future:   hokohoko.entities.Bar

        :param status:  The closing Status of the Order.
        :type status:   hokohoko.entities.Status.

        :param open_time:   The UTC timestamp when the Order was opened, if
                            applicable.
        :type open_time:    numpy.int64

        :param close_time:  The UTC timestamp when the Order was closed, if
                            applicable.
        :type close_time:   numpy.int64

        :param open_rate:   The rate at which the Order opened. This may differ
                            from the requested rate, due to slippage.
        :type open_rate:    numpy.float32

        :param close_rate:  The rate at which the Order closed. This may differ
                            from the requested rate, due to slippage.
        :type close_rate:   numpy.float32

        :param held_value:  An internal value used to calculate
                            minute-by-minute Equity during benchmarking.
        :type held_value:   numpy.float64

        :param initial_value:   An internal value used to calculate Balance
                                changes. This is the initial Equity for the
                                Position.
        :type initial_value:    numpy.float64

        :param final_value:     An internal value used to calculate Balance
                                changes. This is the final Equity for the
                                Postion.
        :type final_value:      numpy.float64
        """
        self.order = order
        self.future = future
        self.status = status
        self.open_time = open_time
        self.close_time = close_time
        self.open_rate = open_rate
        self.close_rate = close_rate
        self.held_value = held_value
        self.initial_value = initial_value
        self.final_value = final_value

    def __str__(self):
        return "\n\t\t{}\n\t\t{}\n\t\t{}\n\t\t\t{} -> {}\n\t\t\t{} -> {}\n\t\t\t{} -> {}".format(
            self.order,
            self.future,
            self.status,
            self.open_time,
            self.close_time,
            self.open_rate,
            self.close_rate,
            self.initial_value,
            self.final_value
        )

    def __repr__(self):
        return self.__str__()
