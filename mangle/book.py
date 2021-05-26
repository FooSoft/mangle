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

import re
from os.path import basename
import os.path
import tempfile
from zipfile import ZipFile

# from PyQt4 import QtGui, QtCore, QtXml, uic
from PyQt5 import QtGui, QtCore, uic, QtXml, QtWidgets
from PyQt5.QtCore import *

from .about import DialogAbout
from .convert import DialogConvert
from .image import ImageFlags
from .options import DialogOptions
from . import util


# Sort function used to sort files in a natural order, by lowering
# characters, and managing multi levels of integers (tome 1/ page 1.jpg, etc etc)
# cf: See http://www.codinghorror.com/blog/archives/001018.html
def natural_key(string_):
    l = []
    print(f"string_ => {string_}")
    print(f"type(string_) => {type(string_)}")
    if string_: 
        for s in re.split(r'(\d+)', string_):
            # str does not have isdigit, so convert it if needed
            if isinstance(s, str):
                s = str(s)
            if s.isdigit():
                l.append(int(s))
            else:
                l.append(s.lower())
    return l


class Book(object):
    DefaultDevice       = 'Kindle Paperwhite 3/Voyage/Oasis'
    DefaultOutputFormat = 'CBZ only'
    DefaultOverwrite    = True
    DefaultImageFlags   = ImageFlags.Orient | ImageFlags.Resize | ImageFlags.Quantize


    def __init__(self):
        self.images       = []
        self.filename     = None
        self.modified     = False
        self.title        = None
        self.titleSet     = False
        self.device       = Book.DefaultDevice
        self.overwrite    = Book.DefaultOverwrite
        self.imageFlags   = Book.DefaultImageFlags
        self.outputFormat = Book.DefaultOutputFormat


    def save(self, filename):
        document = QtXml.QDomDocument()

        root = document.createElement('book')
        document.appendChild(root)

        root.setAttribute('title', self.title)
        root.setAttribute('overwrite', 'true' if self.overwrite else 'false')
        root.setAttribute('device', self.device)
        root.setAttribute('imageFlags', self.imageFlags)
        root.setAttribute('outputFormat', self.outputFormat)

        for filenameImg in self.images:
            itemImg = document.createElement('image')
            root.appendChild(itemImg)
            itemImg.setAttribute('filename', filenameImg)

        textXml = document.toString(4)

        if len(filename) == 2:
            filename = filename[0] # filename received is a tuple: get the first item

        try:
            fileXml = open(str(filename), 'w')
            fileXml.write(textXml)
            fileXml.close()
        except IOError as ioe:
            print(f"IOError caught =>\n{ioe}")
            raise RuntimeError(f'Can\'t save file {filename}')

        self.filename = filename
        self.modified = False


    def load(self, filename):
        try:
            fileXml = open(str(filename), 'r')
            textXml = fileXml.read()
            fileXml.close()
        except IOError:
            raise RuntimeError(f'Can\'t open Mangle file {filename}')

        document = QtXml.QDomDocument()

        if not document.setContent(textXml):
            raise RuntimeError(f'Error parsing Mangle file {filename}')

        root = document.documentElement()
        if root.tagName() != 'book':
            raise RuntimeError(f'Unexpected Mangle format in file {filename}')

        self.title        = root.attribute('title', 'Untitled')
        self.overwrite    = root.attribute('overwrite', 'true' if Book.DefaultOverwrite else 'false') == 'true'
        self.device       = root.attribute('device', Book.DefaultDevice)
        self.outputFormat = root.attribute('outputFormat', Book.DefaultOutputFormat)
        self.imageFlags   = int(root.attribute('imageFlags', str(Book.DefaultImageFlags)))
        self.filename     = filename
        self.modified     = False
        self.images       = []

        items = root.elementsByTagName('image')
        if items is None:
            return

        for i in range(0, len(items)):
            item = items.at(i).toElement()
            if item.hasAttribute('filename'):
                self.images.append(item.attribute('filename'))


