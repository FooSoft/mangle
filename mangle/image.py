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

from PIL import Image, ImageDraw, ImageStat, ImageChops, ImageOps


class ImageFlags:
    Orient = 1 << 0
    Resize = 1 << 1
    Frame = 1 << 2
    Quantize = 1 << 3
    ScaleCrop = 1 << 4
    SplitRightLeft = 1 << 5    # split right then left
    SplitRight = 1 << 6        # split only the right page
    SplitLeft = 1 << 7         # split only the left page
    SplitLeftRight = 1 << 8    # split left then right page
    AutoCrop = 1 << 9


class KindleData:
    Palette4 = [
        0x00, 0x00, 0x00,
        0x55, 0x55, 0x55,
        0xaa, 0xaa, 0xaa,
        0xff, 0xff, 0xff
    ]

    Palette15a = [
        0x00, 0x00, 0x00,
        0x11, 0x11, 0x11,
        0x22, 0x22, 0x22,
        0x33, 0x33, 0x33,
        0x44, 0x44, 0x44,
        0x55, 0x55, 0x55,
        0x66, 0x66, 0x66,
        0x77, 0x77, 0x77,
        0x88, 0x88, 0x88,
        0x99, 0x99, 0x99,
        0xaa, 0xaa, 0xaa,
        0xbb, 0xbb, 0xbb,
        0xcc, 0xcc, 0xcc,
        0xdd, 0xdd, 0xdd,
        0xff, 0xff, 0xff,
    ]

    Palette15b = [
        0x00, 0x00, 0x00,
        0x11, 0x11, 0x11,
        0x22, 0x22, 0x22,
        0x33, 0x33, 0x33,
        0x44, 0x44, 0x44,
        0x55, 0x55, 0x55,
        0x77, 0x77, 0x77,
        0x88, 0x88, 0x88,
        0x99, 0x99, 0x99,
        0xaa, 0xaa, 0xaa,
        0xbb, 0xbb, 0xbb,
        0xcc, 0xcc, 0xcc,
        0xdd, 0xdd, 0xdd,
        0xee, 0xee, 0xee,
        0xff, 0xff, 0xff,
    ]

    Profiles = {
        'Kindle 1': ((600, 800), Palette4),
        'Kindle 2/3/Touch': ((600, 800), Palette15a),
        'Kindle 4 & 5': ((600, 800), Palette15b),
        'Kindle DX/DXG': ((824, 1200), Palette15a),
        'Kindle Paperwhite 1 & 2': ((758, 1024), Palette15b),
        'Kindle Paperwhite 3/Voyage/Oasis': ((1072, 1448), Palette15b),
        'Kobo Mini/Touch': ((600, 800), Palette15b),
        'Kobo Glo': ((768, 1024), Palette15b),
        'Kobo Glo HD': ((1072, 1448), Palette15b),
        'Kobo Aura': ((758, 1024), Palette15b),
        'Kobo Aura HD': ((1080, 1440), Palette15b),
        'Kobo Aura H2O': ((1080, 1430), Palette15a),
    }


# decorate a function that use image, *** and if there
# is an exception raise by PIL (IOError) then return
# the original image because PIL cannot manage it
def protect_bad_image(func):
    def func_wrapper(*args, **kwargs):
        # If cannot convert (like a bogus image) return the original one
        # args will be "image" and other params are after
        try:
            return func(*args, **kwargs)
        except IOError: # Exception from PIL about bad image
            return args[0]

    return func_wrapper
    

@protect_bad_image    
def splitLeft(image):
    widthImg, heightImg = image.size

    return image.crop((0, 0, widthImg / 2, heightImg))


@protect_bad_image
def splitRight(image):
    widthImg, heightImg = image.size

    return image.crop((widthImg / 2, 0, widthImg, heightImg))


@protect_bad_image
def quantizeImage(image, palette):
    colors = len(palette) / 3
    if colors < 256:
        palette = palette + palette[:3] * (256 - colors)

    palImg = Image.new('P', (1, 1))
    palImg.putpalette(palette)

    return image.quantize(palette=palImg)


