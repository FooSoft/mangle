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


import os, os.path
from PyQt4 import QtGui, QtCore, QtXml, uic

import image
from resources import get_ui_path, get_image_path
from image import ImageFlags
from about import DialogAbout
from options import DialogOptions
from convert import DialogConvert

class Book:
    DefaultDevice = 'Kindle 3'
    DefaultOverwrite = True
    DefaultImageFlags = ImageFlags.Orient | ImageFlags.Resize | ImageFlags.Quantize


    def __init__(self):
        self.images = []
        self.filename = None
        self.modified = False
        self.title = None
        self.device = Book.DefaultDevice
        self.overwrite = Book.DefaultOverwrite
        self.imageFlags = Book.DefaultImageFlags


    def save(self, filename):
        document = QtXml.QDomDocument()

        root = document.createElement('book')
        document.appendChild(root)

        root.setAttribute('title', self.title)
        root.setAttribute('overwrite', 'true' if self.overwrite else 'false')
        root.setAttribute('device', self.device)
        root.setAttribute('imageFlags', self.imageFlags)

        for filenameImg in self.images:
            itemImg = document.createElement('image')
            root.appendChild(itemImg)
            itemImg.setAttribute('filename', filenameImg)

        textXml = document.toString(4).toUtf8()

        try:
            fileXml = open(unicode(filename), 'w')
            fileXml.write(textXml)
            fileXml.close()
        except IOError:
            raise RuntimeError('Cannot create book file %s' % filename)

        self.filename = filename
        self.modified = False


    def load(self, filename):
        try:
            fileXml = open(unicode(filename), 'r')
            textXml = fileXml.read()
            fileXml.close()
        except IOError:
            raise RuntimeError('Cannot open book file %s' % filename)

        document = QtXml.QDomDocument()

        if not document.setContent(QtCore.QString.fromUtf8(textXml)):
            raise RuntimeError('Error parsing book file %s' % filename)

        root = document.documentElement()
        if root.tagName() != 'book':
            raise RuntimeError('Unexpected book format in file %s' % filename)

        self.title = root.attribute('title', 'Untitled')
        self.overwrite = root.attribute('overwrite', 'true' if Book.DefaultOverwrite else 'false') == 'true'
        self.device = root.attribute('device', Book.DefaultDevice)
        self.imageFlags = int(root.attribute('imageFlags', str(Book.DefaultImageFlags)))
        self.filename = filename
        self.modified = False
        self.images = []

        items = root.elementsByTagName('image')
        if items == None:
            return

        for i in xrange(0, len(items)):
            item = items.at(i).toElement()
            if item.hasAttribute('filename'):
                self.images.append(item.attribute('filename'))


