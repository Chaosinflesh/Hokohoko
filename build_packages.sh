#   build_upload_packages.sh
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
#   This script builds the packages for PyPI.
#

python Hokohoko/setup.py bdist_wheel
python Assessors/setup.py bdist_wheel
python Predictors/setup.py bdist_wheel
