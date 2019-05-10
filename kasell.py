import pytesseract
from PIL import Image, ImageOps
from sys import argv
from glob import glob

def ppt(fname):
    """Process a file supplied in fname.  File is assumed to be an image from
    a video of Puyo Puyo Tetris.  A region of the screen is cropped and
    fed into pytesseract, and an integer is returned.  For this function,
    the region of the screen is (769, 464) to (955, 496) -- where
    Puyo Puyo Tetrus keeps the score."""

    # load the image through PIL
    original = Image.open(fname)

    # crop it
    crop = original.crop((769, 464, 955, 496))

    # a little processing to help tesseract
    crop = crop.convert('L')
    crop = ImageOps.invert(crop)

    # pull out the text
    text = pytesseract.image_to_string(crop)

    if text == '':
        return 0

    # convert to integer
    output = int(''.join([x for x in text if x.isnumeric()]))

    # done
    return output

# testing
outfile = open('output.txt', 'w')
files = glob('work/test*.png')
files.sort()
for still in files:
    print(ppt(still), file=outfile)

