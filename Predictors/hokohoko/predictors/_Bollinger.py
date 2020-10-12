#   hokohoko/predictors/_Bollinger.py
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
#   This is an implementation of Bollinger bands.
#   TODO: Continue description, make work, etc.
#

import multiprocessing as mp
import sys
from collections import deque
from typing import List, Optional

import numpy as np

from hokohoko import Hokohoko
from hokohoko.entities import Bar, Config, Direction, Order, Predictor


class Bollinger(Predictor):
    """
    This is an example Predictor. It makes a single random prediction per Bar.
    It demonstrates:

    1. How to inherit Predictor and override the appropriate methods.
    2. How to use self.random() to access fully-deterministic RNG.
    3. How to access self.Account. This particular example clears all Positions at the end of
       each bar, as simulate mode doesn't normally do that.
    """
    def __init__(self, lock: mp.Lock, parameters: Optional[str] = None, debug: Optional[bool] = False) -> None:
        """
        Initialises the Predictor, saving the given parameters for use in on_start. It provides the
        following instance objects for use:

        :param lock:        An lock which is shared between all concurrent Predictor processes.
                            Intended use is for shared access to external resource, etc. Stored in
                            self.lock, provided for custom Predictors which might need access to
                            shared external resources.
        :type lock:         multiprocessing.Lock

        :param parameters:  User-customisable parameters, which get stored in self.parameters.
        :type parameters:   str, optional

        Note that it is not strictly necessary to override, this is just to show how to add your
        own data structures in.

        """
        super().__init__(lock, parameters, debug)
        self._middle = {}

    def __enter__(self) -> Predictor:
        """
        Simple demonstration of overriding __enter__.

        :returns:   As per Python `with` specification, self.
        :rtype:     hokohoko.entities.Predictor

        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        This has to be overridden, but does nothing in this example (there are no resources to be
        released).
        """
        pass

    def on_start(self, bars: List[Bar]) -> None:
        """
        Has to be overridden, the base class raises a NotImplementedError otherwise.

        :param bars:    The list of Bars containing the opening values for each currency pair. If
                        set, only the requested subset is provided.
        :type bars:     A list containing one or more hokohoko.entities.Bar[s].

        """
        print(f"This is an example Bar: {bars[0]}")
        for b in bars:
            self._middle[b.symbol_id] = deque([b.high, b.low])

    def on_bar(self, bars: List[Bar]) -> None:
        """
        This implementation picks a random direction for each symbol. Predictors provide access to
        a deterministic RNG source (themselves), so all random calls should be self.random(),
        self.randint(), etc.

        :param bars:    The latest bar in the data. This is an array of the selected currencies.
        :type bars:     A list containing one or more hokohoko.entities.Bar[s].

        """

        # To ensure simulation matches benchmarking conditions, we need to close all pending orders.
        # This is not strictly required, but this demonstrates how to do it correctly.
        # self.account.pending.clear()
        # position_ids = list(self.account.positions)
        # for pid in position_ids:
        #     self.close_order(pid)

        orders = []

        for b in bars:
            self._middle[b.symbol_id].extend([b.high, b.low])
            while len(self._middle[b.symbol_id]) > 500:
                self._middle[b.symbol_id].popleft()

            middle = np.mean(self._middle[b.symbol_id])
            stdev = np.std(self._middle[b.symbol_id])

            if b.open > middle + stdev:
                direction = Direction.SELL
                take_profit = b.close - 0.01
                stop_loss = b.close + 0.0003
            elif b.open < middle - stdev:
                direction = Direction.BUY
                take_profit = b.close + 0.01
                stop_loss = b.close - 0.0003
            else:
                direction = Direction.DONT_BUY
                take_profit = 0.0
                stop_loss = 0.0

            if __debug__:
                print(middle, b.open, direction.name)

            orders.append(Order(
                symbol_id=b.symbol_id,
                direction=direction,
                open_bid=None,
                take_profit=take_profit,
                stop_loss=None
            ))
        self.place_orders(orders)


if __name__ == "__main__":
    # 1. Benchmark first, it's quicker!
    bench_conf = Config(
        predictor_class="Bollinger",
        assessors=["hokohoko.assessors.Accuracy --show-results True", "hokohoko.assessors.AccountViewer"],
        data_parameters="data.npz",
        data_subset="AUDNZD",
        period_count=256,
        process_count=8
    )
    Hokohoko.run(bench_conf)

    sys.exit()
