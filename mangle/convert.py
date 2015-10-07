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


import os
import shutil
from PyQt4 import QtGui, QtCore


from image import ImageFlags
import cbz
import image
import pdfimage


class DialogConvert(QtGui.QProgressDialog):
    def __init__(self, parent, book, directory):
        QtGui.QProgressDialog.__init__(self)

        self.book     = book
        self.bookPath = os.path.join(unicode(directory), unicode(self.book.title))

        self.timer = None
        self.setWindowTitle('Exporting book...')
        self.setMaximum(len(self.book.images))
        self.setValue(0)

        self.archive = None
        if 'CBZ' in self.book.outputFormat:
            self.archive = cbz.Archive(self.bookPath)
        
        self.pdf = None
        if "PDF" in self.book.outputFormat:
            self.pdf = pdfimage.PDFImage(self.bookPath, str(self.book.title), str(self.book.device))



    def showEvent(self, event):
        if self.timer is None:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.onTimer)
            self.timer.start(0)


    def hideEvent(self, event):
        """Called when the dialog finishes processing."""

        # Close the archive if we created a CBZ file
        if self.archive is not None:
            self.archive.close()
        # Close and generate the PDF File
        if self.pdf is not None:
            self.pdf.close()

        # Remove image directory if the user didn't wish for images
        if 'Image' not in self.book.outputFormat:
            shutil.rmtree(self.bookPath)


    def convertAndSave(self, source, target, device, flags, archive, pdf):
        image.convertImage(source, target, device, flags)
        if archive is not None:
            archive.addFile(target)
        if pdf is not None:
            pdf.addImage(target)

                
    def onTimer(self):
        index = self.value()
        target = os.path.join(self.bookPath, '%05d.png' % index)
        source = unicode(self.book.images[index])

        if index == 0:
            try:
                if not os.path.isdir(self.bookPath):
                    os.makedirs(self.bookPath)
            except OSError:
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot create directory %s' % self.bookPath)
                self.close()
                return

            try:
                base = os.path.join(self.bookPath, unicode(self.book.title))

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
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot write manga file(s) to directory %s' % self.bookPath)
                self.close()
                return False

        self.setLabelText('Processing %s...' % os.path.split(source)[1])

        try:
            if self.book.overwrite or not os.path.isfile(target):
                device = str(self.book.device)
                flags = self.book.imageFlags
                archive = self.archive
                pdf = self.pdf

                # Maybe the user ask for a split, but the picture is not a large one, so skip
                # it but only for this picture
                if (flags & ImageFlags.Split) or (flags & ImageFlags.SplitInverse):
                    if not image.isSplitable(source):
                        # remove split flags
                        splitFlags= [ImageFlags.Split, ImageFlags.SplitInverse, ImageFlags.SplitRight, ImageFlags.SplitLeft]
                        for f in splitFlags:
                            flags &= ~f

                # For right page (if requested in options and need for this image)
                if (flags & ImageFlags.Split):
                    # New path based on modified index
                    target = os.path.join(self.bookPath, '%05d.png' % (index * 2 + 0))
                    self.convertAndSave(source, target, device, flags ^ ImageFlags.Split | ImageFlags.SplitRight, archive, pdf)
                    # Change target once again for left page
                    target = os.path.join(self.bookPath, '%05d.png' % (index * 2 + 1))

                # For right page (if requested), but in inverted mode
                if (flags & ImageFlags.SplitInverse):
                    # New path based on modified index
                    target = os.path.join(self.bookPath, '%05d.png' % (index * 2 + 0))
                    self.convertAndSave(source, target, device, flags ^ ImageFlags.SplitInverse | ImageFlags.SplitLeft, archive, pdf)
                    # Change target once again for left page
                    target = os.path.join(self.bookPath, '%05d.png' % (index * 2 + 1))

                # Convert page
                self.convertAndSave(source, target, device, flags, archive, pdf)

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
