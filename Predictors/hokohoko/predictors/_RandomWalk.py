#   hokohoko/predictors/_RandomWalk.py
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
#   This is an implementation of a basic Random Walk predictor.
#   TODO: Continue description, make work, etc.
#

from typing import Iterable

from hokohoko.entities import Predictor, Bar, Direction, Order


class RandomWalk(Predictor):
    """
    This predictor is a simple Random Walk - it predicts the same 1st-order difference.
    """
    def __enter__(self) -> Predictor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        pass

    def on_bar(self, bars: Iterable[Bar]) -> None:
        orders = []

        for b in bars:
            diff = b.close - b.open
            if diff > 0:
                orders.append(Order(
                    symbol_id=b.symbol_id,
                    direction=Direction.BUY,
                    open_bid=None,
                    take_profit=b.close + diff,
                    stop_loss=None
                ))
            elif diff < 0:
                orders.append(Order(
                    symbol_id=b.symbol_id,
                    direction=Direction.SELL,
                    open_bid=None,
                    take_profit=b.close + diff,
                    stop_loss=None
                ))

        self.place_orders(orders)
