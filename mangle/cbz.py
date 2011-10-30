# Copyright (C) 2011  Marek Kubica <marek@xivilization.net>
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
from zipfile import ZipFile, ZIP_STORED


class Archive(object):
    def __init__(self, path):
        outputDirectory = os.path.dirname(path)
        outputFileName = '%s.cbz' % os.path.basename(path)
        outputPath = os.path.join(outputDirectory, outputFileName)
        self.zipfile = ZipFile(outputPath, 'w', ZIP_STORED)


    def addFile(self, filename):
        arcname = os.path.basename(filename)
        self.zipfile.write(filename, arcname)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def close(self):
        self.zipfile.close()
