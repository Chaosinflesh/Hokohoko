#   hokohoko/predictors/_Engel1982.py
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
#   This is a predictor using an implementation of Engel's ARCH model,
#   as propose in [TODO].
#   TODO: Continue description, make work, etc.
#

from typing import Iterable

from hokohoko.entities import Predictor, Bar


class Engel1982(Predictor):
    def __enter__(self) -> Predictor:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def on_start(self, bars: Iterable[Bar]) -> None:
        pass

    def on_bar(self, bars: Iterable[Bar]) -> None:
        pass