@protect_bad_image
def scaleCropImage(image, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size
    
    imgRatio = float(widthImg) / float(heightImg)
    devRatio = float(widthDev) / float(heightDev)

    # don't crop 2 page spreads.
    if imgRatio > devRatio:
        return resizeImage(image, size)
    
    return ImageOps.fit(image, size, Image.ANTIALIAS)


@protect_bad_image
def resizeImage(image, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    if widthImg <= widthDev and heightImg <= heightDev:
        return image

    ratioImg = float(widthImg) / float(heightImg)
    ratioWidth = float(widthImg) / float(widthDev)
    ratioHeight = float(heightImg) / float(heightDev)

    if ratioWidth > ratioHeight:
        widthImg = widthDev
        heightImg = int(widthDev / ratioImg)
    elif ratioWidth < ratioHeight:
        heightImg = heightDev
        widthImg = int(heightDev * ratioImg)
    else:
        widthImg, heightImg = size

    return image.resize((widthImg, heightImg), Image.ANTIALIAS)


@protect_bad_image
def formatImage(image):
    if image.mode == 'RGB':
        return image

    return image.convert('RGB')


@protect_bad_image
def orientImage(image, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    if (widthImg > heightImg) != (widthDev > heightDev):
        return image.rotate(90, Image.BICUBIC, True)
    return image


# We will auto crop the image, by removing just white part around the image
# by inverting colors, and asking a bounder box ^^
@protect_bad_image
def autoCropImage(image):
    try:
        x0, y0, xend, yend = ImageChops.invert(image).getbbox()
    except TypeError: # bad image, specific to chops
        return image
    image = image.crop((x0, y0, xend, yend))

    return image


def frameImage(image, foreground, background, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    pastePt = (
        max(0, (widthDev - widthImg) / 2),
        max(0, (heightDev - heightImg) / 2)
    )

    corner1 = (
        pastePt[0] - 1,
        pastePt[1] - 1
    )

    corner2 = (
        pastePt[0] + widthImg + 1,
        pastePt[1] + heightImg + 1
    )

    imageBg = Image.new(image.mode, size, background)
    imageBg.paste(image, pastePt)

    draw = ImageDraw.Draw(imageBg)
    draw.rectangle([corner1, corner2], outline=foreground)

    return imageBg


def loadImage(source):
    try:
        return Image.open(source)
    except IOError:
        raise RuntimeError('Cannot read image file %s' % source)
    

def saveImage(image, target):
    try:
        image.save(target)
    except IOError:
        raise RuntimeError('Cannot write image file %s' % target)


# Look if the image is more width than hight, if not, means
# it's should not be split (like the front page of a manga,
# when all the inner pages are double)
def isSplitable(source):
    image = loadImage(source)
    try:
        widthImg, heightImg = image.size
        return  widthImg > heightImg
    except IOError: 
        raise RuntimeError('Cannot read image file %s' % source)


def convertImage(source, target, device, flags):
    try:
        size, palette = KindleData.Profiles[device]
    except KeyError:
        raise RuntimeError('Unexpected output device %s' % device)
    # Load image from source path
    image = loadImage(source)

    # Format according to palette
    image = formatImage(image)

    # Apply flag transforms
    if flags & ImageFlags.SplitRight:
        image = splitRight(image)
    if flags & ImageFlags.SplitRightLeft:
        image = splitLeft(image)
    if flags & ImageFlags.SplitLeft:
        image = splitLeft(image)
    if flags & ImageFlags.SplitLeftRight:
        image = splitRight(image)

    # Auto crop the image, but before manage size and co, clean the source so
    if flags & ImageFlags.AutoCrop:
        image = autoCropImage(image)
    if flags & ImageFlags.Orient:
        image = orientImage(image, size)
    if flags & ImageFlags.Resize:
        image = resizeImage(image, size)
    if flags & ImageFlags.ScaleCrop:
        image = scaleCropImage(image, size)
    if flags & ImageFlags.Frame:
        image = frameImage(image, tuple(palette[:3]), tuple(palette[-3:]), size)
    if flags & ImageFlags.Quantize:
        image = quantizeImage(image, palette)
    
    saveImage(image, target)
