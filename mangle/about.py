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


import os.path

from PyQt4 import QtGui, uic

import resources

class DialogAbout(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        ui = uic.loadUi(os.path.join(resources.get_ui_path(), 'about.ui'), self)
        label = ui.findChild(QtGui.QLabel, 'label')
        label.setPixmap(QtGui.QPixmap(os.path.join(resources.get_image_path(), 'banner_about.png')))