class MainWindowBook(QtGui.QMainWindow):
    def __init__(self, filename=None):
        QtGui.QMainWindow.__init__(self)
        ui = uic.loadUi(os.path.join(get_ui_path(), 'book.ui'), self)
        self._setIcon(self.actionFileNew, 'file_new')
        self._setIcon(self.actionFileOpen, 'file_open')
        self._setIcon(self.actionFileSave, 'save_file')
        self._setIcon(self.actionBookAddFiles, 'add_file')
        self._setIcon(self.actionBookAddDirectory, 'add_directory')
        self._setIcon(self.actionBookRemove, 'remove_files')
        self._setIcon(self.actionBookShiftUp, 'shift_up')
        self._setIcon(self.actionBookShiftDown, 'shift_down')
        self._setIcon(self.actionBookExport, 'export_book')
        self.connect(self.actionFileNew, QtCore.SIGNAL('triggered()'), self.onFileNew)
        self.connect(self.actionFileOpen, QtCore.SIGNAL('triggered()'), self.onFileOpen)
        self.connect(self.actionFileSave, QtCore.SIGNAL('triggered()'), self.onFileSave)
        self.connect(self.actionFileSaveAs, QtCore.SIGNAL('triggered()'), self.onFileSaveAs)
        self.connect(self.actionBookOptions, QtCore.SIGNAL('triggered()'), self.onBookOptions)
        self.connect(self.actionBookAddFiles, QtCore.SIGNAL('triggered()'), self.onBookAddFiles)
        self.connect(self.actionBookAddDirectory, QtCore.SIGNAL('triggered()'), self.onBookAddDirectory)
        self.connect(self.actionBookShiftUp, QtCore.SIGNAL('triggered()'), self.onBookShiftUp)
        self.connect(self.actionBookShiftDown, QtCore.SIGNAL('triggered()'), self.onBookShiftDown)
        self.connect(self.actionBookRemove, QtCore.SIGNAL('triggered()'), self.onBookRemove)
        self.connect(self.actionBookExport, QtCore.SIGNAL('triggered()'), self.onBookExport)
        self.connect(self.actionHelpAbout, QtCore.SIGNAL('triggered()'), self.onHelpAbout)
        self.connect(self.actionHelpHomepage, QtCore.SIGNAL('triggered()'), self.onHelpHomepage)
        self.connect(self.listWidgetFiles, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.onFilesContextMenu)
        self.connect(self.listWidgetFiles, QtCore.SIGNAL('itemDoubleClicked (QListWidgetItem *)'), self.onFilesDoubleClick)
        self.listWidgetFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.book = Book()
        if filename != None:
            self.loadBook(filename)


    @staticmethod
    def _setIcon(action, name):
        action.setIcon(QtGui.QIcon(os.path.join(get_image_path(), '%s.png' % name)))


    def closeEvent(self, event):
        if not self.saveIfNeeded():
            event.ignore()


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()


    def dropEvent(self, event):
        directories = []
        filenames = []

        for url in event.mimeData().urls():
            filename = url.toLocalFile()
            if self.isImageFile(filename):
                filenames.append(filename)
            elif os.path.isdir(unicode(filename)):
                directories.append(filename)

        self.addImageDirs(directories)
        self.addImageFiles(filenames)


    def onFileNew(self):
        if self.saveIfNeeded():
            self.book = Book()
            self.listWidgetFiles.clear()


    def onFileOpen(self):
        if not self.saveIfNeeded():
            return

        filename = QtGui.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a book file to open',
            filter='Mangle files (*.mngl);;All files (*.*)'
        )
        if not filename.isNull():
            self.loadBook(self.cleanupBookFile(filename))


    def onFileSave(self):
        self.saveBook(False)


    def onFileSaveAs(self):
        self.saveBook(True)


    def onFilesContextMenu(self, point):
        menu = QtGui.QMenu(self)
        menu.addAction(self.menu_Add.menuAction())

        if len(self.listWidgetFiles.selectedItems()) > 0:
            menu.addAction(self.menu_Shift.menuAction())
            menu.addAction(self.actionBookRemove)

        menu.exec_(self.listWidgetFiles.mapToGlobal(point))


    def onFilesDoubleClick(self, item):
        services = QtGui.QDesktopServices()
        services.openUrl(QtCore.QUrl.fromLocalFile(item.text()))


    def onBookAddFiles(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select image file(s) to add',
            filter='Image files (*.jpeg *.jpg *.gif *.png);;All files (*.*)'
        )
        self.addImageFiles(filenames)


    def onBookAddDirectory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select an image directory to add')
        if not directory.isNull():
            self.addImageDirs([directory])


    def onBookShiftUp(self):
        self.shiftImageFiles(-1)


    def onBookShiftDown(self):
        self.shiftImageFiles(1)


    def onBookRemove(self):
        self.removeImageFiles()


    def onBookOptions(self):
        dialog = DialogOptions(self, self.book)
        dialog.exec_()


    def onBookExport(self):
        if len(self.book.images) == 0:
            QtGui.QMessageBox.warning(self, 'Mangle', 'This book has no images to export')
            return

        if self.book.title == None:
            dialog = DialogOptions(self, self.book)
            if dialog.exec_() == QtGui.QDialog.Rejected:
                return

        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select a directory to export book to')
        if not directory.isNull():
            dialog = DialogConvert(self, self.book, directory)
            dialog.exec_()


    def onHelpHomepage(self):
        services = QtGui.QDesktopServices()
        services.openUrl(QtCore.QUrl('http://foosoft.net/mangle'))


    def onHelpAbout(self):
        dialog = DialogAbout(self)
        dialog.exec_()


    def saveIfNeeded(self):
        if not self.book.modified:
            return True

        result = QtGui.QMessageBox.question(
            self,
            'Mangle',
            'Save changes to the current book?',
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Yes
        )

        return (
            result == QtGui.QMessageBox.No or
            result == QtGui.QMessageBox.Yes and self.saveBook()
        )


    def saveBook(self, browse=False):
        if self.book.title == None:
            QtGui.QMessageBox.warning(self, 'Mangle', 'You must specify a title for this book before saving')
            return False

        filename = self.book.filename
        if filename == None or browse:
            filename = QtGui.QFileDialog.getSaveFileName(
                parent=self,
                caption='Select a book file to save as',
                filter='Mangle files (*.mngl);;All files (*.*)'
            )
            if filename.isNull():
                return False
            filename = self.cleanupBookFile(filename)

        try:
            self.book.save(filename)
        except RuntimeError, error:
            QtGui.QMessageBox.critical(self, 'Mangle', str(error))
            return False

        return True


    def loadBook(self, filename):
        try:
            self.book.load(filename)
        except RuntimeError, error:
            QtGui.QMessageBox.critical(self, 'Mangle', str(error))
        else:
            self.listWidgetFiles.clear()
            for image in self.book.images:
                self.listWidgetFiles.addItem(image)


    def shiftImageFile(self, row, delta):
        validShift = (
            (delta > 0 and row < self.listWidgetFiles.count() - delta) or
            (delta < 0 and row >= abs(delta))
        )
        if not validShift:
            return

        item = self.listWidgetFiles.takeItem(row)

        self.listWidgetFiles.insertItem(row + delta, item)
        self.listWidgetFiles.setItemSelected(item, True)

        self.book.modified = True
        self.book.images[row], self.book.images[row + delta] = (
            self.book.images[row + delta], self.book.images[row]
        )


    def shiftImageFiles(self, delta):
        items = self.listWidgetFiles.selectedItems()
        rows = sorted([self.listWidgetFiles.row(item) for item in items])

        for row in rows if delta < 0 else reversed(rows):
            self.shiftImageFile(row, delta)


    def removeImageFiles(self):
        for item in self.listWidgetFiles.selectedItems():
            row = self.listWidgetFiles.row(item)
            self.listWidgetFiles.takeItem(row)
            self.book.images.remove(item.text())
            self.book.modified = True


    def addImageFiles(self, filenames):
        filenames.sort()

        filenamesListed = []
        for i in xrange(0, self.listWidgetFiles.count()):
            filenamesListed.append(self.listWidgetFiles.item(i).text())

        for filename in filenames:
            if filename not in filenamesListed:
                filename = QtCore.QString(filename)
                self.listWidgetFiles.addItem(filename)
                self.book.images.append(filename)
                self.book.modified = True


    def addImageDirs(self, directories):
        filenames = []

        for directory in directories:
            for root, subdirs, subfiles in os.walk(unicode(directory)):
                for filename in subfiles:
                    path = os.path.join(root, filename)
                    if self.isImageFile(path):
                        filenames.append(path)

        self.addImageFiles(filenames)


    def isImageFile(self, filename):
        imageExts = ['.jpeg', '.jpg', '.gif', '.png']
        filename = unicode(filename)
        return (
            os.path.isfile(filename) and
            os.path.splitext(filename)[1].lower() in imageExts
        )


    def cleanupBookFile(self, filename):
        if len(os.path.splitext(unicode(filename))[1]) == 0:
            filename += '.mngl'
        return filename
