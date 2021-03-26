#!/usr/bin/env python

# Copyright (C) 2013  Jan Martin
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


from distutils.core import setup
import py2exe
import sys


sys.argv.append('py2exe')
setup(
    name='Mangle',
    windows=[{'script': 'mangle.pyw'}],
    data_files=[('', ['LICENSE']),
                  ('mangle/ui', ['mangle/ui/book.ui',
                                 'mangle/ui/about.ui',
                                 'mangle/ui/options.ui']),
                  ('mangle/img', ['mangle/img/add_directory.png',
                                  'mangle/img/add_file.png',
                                  'mangle/img/banner_about.png',
                                  'mangle/img/book.png',
                                  'mangle/img/export_book.png',
                                  'mangle/img/file_new.png',
                                  'mangle/img/file_open.png',
                                  'mangle/img/remove_files.png',
                                  'mangle/img/save_file.png',
                                  'mangle/img/shift_down.png',
                                  'mangle/img/shift_up.png'])],
    options={'py2exe': {
        'bundle_files': 1,
        'includes': ['sip'],
        'packages': ['reportlab.pdfbase'],
        'dll_excludes': ['w9xpopen.exe']
    }},
    zipfile=None
)
