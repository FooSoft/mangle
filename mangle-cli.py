#!/usr/bin/env python2

import shutil
import sys
import os
import getopt

from mangle.book import Book
import mangle.cbz
import mangle.image

try:
	opts, args = getopt.getopt(sys.argv[1:], 'd:t:o:')
except getopt.GetoptError, err:
	print str(err)
	sys.exit(2)

directory = '.'

book = Book()
book.device = 'Kindle 3'
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


for index in range(1, len(args)):
	target = os.path.join(bookPath, '%05d.png' % index)

	mangle.image.convertImage(args[index], target, str(book.device), book.imageFlags)
	archive.addFile(target);


if 'Image' not in book.outputFormat:
	shutil.rmtree(bookPath)

archive.close()
