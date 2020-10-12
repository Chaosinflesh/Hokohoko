#   assessors/__init__.py
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
#   This file maps the assessors to hokohoko.assessors.
#

from hokohoko.standard import Logger
from hokohoko.assessors._AccountHistory import AccountHistory
from hokohoko.assessors._SpeculativeAccuracy import SpeculativeAccuracy

__all__ = [
    "AccountHistory",
    "Logger",
    "SpeculativeAccuracy"
]
