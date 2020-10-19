#   hokohoko/standard/_DoNothing.py
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
#   This is a dummy predictor, which makes no predictions.
#

from typing import Iterable, Optional

import multiprocessing as mp

from hokohoko.entities import Bar, Predictor


class DoNothing(Predictor):
    """
    This Predictor does nothing at all, which causes Hokohoko to
    generate a lot of DONT_BUY, DONT_SELL Orders.
    """

    def __init__(
            self,
            lock: mp.Lock,
            parameters: Optional[str] = None
    ) -> None:
        """
        :param lock:        A single lock shared by all Predictors in
                            each Period for this invocation. Stored in
                            ``self.lock``.
        :type lock:         multiprocessing.Lock

        :param parameters:  The parameters passed in from
                            ``hokohoko.entities.Config``.
                            Stored in ``self.parameters``.
        :type parameters:   str
        """
        super().__init__(lock, parameters)

    def __enter__(self) -> Predictor:
        """
        Does nothing.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Does nothing.
        """
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        """
        Does nothing.

        :param bars: The list of opening values for the Period.
        :type bars:  list[hokohoko.entities.Bar]
        """
        pass

    def on_bar(self, bars: Iterable[Bar]) -> None:
        """
        Does nothing, which is the same as declaring DONT_BUY, DONT_SELL on
        every Symbol.

        :param bars: A list containing the just-closed Bar for each Symbol.
        :type bars:  list[hokohoko.entities.Bar]
        """
        pass

    def on_stop(self) -> None:
        """
        Does nothing.
        """
        pass
