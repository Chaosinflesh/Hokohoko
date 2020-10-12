#   hokohoko/example.py
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
#   This is an example predictor, showing how to use Hokohoko
#   programmatically.  It assumes the data file is available locally.
#   The latest data file can be found at <<<TODO: Insert link>>>.
#

import multiprocessing as mp
import sys
from typing import List, Optional

from hokohoko import Hokohoko
from hokohoko.entities import Bar, Config, Direction, Order, Predictor


class Example(Predictor):
    """
    This is an example Predictor. It makes a single random prediction
    per Bar.  It demonstrates:

    1. How to inherit Predictor and override the appropriate methods.
    2. How to use self.random() to access fully-deterministic RNG.
    3. How to access self.Account.  This particular example clears all
       Positions at the end of each bar, as simulate mode doesn't
       normally do that.
    """
    def __init__(
        self,
        lock: mp.Lock,
        parameters: Optional[str] = None
    ) -> None:
        """
        Initialises the Predictor, saving the given parameters for use
        in on_start. It provides the following instance objects for use:

        :param lock:        An lock which is shared between all
                            concurrent Predictor processes.  Intended
                            use is for shared access to external
                            resources, etc.  Stored in self.lock, this
                            is provided for custom Predictors which
                            might need access to shared external
                            resources.
        :type lock:         multiprocessing.Lock

        :param parameters:  User-customisable parameters, which get
                            stored in self.parameters.
        :type parameters:   str, optional

        Note that it is not strictly necessary to override, this is just
        to show how to add your own data structures into a Predictor.

        """
        super().__init__(lock, parameters)
        self.exclamation = "This is an example 'predictor', which inherits from Predictor!"

    def __enter__(self) -> Predictor:
        """
        Simple demonstration of overriding __enter__.

        :returns:   As per Python `with` specification, self.
        :rtype:     hokohoko.entities.Predictor

        """
        print(self.exclamation)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        This has to be overridden, but does nothing in this example, as
        there are no external resources to be released.
        """
        pass

    def on_start(self, bars: List[Bar]) -> None:
        """
        Has to be overridden, as the base class will raise a
        NotImplementedError otherwise.

        :param bars:    The list of Bars containing the opening values
                        for each currency pair.  If set, only the
                        requested subset is provided.
        :type bars:     List[hokohoko.entities.Bar].

        """
        print(f"This is an example Bar: {bars[0]}")

    def on_bar(self, bars: List[Bar]) -> None:
        """
        This routine is where data is provided to the Predictor, and it
        processes it's own logic.  Predictions are indicated to Hokohoko
        by placing Orders, with TAKE_PROFIT indicating the prediction,
        and STOP_LOSSES the predicted amount of drawdown required to
        achieve the TAKE_PROFIT.

        This implementation picks a random direction for each symbol.
        hokohoko.entities.Predictor inherits from Random, so all
        Predictors have access to a deterministic RNG source through
        self. Seeding is controlled by Hokohoko.  Example random calls
        include self.random() and self.randint(), etc.

        :param bars:    The latest bar in the data. This is a list of
                        the selected currencies.  This list is always in
                        the same order - that is, the order of the
                        currencies list provided in self.symbol_ids[].
        :type bars:     List[hokohoko.entities.Bar].

        """

        orders = []

        for b in bars:
            if self.random() > 0.5:
                direction = Direction.BUY
            else:
                direction = Direction.SELL

            orders.append(Order(
                symbol_id=b.symbol_id,
                direction=direction,
                open_bid=None,
                take_profit=None,
                stop_loss=None
            ))
        self.place_orders(orders)


if __name__ == "__main__":
    conf = Config(
        predictor_class="Example",
        assessors=["hokohoko.standard.Logger"],
        data_parameters="data.npz",
        data_subset="EURGBP",
        period_count=32,
        process_count=8
    )
    Hokohoko.run(conf)

    sys.exit()
