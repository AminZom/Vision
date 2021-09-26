"""
Dataset creator pipeline

"""
# imports

class circle_gen():

    def min_max(self):
        # number of creating objects in mind
        return None

    def change_contrast(self):
        # background, foreground change all in grayscale
        #
        return None

    def save_img(self):
        return None

    def save_annotation(self):
        # save center (x, y), radius
        pass

    def circle_width(self):
        pass

    def random_circles(self):
        # circle size change, numbers, contrast, then save_img, then save_annotation
        pass

import numpy as np
from shapely.geometry.point import Point
from skimage.draw import circle_perimeter_aa
import sys


def draw_circle(img, row, col, rad):
    rr, cc, val = circle_perimeter_aa(row, col, rad)
    valid = (
        (rr >= 0) &
        (rr < img.shape[0]) &
        (cc >= 0) &
        (cc < img.shape[1])
    )
    img[rr[valid], cc[valid]] = val[valid]

def iou(params0, params1):
    row0, col0, rad0 = params0
    row1, col1, rad1 = params1

    shape0 = Point(row0, col0).buffer(rad0)
    shape1 = Point(row1, col1).buffer(rad1)

    return (
        shape0.intersection(shape1).area /
        shape0.union(shape1).area
    )

def noisy_circle(size, radius, noise):
    img = np.zeros((size, size), dtype=np.float)

    # Circle
    row = np.random.randint(size)
    col = np.random.randint(size)
    rad = np.random.randint(10, max(10, radius))
    draw_circle(img, row, col, rad)

    # Noise
    img += noise * np.random.rand(*img.shape)
    return (row, col, rad), img