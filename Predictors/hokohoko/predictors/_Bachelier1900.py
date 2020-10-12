#   hokohoko/predictors/_Bachelier1900.py
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
#   This is a predictor based on an implementation of Bachelier's 1900
#   Gaussian probability predictor.
#   TODO: Continue description, make work, etc.
#

from argparse import ArgumentParser
from collections import defaultdict
from typing import Iterable, Optional

import multiprocessing as mp
import numpy as np

from hokohoko import defaults
from hokohoko.entities import Bar, Direction, Order, Predictor


class PerSymbol:

    """
    This contains the data object keeping track of probabilities per-Symbol.
    """
    def __init__(self, y_low, y_high, y_open):
        """
        Initialise the arrays.

        :param y_low:   The opening low price.
        :type y_low:    float

        :param y_high:  The opening high price.
        :type y_high:   float

        :param y_open:  The opening price.
        :type y_open:   float
        """
        self.ranges = set()
        self.deltas = set()
        self.p_ranges = defaultdict(int)
        self.p_deltas = defaultdict(int)
        self.add_epoch(y_low, y_high, y_open)

    def add_epoch(
            self,
            y_low: float,
            y_high: float,
            y_open: float
    ):
        """
        Puts a epoch into sparse data.

        :param y_low:    The low price observed over the Epoch.
        :type y_low:     float

        :param y_high:   The high price observed over the Epoch.
        :type y_high:    float

        :param y_open:   The open price for the Epoch. Used to calculate the range of d_y values.
        :type y_open:    float
        """
        self.ranges.update([y_low, y_high])
        self.deltas.update([y_low - y_open, y_high - y_open])
        self.p_ranges[(y_low, y_high)] += 1
        self.p_deltas[(y_low - y_open, y_high - y_open)] += 1

    def get_highest_probability(self, rate) -> float:
        """
        Calculates from a given rate what price has the highest probability next.

        :param rate:    The current exchange rate. This is treated as the next Epoch's ``open``.
        :type rate:     float

        :return:        The exchange value with the maximum likelihood, as determined by Bachelier's formula.
        :rtype:         float
        """
        # This algorithm is unfortunately O(n^2), but we'll see if we can optimise it later.
        max_seen = [(0, rate)]
        for d in self.deltas:
            to_check = rate + d
            p_d = 0
            p_r = 0
            for p in self.p_deltas:
                if p[0] <= d <= p[1]:
                    p_d += 1
            for r in self.p_ranges:
                if r[0] <= to_check <= r[1]:
                    p_r += 1
            p = p_d * p_r
            if p > max_seen[0][0]:
                max_seen = [(p, to_check)]
            elif p == max_seen[0][0]:
                max_seen.append((p, to_check))
        return np.float(np.mean([m[1] for m in max_seen]))


class Bachelier1900(Predictor):
    """
    This predictor is based on the paper *Théorie de la Spéculation* by Louis Bachelier [Bachelier1900_], now widely
    regarded as the first academic attempt at predicting stock market prices through mathematical analysis. His formulae
    are significantly more complex than the implementation presented here, as he attempted to take into account the
    *spread*, as well as predict multiple epochs ahead and how many epochs there might be before a price was expected to
    eventuate.

    Given

    .. math::

        x_t, x_{t+1}:\\ x \\in \\mathbb{R}

    and

    .. math::

        \\begin{equation}
        \\Delta x = x_{t+1} - x_t
        \\end{equation}

    generate two probabilities:

    .. math::

        P(x_t), P(\\delta x)

    From these, we can generate

    .. math::

        \\begin{equation}
        P(x_{t+2}) = P(x_{t+2}) \\times P(x_{t+2} - x_{t+1})
        \\end{equation}

    Maximise for predicted price.

    .. [Bachelier1900]:
        Bachelier, L. "Théorie de la Spéculation"
        *Annales scientifiques de l'École Normale Supérieure*, Sér 3, 17 (1900) p 21-86.
        Translated by D. May, 2011.

    """

    def __init__(
            self,
            lock: mp.Lock,
            args: Optional[str] = None,
            debug: Optional[bool] = False
    ) -> None:
        super().__init__(lock, args, debug)

        # 0. Arguments
        # ap = ArgumentParser()
        # ap.add_argument('--tp_ratio', type=float, default=1.0)
        # ap.add_argument('--sl_ratio', type=float, default=defaults.DEFAULT_SL_RATIO)
        # ap.add_argument('--sl_min', type=float, default=defaults.DEFAULT_SL_MIN)
        # self.parameters = ap.parse_args(self.parameters.split() if self.parameters is not None else [])
        #
        # # 1. Ratio overrides
        # self._tp_ratio = self.parameters.tp_ratio
        # self._sl_ratio = self.parameters.sl_ratio
        # self._sl_min = self.parameters.sl_min
        # self.per_symbol = {}

    def __enter__(self) -> Predictor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        pass
        # for b in bars:
        #     self.per_symbol[b.symbol_id] = PerSymbol(b.low, b.high, b.open)

    def on_bar(self, bars: Iterable[Bar]) -> None:

        orders = []
        # for b in bars:
        #     self.per_symbol[b.symbol_id].add_epoch(b.low, b.high, b.open)
        #     prediction = self.per_symbol[b.symbol_id].get_highest_probability(b.close)
        #
        #     up = prediction - b.close
        #     down = b.close - prediction
        #     buy_tp = b.close + up * self._tp_ratio
        #     buy_sl = b.close - up * self._sl_ratio
        #     sell_tp = b.close - down * self._tp_ratio
        #     sell_sl = b.close + down * self._sl_ratio
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