class MainWindowBook(QtWidgets.QMainWindow):
    def __init__(self, filename=None):
        QtWidgets.QMainWindow.__init__(self)

        uic.loadUi(util.buildResPath('mangle/ui/book.ui'), self)
        self.listWidgetFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.actionFileNew.triggered.connect(self.onFileNew)
        self.actionFileOpen.triggered.connect(self.onFileOpen)
        self.actionFileSave.triggered.connect(self.onFileSave)
        self.actionFileSaveAs.triggered.connect(self.onFileSaveAs)
        self.actionBookOptions.triggered.connect(self.onBookOptions)
        self.actionBookAddFiles.triggered.connect(self.onBookAddFiles)
        self.actionBookAddDirectory.triggered.connect(self.onBookAddDirectory)
        self.actionBookShiftUp.triggered.connect(self.onBookShiftUp)
        self.actionBookShiftDown.triggered.connect(self.onBookShiftDown)
        self.actionBookRemove.triggered.connect(self.onBookRemove)
        self.actionBookExport.triggered.connect(self.onBookExport)
        self.actionHelpAbout.triggered.connect(self.onHelpAbout)
        self.actionHelpHomepage.triggered.connect(self.onHelpHomepage)
        self.listWidgetFiles.customContextMenuRequested.connect(self.onFilesContextMenu)
        self.listWidgetFiles.itemDoubleClicked.connect(self.onFilesDoubleClick)

        self.book = Book()
        if filename is not None:
            self.loadBook(filename)


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
            elif os.path.isdir(str(filename)):
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

        filename = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a book file to open',
            filter='Mangle files (*.mngl);;All files (*.*)'
        )
        filename = filename[0] # first item is filename (second is filter)

        if filename:
            self.loadBook(self.cleanupBookFile(filename))


    def onFileSave(self):
        self.saveBook(False)


    def onFileSaveAs(self):
        self.saveBook(True)


    def onFilesContextMenu(self, point):
        menu = QtWidgets.QMenu(self)
        menu.addAction(self.menu_Add.menuAction())

        if len(self.listWidgetFiles.selectedItems()) > 0:
            menu.addAction(self.menu_Shift.menuAction())
            menu.addAction(self.actionBookRemove)

        menu.exec_(self.listWidgetFiles.mapToGlobal(point))


    def onFilesDoubleClick(self, item):
        services = QtGui.QDesktopServices()
        services.openUrl(QtCore.QUrl.fromLocalFile(item.text()))


    def onBookAddFiles(self):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select image file(s) to add',
            filter='Image files (*.jpeg *.jpg *.gif *.png);;Comic files (*.cbz)'
        )
        filenames = filenames[0] # get first tuple item (second is file filter)
        
        if(self.containsCbzFile(filenames)):
            self.addCBZFiles(filenames)
        else:
            self.addImageFiles(filenames)


    def onBookAddDirectory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select an image directory to add')
        if directory:
            self.book.title = os.path.basename(os.path.normpath(str(directory)))
            self.addImageDirs([directory])


    def onBookShiftUp(self):
        self.shiftImageFiles(-1)


    def onBookShiftDown(self):
        self.shiftImageFiles(1)


    def onBookRemove(self):
        self.removeImageFiles()


    def onBookOptions(self):
        dialog = DialogOptions(self, self.book)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.book.titleSet = True


    def onBookExport(self):
        if len(self.book.images) == 0:
            QtWidgets.QMessageBox.warning(self, 'Mangle', 'This book has no images to export')
            return

        if not self.book.titleSet:  # if self.book.title is None:
            dialog = DialogOptions(self, self.book)
            if dialog.exec_() == QtWidgets.QDialog.Rejected:
                return
            else:
                self.book.titleSet = True

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a directory to export book to')
        if directory:
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

        result = QtWidgets.QMessageBox.question(
            self,
            'Mangle',
            'Save changes to the current book?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Yes
        )

        return (
            result == QtWidgets.QMessageBox.No or
            result == QtWidgets.QMessageBox.Yes and self.saveBook()
        )


    def saveBook(self, browse=False):
        if self.book.title is None:
            QtWidgets.QMessageBox.warning(self, 'Mangle', 'You must specify a title for this book before saving')
            return False

        filename = self.book.filename
        if filename is None or browse:
            filename = QtWidgets.QFileDialog.getSaveFileName(
                parent=self,
                caption='Select a book file to save as',
                filter='Mangle files (*.mngl);;All files (*.*)'
            )
            if not filename:
                return False
            filename = self.cleanupBookFile(filename)

        try:
            self.book.save(filename)
        except RuntimeError as error:
            QtWidgets.QMessageBox.critical(self, 'Mangle', str(error))
            return False

        return True


    def loadBook(self, filename):
        try:
            self.book.load(filename)
        except RuntimeError as error:
            QtWidgets.QMessageBox.critical(self, 'Mangle', str(error))
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
        filenamesListed = []
        for i in range(0, self.listWidgetFiles.count()):
            filenamesListed.append(self.listWidgetFiles.item(i).text())

        # Get files but in a natural sorted order
        sorted_filenames = sorted(filenames, key=natural_key)
        
        for filename in sorted_filenames:
            if filename not in filenamesListed:
                filename = str(filename)
                self.listWidgetFiles.addItem(filename)
                self.book.images.append(filename)
                self.book.modified = True


    def addImageDirs(self, directories):
        filenames = []

        for directory in directories:
            for root, _, subfiles in os.walk(str(directory)):
                for filename in subfiles:
                    path = os.path.join(root, filename)
                    if self.isImageFile(path):
                        filenames.append(path)
                        
        self.addImageFiles(filenames)


    def addCBZFiles(self, filenames):
        directories = []
        tempDir = tempfile.gettempdir()
        filenames.sort()

        filenamesListed = []
        for i in range(0, self.listWidgetFiles.count()):
            filenamesListed.append(self.listWidgetFiles.item(i).text())

        for filename in filenames:
            folderName = os.path.splitext(basename(str(filename)))[0]
            path = tempDir + "/" + folderName + "/"
            cbzFile = ZipFile(str(filename))
            for f in cbzFile.namelist():
                if f.endswith('/'):
                    try:
                        os.makedirs(path + f)
                    except:
                        pass  # the dir exists so we are going to extract the images only.
                else:
                    cbzFile.extract(f, path)
            if os.path.isdir(str(path)):  # Add the directories
                directories.append(path)
        
        self.addImageDirs(directories)  # Add the files


    def isImageFile(self, filename):
        imageExts = ['.jpeg', '.jpg', '.gif', '.png']
        filename = str(filename)
        return (
            os.path.isfile(filename) and
            os.path.splitext(filename)[1].lower() in imageExts
        )

    def containsCbzFile(self, filenames):
        cbzExts = ['.cbz']
        for filename in filenames:
            filename = str(filename)
            result = (
            os.path.isfile(filename) and
            os.path.splitext(filename)[1].lower() in cbzExts
            )
            if result == True:
                return result
        return False     

    def cleanupBookFile(self, filename):
        if len(os.path.splitext(str(filename))[1]) == 0:
            filename += '.mngl'
        return filename
