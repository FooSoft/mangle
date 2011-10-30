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

import os, shutil

from PyQt4 import QtGui, QtCore

import image
import cbz


class DialogConvert(QtGui.QProgressDialog):
    def __init__(self, parent, book, directory):
        QtGui.QProgressDialog.__init__(self)

        self.book = book
        self.directory = directory

        self.timer = None
        self.setWindowTitle('Exporting book...')
        self.setMaximum(len(self.book.images))
        self.setValue(0)

        self.archive = None
        if 'cbz' in self.book.outputFormat:
            # TODO: switch to API 2, to get rid of the unicode conversions
            self.archive = cbz.Archive(
                    os.path.join(unicode(self.directory), unicode(self.book.title)))


    def showEvent(self, event):
        if self.timer is None:
            self.timer = QtCore.QTimer()
            self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.onTimer)
            self.timer.start(0)


    def hideEvent(self, event):
        """Called when the dialog finishes processing."""
        # close the archive if we created a CBZ file
        if self.archive is not None:
            self.archive.close()
        # remove image directory if the user didn't wish for images
        if 'image' not in self.book.outputFormat:
            path = os.path.join(unicode(self.directory), unicode(self.book.title))
            shutil.rmtree(path)

    def onTimer(self):
        index = self.value()
        directory = os.path.join(unicode(self.directory), unicode(self.book.title))
        target = os.path.join(directory, '%05d.png' % index)
        source = unicode(self.book.images[index])

        if index == 0:
            try:
                if not os.path.isdir(directory):
                    os.makedirs(directory)
            except OSError:
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot create directory %s' % directory)
                self.close()
                return

            try:
                base = os.path.join(directory, unicode(self.book.title))

                mangaName = base + '.manga'
                if self.book.overwrite or not os.path.isfile(mangaName):
                    manga = open(mangaName, 'w')
                    manga.write('\x00')
                    manga.close()

                mangaSaveName = base + '.manga_save'
                if self.book.overwrite or not os.path.isfile(mangaSaveName):
                    mangaSave = open(base + '.manga_save', 'w')
                    saveData = u'LAST=/mnt/us/pictures/%s/%s' % (self.book.title, os.path.split(target)[1])
                    mangaSave.write(saveData.encode('utf-8'))
                    mangaSave.close()

            except IOError:
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot write manga file(s) to directory %s' % directory)
                self.close()
                return False

        self.setLabelText('Processing %s...' % os.path.split(source)[1])

        try:
            if self.book.overwrite or not os.path.isfile(target):
                image.convertImage(source, target, str(self.book.device), self.book.imageFlags)
                if self.archive is not None:
                    self.archive.addFile(target)
        except RuntimeError, error:
            result = QtGui.QMessageBox.critical(
                self,
                'Mangle',
                str(error),
                QtGui.QMessageBox.Abort | QtGui.QMessageBox.Ignore,
                QtGui.QMessageBox.Ignore
            )
            if result == QtGui.QMessageBox.Abort:
                self.close()
                return

        self.setValue(index + 1)
