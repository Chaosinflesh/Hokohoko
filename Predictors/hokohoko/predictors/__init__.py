#   hokohoko/predictors/__init__.py
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
#   This file maps the predictors to hokohoko.predictors.
#

from hokohoko.standard import DoNothing
from hokohoko.predictors._Bachelier1900 import Bachelier1900
from hokohoko.predictors._Bollerslev1986 import Bollerslev1986
from hokohoko.predictors._Bollinger import Bollinger
from hokohoko.predictors._BoxJenkins1970 import BoxJenkins1970
from hokohoko.predictors._BoxJenkins1976 import BoxJenkins1976
from hokohoko.predictors._Engel1982 import Engel1982
from hokohoko.predictors._Random import Random
from hokohoko.predictors._RandomWalk import RandomWalk
from hokohoko.predictors._Static import Static
from hokohoko.predictors._YaoTan2000 import YaoTan2000
from hokohoko.predictors._Yule1927 import Yule1927

__all__ = [
    "Bachelier1900",
    "Bollerslev1986",
    "Bollinger",
    "BoxJenkins1970",
    "BoxJenkins1976",
    "DoNothing",
    "Engel1982",
    "Random",
    "RandomWalk",
    "Static",
    "YaoTan2000",
    "Yule1927"
]
