from __future__ import division
import math
import pprint
import scipy.misc
import numpy as np
from scipy.misc import imresize

pp = pprint.PrettyPrinter()

get_stddev = lambda x, k_h, k_w: 1/math.sqrt(k_w*k_h*x.get_shape()[-1])


def transform_image(image_path, image_size, is_crop):
    return transform(imread(image_path), image_size, is_crop)


def resize(x, size):
    x = np.copy((x+1.)*127.5).astype("uint8")
    y = imresize(x, [size, size])
    return y


def imread(path):
    return scipy.misc.imread(path).astype(np.float)


def center_crop(x, crop_h, crop_w=None, resize_w=256):
    if crop_w is None:
        crop_w = crop_h
    h, w = x.shape[:2]
    j = int(round((h - crop_h)/2.))
    i = int(round((w - crop_w)/2.))
    return scipy.misc.imresize(x[j:j+crop_h, i:i+crop_w],
                               [resize_w, resize_w])


def transform(image, size, is_crop):
    # npx : # of pixels width/height of image
    if is_crop:
        cropped_image = center_crop(image, size)
    else:
        cropped_image = image
    return np.array(cropped_image)/127.5 - 1.


def save_image(image, image_path):
    img = inverse_transform(image)
    return scipy.misc.imsave(image_path, img[0])


def inverse_transform(image):
    return (image+1.)/2.


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    img = np.zeros((h * size[0], w * size[1], 3))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j*h:j*h+h, i*w:i*w+w, :] = image

    return img