# Mangle #

Mangle is a cross-platform image converter and optimizer built for reading Manga on the Amazon Kindle and other E-ink
devices written in Python. With this application you can easily:

*   Sort and organize images from different directories; bulk rename feature exists for output to the Kindle.
*   Optionally re-save images in a format Kindle will be sure to understand with no visible quality loss.
*   Downsample and rotate images for optimal viewing on Kindle, convert to grayscale to save space and improve contrast.
*   Automatically generate book meta-data so that your Manga is always properly detected and viewable in-order.

## Motivation ##

Many years ago I received an [Amazon Kindle](http://en.wikipedia.org/wiki/Kindle) gift. I immediately began playing
around with it and reading about certain undocumented features that the Kindle has to offer. After a couple of hours I
discovered it to be the perfect device for reading [Manga](http://en.wikipedia.org/wiki/Manga) is almost always
grayscale, and the aspect ratio fits the Kindle's 600x800 pixel screen almost perfectly. Better yet, the Kindle's
undocumented image viewer actually keeps track of the last image you viewed and thus you are always able to return to
the page you left off on when you power on your Kindle. The device supports several popular image formats (jpeg, png,
gif, etc), and is able to dither and downscale images to fit the screen.

However... The Kindle's image viewer does have certain shortcomings:

*   The Kindle is very picky about file format; any additional embedded data (thumbnails, comments, possibly even EXIF
    data) can confuse it. As a result, images may not display properly or even not at all (which actually prevents you
    from reading the given book, as one bad panel will prevent you from viewing subsequent images).
*   The first image that you view in a Manga (until the Kindle first writes the "bookmark" file) seems to be arbitrary
    even when files are named sequentially.  About half the time it will correctly pick the first file in the batch, at
    other times it will pick out some other image seemingly at random.
*   Normally for Kindle to find your Manga scans you have to press <kbd>Alt</kbd> + <kbd>Z</kbd> on the home screen. I
    haven't always had luck with it correctly identifying image directories. At other times, after finding an image
    directory the Kindle will appear to hang while trying to access it (forcing you to return to the home screen).
*   The Kindle image viewer has no functionality to rotate images. So if there is a horizontally large image (such as
    what often happens with dual-page scans), it can be difficult to make out the text because the image is simply
    scaled to fit (consequently leaving a lot of wasted space at the bottom of the screen).
*   Scanlation images are oftentimes much larger than the 600x800 screen; not only does this make them take more space
    on your memory card but it also slows down image loading (the Kindle has to read more data off of the slow SD card
    and scale the image). Scanlations often also include color scans of covers and inserts which take up more space than
    a grayscale equivalent (which is would be fine for the Kindle's limited display).
*   Kindle's image viewer provides no way to sort images (to determine in which order they are shown). This can be very
    problematic especially considering that scanlation groups have differing naming conventions, and as a result files
    from later chapters may appear before earlier ones when you are reading your Manga (spoilers ftl).

Mangle was born out of my annoyance with these issues. The program name is a portmanteau of "Manga" and "Kindle"; I
thought it was pretty clever at the time.

## Usage ##

1.  Add the desired images and image directories to the current book.
2.  Re-order the images as needed (files pre-sorted alphabetically).
3.  Configure the book title and image processing options.
4.  Create a root-level directory on your Kindle called `pictures` (case sensitive).
5.  Export your images, selecting the `pictures` directory you just created.
6.  Enjoy your Manga (if it doesn't show up, press <kbd>Alt</kbd> + <kbd>Z</kbd> while on the home menu).

## Installation ##

Pre-build binaries are available for the platforms listed below. I don't have the means to make MacOS X releases myself,
so I am providing the old (and unsupported) package built by Rob White instead. Linux users should run Mangle directly
from source.

*  [magnle_win.zip](https://foosoft.net/projects/mangle/dl/mangle_win.zip)
*  [mangle_osx.zip](https://foosoft.net/projects/mangle/dl/mangle_osx.zip) (quite old)

To run Mangle from source make sure you have [Python](https://www.python.org/) and the following dependencies installed:

*   [PyQT4](http://www.riverbankcomputing.com/software/pyqt/download)
*   [Python 2.7](http://www.python.org/download/releases/2.7/)
*   [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/)
*   [ReportLab](https://pypi.python.org/pypi/reportlab)

## Screenshots ##

[![Main window](https://foosoft.net/projects/mangle/img/main-thumb.png)](https://foosoft.net/projects/mangle/img/main.png)
[![Options dialog](https://foosoft.net/projects/mangle/img/options-thumb.png)](https://foosoft.net/projects/mangle/img/options.png)

## On the Kindle... ##

[![](https://foosoft.net/projects/mangle/img/kindle1-thumb.png)](https://foosoft.net/projects/mangle/img/kindle1.png)
[![](https://foosoft.net/projects/mangle/img/kindle2-thumb.png)](https://foosoft.net/projects/mangle/img/kindle2.png)
[![](https://foosoft.net/projects/mangle/img/kindle3-thumb.png)](https://foosoft.net/projects/mangle/img/kindle3.png)
[![](https://foosoft.net/projects/mangle/img/kindle4-thumb.png)](https://foosoft.net/projects/mangle/img/kindle4.png)

## License ##

GPL
