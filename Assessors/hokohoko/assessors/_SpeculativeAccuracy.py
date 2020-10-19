#   assessors/_Accuracy.py
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
#   This file contains the definition of the Accuracy Assessor, as
#   defined in Bradley, Mayo and Patros (2020).
#

"""
===================
SpeculativeAccuracy
===================
"""
from argparse import ArgumentParser
from typing import Iterable, List, NamedTuple, Union, Optional

import numpy as np
from scipy.stats import kurtosis, skew

from hokohoko import utils
from hokohoko.entities import Assessor, Direction, Position, Status


class _CalculatedAccuracy(NamedTuple):
    history: Position
    max_profit: Union[float, np.float32]
    max_loss: Union[float, np.float32]
    actual_profit: Union[float, np.float32]
    performance: Union[float, np.float64]


class SpeculativeAccuracy(Assessor):
    """
    Historically, researchers in foreign exchange prediction have shunned the use of an absolute
    measure (such as maximum profit possible per trade). Hokohoko aims to change that, with the
    introduction of a new metric, *Speculative Accuracy*. This measures how close to maximum profit
    a position makes from the ``OPEN`` price, whilst making allowance for trades for which profit
    was impossible.

    The logic behind this metric is that, for any given future period of time, the conditions of a
    taken Position may be met, and thus the Position/prediction is correct. However, it is only
    maximally correct if its ``take_profit`` matches the observed ``HIGH``/``LOW`` (depending on
    trade **Direction**), and thus anything otherwise is only partially correct. We also need to
    take into account the times where a Position cannot be profitable, and other times when there
    is no movement in the market.

    Therefore, given a Position with

    .. math::

        \\begin{equation}
        result=\\lbrace
        max\\_profit \\in \\mathbb{R}_{\\geq 0},
        max\\_loss \\in \\mathbb{R}_{\\leq 0},
        actual\\_profit \\in \\mathbb{R},
        taken \\in \\lbrace 0, 1 \\rbrace \\rbrace\\ \\ \\ \\ (1)
        \\end{equation}

    we define thus

    .. math::

        \\begin{equation}
        accuracy(result) = \\left\\{
        \\begin{array}{@{}rl@{}}
        \\frac{actual\\_profit}{max\\_profit}, & \\text{if}\\ max\\_profit \\gt 0 \\\\
        1.0, & \\text{if}\\ max\\_profit = 0 \\land taken = 0\\ \\ \\ \\ (2) \\\\
        \\frac{-actual\\_profit}{max\\_loss}, & \\text{if}\\ max\\_loss \\lt 0 \\\\
        0.0, & \\text{otherwise}
        \\end{array}\\right.
        \\end{equation}

    The astute observer will note that these equations are:

    1. Unbounded to the negative---incorrect predictions are heavily penalised.
    2. Highly optimistic---making a loss for a potential 1 pip profit is very heavily penalised.
    3. Heavily skewed for correct ``DONT_BUY``, ``DONT_SELL``.
    4. Not the absolute profit possible, allowing possible results > 100%.

    To these, the author notes:

    1. Accepted, no apologies. Make better predictions.
    2. Accepted, still no apologies. As above.
    3. Within the default dataset provided, ``¬taken`` will only be correct about two percent of
       the time. The heavy skew is considered acceptable in this scenario (and is logically true).
    4. If a predictor can more accurately predict the dips and rises that allow for profits greater
       than from ``OPEN`` to ``HIGH``/``LOW``, it deserves the score it gets. Accepted.

    This Assessor takes the following options:

    .. code-block:: Text

        --show_results
                        Prints out the list of all given results, which may be piped into a file for
                        further processing.


    """

    def __init__(self, parameters):
        """
        :param parameters:  The ``assessor_parameters`` provided via HokohokoConfig.
        :type parameters:   str

        """
        super().__init__(parameters)

        # 0. Arguments
        ap = ArgumentParser()
        ap.add_argument('--show-results', type=bool, default=False)
        self.parameters = ap.parse_args(self.parameters.split() if self.parameters is not None else [])

        # 2. Stop-loss ratio
        self._show_results = self.parameters.show_results

    def analyse(self, period_results: Iterable) -> None:
        """
        This is the routine that is called by Hokohoko after initialization. It calculates and collates the provided
        account data into an overview table.

        :param period_results:    The accounts from benchmarking.
        :type period_results:     Iterable[multiprocessing.pool.AsyncResult[hokohoko.entities.Account]]

        """

        periodic = {}
        symbolic = {}

        for pr in period_results:
            period, account = pr.get()
            periodic[period] = []
            maxes = {}
            for symbol in account.symbol_ids:
                if symbol not in symbolic:
                    symbolic[symbol] = []
                maxes[symbol] = 0

            if self._show_results:
                print()
                print(
                    "{:>4}\t{:8}\t{:8}\t{:10}\t{:>12}\t{:16}\t{:>12}\t{:>12}\t{:>12}\t{:>12}\t{:>12}\t{:>12}"
                    "\t{:>12}".format(
                        "Period",
                        "Order ID",
                        "Symbol",
                        "Trade Type",
                        "Order Time",
                        "Result",
                        "Open Time",
                        "Close Time",
                        "Profit",
                        "Max Profit",
                        "Max Loss",
                        "Accuracy %",
                        "Real Profit"
                    )
                )
                print("-" * 160)

            for h_id, history in account.history.items():
                max_profit, max_loss, actual_profit = Accuracy.calculate_rate_changes(history)
                maxes[history.order.symbol_id] = max(maxes[history.order.symbol_id], max_profit)
                perf = Accuracy.calculate_accuracy(max_profit, max_loss, actual_profit, history.status)

                # Collate stats.
                periodic[period].append(_CalculatedAccuracy(history, max_profit, max_loss, actual_profit, perf))

                if self._show_results:
                    print(str.format(
                        "{:>4}\t{:8}\t{:8}\t{:10}\t{:12.0f}\t{:16}\t{:12.0f}\t{:12.0f}\t{:12.5f}\t{:12.5f}\t{:12.5f}"
                        "\t{:12.5f}\t{:12.5f}",
                        period,
                        h_id,
                        utils.convert_id_to_symbol(history.order.symbol_id),
                        history.order.direction.name,
                        history.future.start,
                        history.status.name,
                        history.open_time,
                        history.close_time,
                        actual_profit,
                        max_profit,
                        max_loss,
                        perf,
                        history.final_value - history.initial_value
                    ))

            # Normalise results, and collate into per_symbol.
            for i in range(len(periodic[period])):
                ca = periodic[period][i]
                m_profit = ca.max_profit
                t_perf = ca.performance
                symbol = ca.history.order.symbol_id
                if m_profit > 0:
                    t_perf = ca.performance * m_profit / maxes[symbol]
                    periodic[period][i] = _CalculatedAccuracy(ca.history, ca.max_profit, ca.max_loss, ca.actual_profit, t_perf)
                symbolic[symbol].append(periodic[period][i])

        combined = []
        Accuracy._output_header("Symbolic Results:")
        for key, part in symbolic.items():
            Accuracy._output_collated(part, f"{utils.convert_id_to_symbol(key)}")
        Accuracy._output_tail()
        Accuracy._output_header("Period Results")
        for key, part in periodic.items():
            combined.append(Accuracy._output_collated(part, f"{key:03d}"))
        Accuracy._output_tail()

        Accuracy._output_total(combined, "Overall Results:")

    @staticmethod
    def _output_total(combined: list, name: str):
        print(f"\n\x1b[7m{name:90}\x1b[0m")
        print(f"{'':20}{'Mean':>10}{'StdDev':>16}{'Skew':>16}{'Kurtosis':>16}{'Count':>12}")
        print("-" * 90)
        print(f"{'Periodic Overall:':20}", end="")

        # Mean
        if len(combined) > 0:
            mean = np.mean(combined)
        else:
            mean = 0.0
        print(f"{mean:10.5f}", end="")

        # StdDev
        if len(combined) > 1:
            print(f"{np.std(combined):16.5f}", end="")
        else:
            print(f"{'':16}", end="")

        # Skew
        if len(combined) > 2:
            print(f"{skew(np.array(combined)):16.5f}", end="")
        else:
            print(f"{'':16}", end="")

        # Kurtosis
        if len(combined) > 2:
            print(f"{kurtosis(combined):16.5f}", end="")
        else:
            print(f"{'':16}", end="")

        # Count
        print(f"{len(combined):12d}")

    @staticmethod
    def _output_header(name) -> None:
        title = f"Overall ({name})"

        # len(Status) = 7, so 84 for all statuses.
        print(f"|{'-' * 68}|{'-' * 24}|{'-' * 84}|{'-' * 96}|{'-' * 96}|")
        print(f"|{title:^68}|{'Profit':^24}|{'ALL':^84}|{'BUY':^96}|{'SELL':^96}|")
        print(
            f"|{name[:6]:20}{'Mean':>12}{'StdDev':>12}{'Skew':>12}{'Kurtosis':>12}"
            f"|{'Possible':>12}{'Impossible':>12}|", end=""
        )
        for status in Status:
            print(f"{status.name.replace('CLOSED_', ''):>12}", end="")
        print(f"|{'All':>12}", end="")
        for status in Status:
            print(f"{status.name.replace('CLOSED_', ''):>12}", end="")
        print(f"|{'All':>12}", end="")
        for status in Status:
            print(f"{status.name.replace('CLOSED_', ''):>12}", end="")
        print(f"|\n|{'-' * 68}|{'-' * 24}|{'-' * 84}|{'-' * 96}|{'-' * 96}|")

    @staticmethod
    def _output_tail() -> None:
        print(f"|{'-' * 68}|{'-' * 24}|{'-' * 84}|{'-' * 96}|{'-' * 96}|\n")

    @staticmethod
    def _output_collated(collated, name) -> float:
        print(f"|{name:20}", end='')

        # Overall
        mean = np.float64(np.mean([c.performance for c in collated]))
        print(f"{mean:12.5f}", end='')
        print(f"{np.std([c.performance for c in collated]) if len(collated) > 1 else 0.0:12.5f}", end='')
        print(f"{skew(np.array([c.performance for c in collated])) if len(collated) > 1 else 0.0:12.5f}", end='')
        print(f"{kurtosis([c.performance for c in collated]) if len(collated) > 1 else 0.0:12.5f}|", end='')

        # Profit
        Accuracy._output_mean([c.performance for c in collated if c.max_profit > 0])
        Accuracy._output_mean([c.performance for c in collated if c.max_profit <= 0])

        # ALL
        print("|", end="")
        for status in Status:
            Accuracy._output_mean([c.performance for c in collated if c.history.status == status])

        # BUY
        print("|", end="")
        buy = [c for c in collated if c.history.order.direction in (Direction.BUY, Direction.DONT_BUY)]
        Accuracy._output_mean([b.performance for b in buy])
        for status in Status:
            Accuracy._output_mean([b.performance for b in buy if b.history.status == status])

        # SELL
        print("|", end="")
        sell = [c for c in collated if c.history.order.direction in (Direction.SELL, Direction.DONT_SELL)]
        Accuracy._output_mean([s.performance for s in sell])
        for status in Status:
            Accuracy._output_mean([s.performance for s in sell if s.history.status == status])
        print("|")

        return mean

    @staticmethod
    def _output_mean(data: List[Union[float, np.float64]]):
        """
        Output a single stat or blank if appropriate.

        :param data:    The data to average.
        :type data:     list[np.float64]

        """
        print(f"{np.mean(data):12.5f}" if len(data) > 0 else " " * 12, end="")

    @staticmethod
    @utils.generate_tests("""
        raises an error if result is None
        raises an error if results is not a Result
        returns a tuple of three floats
        calculates values correctly for all directions
    """)
    def calculate_rate_changes(history: Position) -> (np.float64, np.float64, np.float64):
        """
        Calculates the maximum profit, maximum loss, and actual profit (in pips) for a given Result.

        :param history: The Position History to analyse.
        :type history:  hokohoko.entities.Position

        :return:        A tuple of the order: max_profit, max_loss, actual_profit.
                        actual_profit may be negative (and therefore a loss).
        :rtype:         tuple<numpy.float64, numpy.float64, numpy.float64>

        """

        # 1. Calculate maximum profit, maximum loss based on the position's direction.
        if history.order.direction in (Direction.BUY, Direction.DONT_BUY):
            max_profit = history.future.high - history.future.open
            max_loss = history.future.low - history.future.open
        else:
            max_profit = history.future.open - history.future.low
            max_loss = history.future.open - history.future.high

        # 2. Calculate actual profit/loss made:
        actual_profit = 0
        if history.open_rate is not None:
            t_open = history.open_rate
        else:
            t_open = history.order.open_bid if history.order.open_bid is not None else history.future.open

        if history.close_rate is not None:
            t_close = history.close_rate
        elif history.status == Status.OPEN:
            t_close = history.future.close
        else:
            t_close = t_open    # Set to 0 if pending.

        if history.order.direction == Direction.BUY:
            actual_profit = t_close - t_open
        elif history.order.direction == Direction.SELL:
            actual_profit = t_open - t_close
        else:
            actual_profit = 0.0

        return max_profit, max_loss, actual_profit

    @staticmethod
    @utils.generate_tests("""
        # based on the Accuracy specification:
        returns the correct accuracy for profit and profitable
        returns the correct accuracy for not taken and profitable
        returns the correct accuracy for loss and profitable
        returns the correct accuracy for loss and unprofitable
        returns the correct accuracy for not taken and unprofitable
        returns the correct accuracy for taken and no movement
        returns the correct accuracy for not taken and no movement
    """)
    def calculate_accuracy(
            max_profit: Union[float, np.float32],
            max_loss: Union[float, np.float32],
            actual_profit: Union[float, np.float32],
            status: Status,
            mode: Optional[int] = 0,
            weight: Optional[Union[float, np.float32]] = 1
    ) -> np.float64:
        """
        Calculates the accuracy measure for the given parameters.

        :param max_profit:      The maximum profit possible (``OPEN`` to ``HIGH``/``LOW`` for ``BUY``, ``SELL``
                                respectively), in pips.
        :type max_profit:       float

        :param max_loss:        The maximum loss possible (``OPEN`` to ``LOW``/``HIGH`` for ``BUY``, ``SELL``
                                respectively), in pips.
        :type max_loss:         float

        :param actual_profit:   The actual profit/loss made, in pips.
        :type actual_profit:    float

        :param status:          The status of the result. Used to check if an order was requested or not.
        :type status:           hokohoko.entities.Status

        :param mode:            The type of Speculative Performance metric to use:
                                0 - Basic SP.
                                1 - Taking a Position without Profit-potential = -1
                                2 - Normalises via symlog_10
                                3 - Normalises via symlog_e
                                4 - Normalises via tanh
                                5 - Normalises with the provided weight.
        :type mode:             int

        :param weight:          A weigting to normalise the score with.
        :type weight:           float

        :return:                Returns an accuracy score. See Bradley *et al* for the historical background
                                for this measure.
        :rtype:                 float

        """
        perf = 0.0
        if max_profit > 0:
            perf = actual_profit / max_profit

            if mode == 2:
                if perf > 1:
                    perf = np.log10(perf) + 1
                elif perf < -1:
                    perf = -np.log10(-perf) - 1
            elif mode == 3:
                if perf > 1:
                    perf = np.log(perf) + 1
                elif perf < -1:
                    perf = -np.log(-perf) - 1
            elif mode == 4:
                perf = np.tanh(perf) / np.tanh(1)
            elif mode == 5:
                perf *= max_profit / weight
        else:
            if status == Status.NOT_TAKEN:
                perf = 1
            elif mode == 1:
                perf = -1
            elif max_loss < 0:
                perf = -actual_profit / max_loss


        return perf
