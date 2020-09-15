#   assessors/setup.py
#
#   Copyright 2020 Neil Bradley, Bebecom NZ Limited
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
#   This script contains the setup parameters for the
#	hokohoko_assessors package.
#

import datetime
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

with open("VERSION", "r") as fv:
	version = fv.read().strip() + f"_{int(datetime.datetime.utcnow().timestamp())}"

setuptools.setup(
	name="hokohoko_assessors",
	version=version,
	author="Neil Bradley",
	author_email="neil.bradley@bebecom.co.nz",
	description="Provides a selection of Assessors for the Hokohoko library.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/nc-bradley/Hokohoko",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved ::  GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.7",
	install_requires=['numpy', 'scipy', 'hokohoko']
)
