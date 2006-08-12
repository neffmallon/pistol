#!/usr/bin/env python
"""\
 Use PIL to make a contact sheet from a number of images.
 This program was inspired by the Life Poster described here:
 
 http://www.mikematas.com/blog/2005/01/how-to-make-life-poster.html

 I found that my version of IPhoto was too old to do everything,
 plus the Python Imaging Library makes this pretty easy to do.

 My suggestion is to follow the instructions for the life poster
 through step 2, since the constrained cropping is hard to do
 without a graphical interface. Then export those files into
 a directory, and use the attached script to make a contact sheet.

 You can save the resulting image (caution, it will be huge: mine
 was 155 MB), re-import it to IPhoto, and order a poster for yourself.
"""

import os
import glob
import Image

def make_contact_sheet(fnames,(ncols,nrows),(photow,photoh),
                       (marl,mart,marr,marb),
                       padding):
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of sames of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marl         The left margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize((photow,photoh)) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew

def test():
    ncols,nrows = 7,14

    os.chdir('/home/rmuller/Desktop/alex')
    files = glob.glob('*.TIFF')

    # Don't bother reading in files we aren't going to use
    if len(files) > ncols*nrows: files = files[:ncols*nrows]

    # These are all in terms of pixels:
    photow,photoh = 200,150
    photo = (photow,photoh)

    margins = [5,5,5,5]

    padding = 1
    
    inew = make_contact_sheet(files,(ncols,nrows),photo,margins,padding)
    inew.save('bs.png')
    #os.system('display bs.png')
    os.system('open bs.png')

if __name__ == '__main__': test()


