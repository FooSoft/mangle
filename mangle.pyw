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

## TODO # Port to Python3, PyQt5 # TODO ##
# X run 2to3
# X change imports to PyQt5 and update PyQt method calls 
# X test main functionality:
#	X build comic with images and generate all formats for at least 2 types of Kindle
#	X test load/save .mngl files and other menu bar buttons.
# - remove unused imports
# - remove print/ debug
# - test all functions

import sys

from PyQt5 import QtGui, QtCore, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *

from mangle.book import MainWindowBook

application = QtWidgets.QApplication(sys.argv)
filename = sys.argv[1] if len(sys.argv) > 1 else None
window = MainWindowBook(filename)
window.show()
application.exec_()
