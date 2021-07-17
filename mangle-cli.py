#!/usr/bin/env python2
"""python mangle-cli.py  extracted_cbz_folder/*
    -d directory_name defaults to ./
    -t title defaults 'Unknown'
    -o book.outputFormat defaults to 'CBZ only'

NOTE order of arguments for image files is significant.

Example:

    mkdir my_comic
    cd my_comic
    7z x /full/path/my/comic.cbz
    cd ..
    python mangle-cli.py -tmy_comic  my_comic/*

"""

import shutil
import sys
import os
import getopt

import mangle.cbz
import mangle.image
from mangle.image import ImageFlags


class FakeBook:
	device = 'Kindle 2/3/Touch'  # See mangle/image.py KindleData.Profiles
	outputFormat = 'CBZ only'
	title = 'Unknown'
	imageFlags = ImageFlags.Orient | ImageFlags.Resize | ImageFlags.Quantize


try:
	opts, args = getopt.getopt(sys.argv[1:], 'd:t:o:')
except getopt.GetoptError, err:
	print(str(err))
	sys.exit(2)

directory = '.'

book = FakeBook()
book.device = 'Kindle 2/3/Touch'
#book.device = 'Kindle Paperwhite 1 & 2'
book.outputFormat = 'CBZ only'
book.title = 'Unknown'


for o,a in opts:
	if o == '-d':
		directory = a
	elif o == '-t':
		book.title = a
	elif o == '-o':
		book.outputFormat = a


bookPath = os.path.join(directory, book.title)

archive = mangle.cbz.Archive(bookPath)

if not os.path.isdir(bookPath):
	os.makedirs(bookPath)


for index in range(0, len(args)):
	target = os.path.join(bookPath, '%05d.png' % index)  # FIXME preserve original; format and name?

	print(index, args[index], target)  # cheap display progress
	mangle.image.convertImage(args[index], target, str(book.device), book.imageFlags)
	archive.addFile(target);


if 'Image' not in book.outputFormat:
	shutil.rmtree(bookPath)

archive.close()

