#   hokohoko/predictors/_YaoTan2000.py
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
#   This is an implementation of Yao and Tan's predictor.
#   TODO: Continue description, make work, etc.
#

from argparse import ArgumentParser
from ast import literal_eval
from collections import deque
from typing import Iterable, Optional
from random import Random

import multiprocessing as mp
import numpy as np
from scipy.ndimage.interpolation import shift

from hokohoko.entities import Predictor, Bar, Order, Direction


class Network:
    """
    This class is derived from Nielsen, M. Neural Networks and Deep Learning, 2015.
    """
    def __init__(self, iho, rand):
        self.layers = len(iho)
        self.iho = iho
        self.rand = rand
        self.biases = [np.array([[self.rand.gauss(0, 1)] for j in range(i)]) for i in iho[1:]]
        self.weights = [
            np.array([[self.rand.gauss(0, 1) for j in range(x)] for i in range(y)])
            for x, y in zip(iho[:-1], iho[1:])
        ]

    def feed_forward(self, input_):
        """
        Calculate the output, given an input input_
        :param input_:
        :return:
        """
        for b, w in zip(self.biases, self.weights):
            input_ = Network.ff_algorithm(np.dot(w, input_) + b)
        return input_

    def grad_descent(self, training_data, limit, alpha, tolerance, test_data=None):
        last = 0
        errs = np.ones(25)
        for j in range(limit):
            errs = np.roll(errs, 1)
            errs[0] = self.update(training_data, alpha)
            if np.std(errs) < tolerance:
                # print(f"({errs[0]:12.5f})", end="\t")
                break

        if test_data:
            t = self.evaluate(test_data)
            if t != last:
                # print("Epoch {0}: {1} / {2}".format(j, t, len(test_data)), end="\t")
                last = t

    def update(self, batch, alpha):
        """
        This updates the weight's and biases using back-propagation.
        :param batch: The training data.
        :param alpha: The learning rate.
        :return:
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        a_err = 0
        for x, y in batch:
            delta_nabla_b, delta_nabla_w, err = self.back_propagate(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            a_err += err * err
        self.weights = [w - (alpha / len(batch)) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (alpha / len(batch)) * nb for b, nb in zip(self.biases, nabla_b)]
        return np.sqrt(a_err) / len(batch)

    def back_propagate(self, x, y):
        """
        Returns the gradient of the cost function.
        :param x:
        :param y:
        :return:
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # Feedforward
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = Network.ff_algorithm(z)
            activations.append(activation)

        # Backwards
        delta = activations[-1] - y * Network.ff_derivative(zs[-1])
        ret = abs(delta)
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for r in range(2, self.layers):
            z = zs[-r]
            d = Network.ff_derivative(z)
            delta = np.dot(self.weights[-r + 1].transpose(), delta) * d
            nabla_b[-r] = delta
            nabla_w[-r] = np.dot(delta, activations[-r - 1].transpose())

        return nabla_b, nabla_w, ret

    def evaluate(self, test_data):
        test_results = [self.feed_forward(x) * y for (x, y) in test_data]
        return sum(int(x > 0) for x in test_results)

    @staticmethod
    def ff_algorithm(z):
        return np.tanh(z)

    @staticmethod
    def ff_derivative(z):
        return 1 - np.tanh(z) ** 2


class YaoTan2000(Predictor):
    """
    This is an implementation of Yao & Tan's best performing predictor (6-3-1).

    Yao & Tan used a 6-3-1 network with MAs of 5, 10, 20, 60, 120 weeks, plus current value as inputs.
    They used a 70-20-10 training-validation-test split. In this application, we don't need that, so we'll use a 75-25
    training-validation split.
    They appraised with NMSE, S_stat and D_stat (Page 85).
    Input: Normalised exchange rate differences of previous 6 Bars. ()
    They used Strategy 1 (Page 87; Footnote 2, page 89).
    No information was provided as to the FF/BP algorithms. Output was centered around 0, however (p87), so we'll use
    tanh:

    FF: (e^x - e^-x)/(e^x + e^-x)
    BP: 1 - FF(x)^2
    """
    def __init__(self, lock: mp.Lock, parameters: Optional[str] = None, debug: Optional[bool] = False) -> None:
        super().__init__(lock, parameters, debug)

        # 0. Arguments
        ap = ArgumentParser()
        ap.add_argument('-a', '--learning_rate', type=float, default=0.5)
        ap.add_argument('-l', '--limit', type=int, default=1000)
        ap.add_argument('-t', '--tolerance', type=float, default=0.00001)     # 0.1 pips

        self.parameters = ap.parse_args(self.parameters.split() if self.parameters is not None else [])
        self._alpha = self.parameters.learning_rate
        self._limit = self.parameters.limit
        self._tolerance = self.parameters.tolerance

        # 1. Structures
        self._mas = [1, 5, 10, 20, 60, 120]
        self.last_averages = {}
        self.histories = {}
        self.anns = {}
        self.last_predictions = {}

    def __enter__(self) -> Predictor:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        for b in bars:
            self.last_averages[b.symbol_id] = b.close
            self.histories[b.symbol_id] = np.array([0])
            self.anns[b.symbol_id] = Network([6, 3, 1], self)
            self.last_predictions[b.symbol_id] = 0

    def on_bar(self, bars: Iterable[Bar]) -> None:
        orders = []
        for b in bars:

            # 0. Update history. These are first-order differences of the average value for the Bar.
            average = (b.open + b.high + b.low + b.close) / 4
            average_diff = np.array([average - self.last_averages[b.symbol_id]])
            self.histories[b.symbol_id] = np.concatenate([average_diff, self.histories[b.symbol_id]])
            self.last_averages[b.symbol_id] = average

            # Requires a minimum of 129 values to work (7:2 training:validation ratio)
            if len(self.histories[b.symbol_id]) < 129:
                continue

            # 1. Normalise history into [-1,1].
            norm = self.histories[b.symbol_id] / np.max(np.abs(self.histories[b.symbol_id]))

            # 2. Get inputs - 5 moving averages plus the current value.
            data = []
            for i in range(len(norm) - 120):
                d = np.array([[0]] * 6, dtype=np.float64)
                for j in range(len(self._mas)):
                    d[j][0] = np.average(norm[1 + i:self._mas[j] + 1 + i])
                data.append((d, norm[i]))

            # 3. Send into NN.
            split = int(len(data) * 2 / 9)
            self.anns[b.symbol_id].grad_descent(data[:-split], self._limit, self._alpha, self._tolerance, data[-split:])

            # 4. Make prediction. (Apply Strategy 1).
            req = np.array([[0]] * 6, dtype=np.float64)
            for j in range(len(self._mas)):
                req[j][0] = np.average(norm[:self._mas[j]])
            pred = (self.anns[b.symbol_id].feed_forward(req) * np.max(np.abs(self.histories[b.symbol_id])) + average)[0][0]
            if pred > self.last_predictions[b.symbol_id] and pred > b.close:
            # if pred > b.close:
                # print("BUY")
                orders.append(Order(b.symbol_id, Direction.BUY, None, pred, None))
            elif pred < self.last_predictions[b.symbol_id] and pred < b.close:
            # elif pred < b.close:
                orders.append(Order(b.symbol_id, Direction.SELL, None, pred, None))
                # print("SELL")
            else:
                # print("DONT")
                pred = 0
            self.last_predictions[b.symbol_id] = pred

        self.place_orders(orders)

