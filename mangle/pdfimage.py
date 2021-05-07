# Copyright (C) 2012  Cristian Lizana <cristian@lizana.in>
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


# import os.path

# from reportlab.pdfgen import canvas

# from .image import KindleData


# class PDFImage(object):
#     def __init__(self, path, title, device):
#         outputDirectory = os.path.dirname(path)
#         outputFileName = '%s.pdf' % os.path.basename(path)
#         outputPath = os.path.join(outputDirectory, outputFileName)
#         self.currentDevice = device
#         self.bookTitle = title
#         self.pageSize = KindleData.Profiles[self.currentDevice][0]
#         # pagesize could be letter or A4 for standarization but we need to control some image sizes
#         self.canvas = canvas.Canvas(outputPath, pagesize=self.pageSize)
#         self.canvas.setAuthor("Mangle")
#         self.canvas.setTitle(self.bookTitle)
#         self.canvas.setSubject("Created for " + self.currentDevice)


#     def addImage(self, filename):
#         self.canvas.drawImage(filename, 0, 0, width=self.pageSize[0], height=self.pageSize[1], preserveAspectRatio=True, anchor='c')
#         self.canvas.showPage()

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.close()

#     def close(self):
#         self.canvas.save()
