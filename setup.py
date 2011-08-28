#!/usr/bin/env python

# Copyright (C) 2010  Alex Yatskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from distutils.core import setup
import py2exe


sys.argv.append('py2exe')
setup(
    windows=[{'script': 'mangle.pyw'}],
    options={'py2exe': {'bundle_files': 1, 'includes': ['sip']}},
    zipfile=None
)
