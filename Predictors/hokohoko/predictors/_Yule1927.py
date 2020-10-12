#   hokohoko/predictors/_Yule1927.py
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
#   This is an implementation of Yule's predictor.
#   TODO: Continue description, make work, etc.
#

from argparse import ArgumentParser
from collections import deque
from typing import Iterable, Optional

import numpy as np
import multiprocessing as mp
import warnings

from hokohoko import defaults
from hokohoko.entities import Bar, Direction, Order, Predictor


class Yule1927(Predictor):
    """
    This Predictor is based on the AR algorithm proposed by Yule in 1927.

    It is a wrapper for AR from statsmodels.
    """

    DEFAULT_WINDOW = 180

    def __init__(
            self,
            lock: mp.Lock,
            args: Optional[str] = None,
            debug: Optional[bool] = False
    ) -> None:
        super().__init__(lock, args, debug)

        # # 0. Arguments
        # ap = ArgumentParser()
        # ap.add_argument('--window', type=int, default=Yule1927.DEFAULT_WINDOW)
        # ap.add_argument('--tp_ratio', type=float, default=defaults.DEFAULT_TP_RATIO)
        # ap.add_argument('--sl_ratio', type=float, default=defaults.DEFAULT_SL_RATIO)
        # ap.add_argument('--sl_min', type=float, default=defaults.DEFAULT_SL_MIN)
        # self.parameters = ap.parse_args(self.parameters.split() if self.parameters is not None else [])
        #
        # # 1. Ratio overrides
        # self._tp_ratio = self.parameters.tp_ratio
        # self._sl_ratio = self.parameters.sl_ratio
        # self._sl_min = self.parameters.sl_min
        #
        # # 2. AR configuration
        # self._window = self.parameters.window
        # self._highs = {}
        # self._lows = {}

    def __enter__(self) -> Predictor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        pass
        # for b in bars:
        #     self._highs[b.symbol_id] = deque([b.high] * self._window, self._window)
        #     self._lows[b.symbol_id] = deque([b.low] * self._window, self._window)

    def on_bar(self, bars: Iterable[Bar]) -> None:

        orders = []
        # for b in bars:
        #     self._highs[b.symbol_id].append(b.high)
        #     self._lows[b.symbol_id].append(b.low)
        #     up_fit = AR(np.array(self._highs[b.symbol_id])).fit(disp=0, trend='nc')
        #     down_fit = AR(np.array(self._lows[b.symbol_id])).fit(disp=0, trend='nc')
        #     up = up_fit.predict(start=self._window, end=self._window)[0] - b.close
        #     down = b.close - down_fit.predict(start=self._window, end=self._window)[0]
        #
        #     buy_tp = b.close + up * self._tp_ratio
        #     buy_sl = b.close - down * self._sl_ratio
        #     sell_tp = b.close - down * self._tp_ratio
        #     sell_sl = b.close + up * self._sl_ratio
        #
        #     # Check for minimum stop-losses.
        #     if buy_sl >= b.close:
        #         buy_sl = b.close - self._sl_min
        #     if sell_sl <= b.close:
        #         sell_sl = b.close + self._sl_min
        #
        #     # Check for don't buy/sell
        #     if buy_tp <= b.close:
        #         buy_d, buy_tp, buy_sl = Direction.DONT_BUY, None, None
        #     else:
        #         buy_d = Direction.BUY
        #     if sell_tp >= b.close:
        #         sell_d, sell_tp, sell_sl = Direction.DONT_SELL, None, None
        #     else:
        #         sell_d = Direction.SELL
        #
        #     orders.extend([
        #         # Order(b.symbol_id, buy_d, None, buy_tp, buy_sl),
        #         # Order(b.symbol_id, sell_d, None, sell_tp, sell_sl)
        #         # This is just for my testing.
        #         Order(b.symbol_id, buy_d, None, buy_tp, None),
        #         Order(b.symbol_id, sell_d, None, sell_tp, None)
        #     ])

        self.place_orders(orders)
