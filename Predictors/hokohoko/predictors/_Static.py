#   hokohoko/predictors/_Static.py
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
#   This is not so much a predictor, as a trading strategy using fixed
#   TAKE_PROFIT and STOP_LOSS values.
#   TODO: Continue description, make work, etc.
#

from typing import Iterable

from hokohoko.entities import Predictor, Bar, Order, Direction


class Static(Predictor):
    """
    This allows the testing of purely static settings, e.g. TAKE_PROFIT set to 0.01 (100 pips).
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
            # 100 pips.
            orders.append(Order(b.symbol_id, Direction.BUY, None, b.close + 0.01, None))
            orders.append(Order(b.symbol_id, Direction.SELL, None, b.close - 0.01, None))

        self.place_orders(orders)
