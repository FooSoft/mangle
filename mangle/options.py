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


#from PyQt4 import QtGui, uic
from PyQt5 import QtGui, uic, QtWidgets

from .image import ImageFlags
from . import util


class DialogOptions(QtWidgets.QDialog):
    def __init__(self, parent, book):
        QtWidgets.QDialog.__init__(self, parent)

        uic.loadUi(util.buildResPath('mangle/ui/options.ui'), self)
        self.accepted.connect(self.onAccept)

        self.book = book
        self.moveOptionsToDialog()


    def onAccept(self):
        self.moveDialogToOptions()


    # Get options from current book (like a loaded one) and set the dialog values
    def moveOptionsToDialog(self):
        self.lineEditTitle.setText(self.book.title or 'Untitled')
        self.comboBoxDevice.setCurrentIndex(max(self.comboBoxDevice.findText(self.book.device), 0))
        self.comboBoxFormat.setCurrentIndex(max(self.comboBoxFormat.findText(self.book.outputFormat), 0))
        self.checkboxOverwrite.setChecked(self.book.overwrite)
        self.checkboxOrient.setChecked(self.book.imageFlags & ImageFlags.Orient)
        self.checkboxResize.setChecked(self.book.imageFlags & ImageFlags.Resize)
        self.checkboxStretch.setChecked(self.book.imageFlags & ImageFlags.Stretch)
        self.checkboxQuantize.setChecked(self.book.imageFlags & ImageFlags.Quantize)
        self.checkboxFrame.setChecked(self.book.imageFlags & ImageFlags.Frame)


    # Save parameters set on the dialogs to the book object if need
    def moveDialogToOptions(self):
        # First get dialog values
        title        = self.lineEditTitle.text()
        device       = self.comboBoxDevice.currentText()
        outputFormat = self.comboBoxFormat.currentText()
        overwrite    = self.checkboxOverwrite.isChecked()

        # Now compute flags
        imageFlags = 0
        if self.checkboxOrient.isChecked():
            imageFlags |= ImageFlags.Orient
        if self.checkboxResize.isChecked():
            imageFlags |= ImageFlags.Resize
        if self.checkboxStretch.isChecked():
            imageFlags |= ImageFlags.Stretch
        if self.checkboxQuantize.isChecked():
            imageFlags |= ImageFlags.Quantize
        if self.checkboxFrame.isChecked():
            imageFlags |= ImageFlags.Frame
        if self.checkboxSplit.isChecked():
            imageFlags |= ImageFlags.SplitRightLeft
        if self.checkboxSplitInverse.isChecked():
            imageFlags |= ImageFlags.SplitLeftRight
        if self.checkboxAutoCrop.isChecked():
            imageFlags |= ImageFlags.AutoCrop

        # If we did modified a value, update the book
        # and only if we did change something to not
        # warn for nothing the user
        modified = (
            self.book.title != title or
            self.book.device != device or
            self.book.overwrite != overwrite or
            self.book.imageFlags != imageFlags or
            self.book.outputFormat != outputFormat
        )

        if modified:
            self.book.modified     = True
            self.book.title        = title
            self.book.device       = device
            self.book.overwrite    = overwrite
            self.book.imageFlags   = imageFlags
            self.book.outputFormat = outputFormat
