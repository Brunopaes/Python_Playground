# -*- coding: utf-8 -*-
from PIL import Image

import pytesseract
import numpy
import json
import cv2
import os


def read_json(path):
    """This function opens a json file and parses it content into a python dict.
    Parameters
    ----------
    path : str
        The json file path.
    Returns
    -------
    json.load : dict
        The json content parsed into a python dict.
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(e.args[-1])


def resize(max_width, max_height, image_path, out_dir, upscale=False):
    """This function resizes images into a directory.

    Parameters
    ----------
    max_width : int
        Max resized width.
    max_height : int
        Max resized height.
    image_path : str
        Images path.
    out_dir : str
        Goal directory.
    upscale : bool
        Upscale option. Default False.

    Returns
    -------

    """
    dir_path = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(dir_path, image_path)
    images = os.listdir(image_path)

    for counter, im in enumerate(images):
        image = cv2.imread(os.path.join(image_path, im))
        height = image.shape[0]
        width = image.shape[1]

        if upscale:
            if width < max_width:
                ratio = max_width / width
                new_height = int(ratio * height)
                image = cv2.resize(image, (max_width, new_height))

                if new_height < max_height:
                    ratio = max_height / new_height
                    new_width = int(ratio * max_width)
                    image = cv2.resize(image, (new_width, max_height))
        else:
            if width > max_width:
                ratio = max_width / width
                new_height = int(ratio * height)
                image = cv2.resize(image, (max_width, new_height))

                if new_height > max_height:
                    ratio = max_height / new_height
                    new_width = int(ratio * max_width)
                    image = cv2.resize(image, (new_width, max_height))

        out_path = os.path.join(out_dir, im)
        cv2.imwrite(out_path, image)


def ocr(path, lang='eng'):
    """Optical Character Recognition function.

    Parameters
    ----------
    path : str
        Image path.
    lang : str, optional
        Decoding language. Default english.

    Returns
    -------


    """
    image = Image.open(path)

    vectorized_image = numpy.asarray(image).astype(numpy.uint8)

    vectorized_image[:, :, 0] = 0
    vectorized_image[:, :, 2] = 0

    im = cv2.cvtColor(vectorized_image, cv2.COLOR_RGB2GRAY)

    return pytesseract.image_to_string(
        Image.fromarray(im),
        lang=lang
    )[:5]


def crop_image(path, coordinates):
    """This function crops a given image.

    Parameters
    ----------
    path : str
        To be cropped image path.
    coordinates : tuple
        Cropping bounding boxes.

    Returns
    -------

    """
    Image.open(path).crop(coordinates).save(path)
