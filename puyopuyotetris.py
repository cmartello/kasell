"""
puyopuyotetris.py

This module is for handling scores from videos of Puyo Puyo Tetris.
Specifically tetris endless marathon mode; any other modes and your
mileage will vary greatly.
"""

from glob import glob

import pytesseract
from PIL import Image, ImageOps


def extract_data(user):
    """Extracts the time, level, lines, and score from a PIL image object
    and returns them as a tuple.  This function is used elsewhere to
    generate a CSV file for analysis later.
    """

    rects = {'time': (757, 378, 955, 416),
             'level': (780, 299, 959, 341),
             'lines': (776, 218, 957, 263),
             'score': (769, 464, 955, 496)}

    values = dict()

    for item in rects:
        # crop region
        crop = user.crop(rects[item])

        # convert and invert for tesseract's aid
        crop = crop.convert('L')
        crop = ImageOps.invert(crop)

        # extract the raw text
        text = pytesseract.image_to_string(crop)

        # empty text?  default zero
        if text == '':
            text = '0'

        # convert to an integer unless we're working with time
        if item != 'time':
            values[item] = int(''.join([x for x in text if x.isnumeric()]))
        elif item == 'time':
            values[item] = text

    # repack as a tuple and return
    return (values['time'], values['level'], values['lines'], values['score'])


def process_files(userglob):
    """Accepts a string that is used as a file glob.  Each file is opened
    and processed through extract_data().  Implemented as a generator
    and each output is a tuple with the frame number prepending the output
    from extract_data().
    """

    # get the specified file list
    images = glob(userglob)
    images.sort()

    frame = 0
    for pic in images:
        tmp = Image.open(pic)
        data = extract_data(tmp)
        data = (frame, data[0], data[1], data[2], data[3])
        frame += 1
        yield data


# some testing code
if __name__ == '__main__':
    for info in process_files('work/*.png'):
        print(info)
