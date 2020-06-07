#!/usr/bin/env python3
"""
python3 find_temp_drift.py <directory>

Tries to find a temparature drift(s) in the series of images in the given folder
"""
import os
import sys
import math
import numpy
from PIL import Image


def image_head(img_arr, fraction):
    num_rows, num_cols = img_arr.shape
    fit_rows = int(fraction * num_rows)
    return img_arr[:fit_rows]


def image_tail(img_arr, fraction):
    num_rows, num_cols = img_arr.shape
    fit_rows = int(fraction * num_rows)
    return img_arr[-fit_rows:]


def head_and_tail_means(img_arr, fraction):
    """
    Calculate averages for first and last N rows
    return pair (first_rows_avg, last_rows_avg)
    """
    head = image_head(img_arr, fraction)
    tail = image_tail(img_arr, fraction)
    return int(head.mean()), int(tail.mean())


def rows_means(img_arr):
    """
    Calculate mean for every row (axis=1) in the given array 
    returns list of rows means
    """
    return numpy.mean(img_arr, axis=1)


def similar_means(xs, ys, threshold=0.03):
    # for every pair of values x, y from both lists
    # we check if they differ by > threshold (default 0.1)
    # if yes then means are not similar, if no we continue and finally return True
    for x, y in zip(xs, ys):
        if abs(y - x) / x > threshold:
            return False
    return True


def common_rows(head, tail):
    """
    Common between some head and some tail is a number of rows with very close means
    """
    head_means = rows_means(head)
    tail_means = rows_means(tail)
    assert len(head_means) == len(tail_means), "head and tail should have same number of rows"
    n = len(head_means)
    # trying n, n-1, n-2,...,0 rows
    for size in reversed(range(1, n + 1)):
        if similar_means(head_means[:size], tail_means[-size:]):
            return size
    # no match found, returning 0
    return 0


def analyze(input_dir, fit_fraction):
    """
    Go through the list of files .tif in given directory
    for each file:
        - calculate head_mean and tail_mean
        - compare current tail_mean with previous image head_mean
    """
    assert 0 < fit_fraction < 1
    
    last_head_mean = None
    last_head = None

    # visit every file .tif in the given directory in the "by name" order
    tif_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.tif')])
    for file_name in tif_files:
        # load image and convert into numpy array
        file_path = os.path.join(input_dir, file_name)
        img = Image.open(file_path)
        img_arr = numpy.array(img)
        # calculate head and tail means
        head_mean, tail_mean = head_and_tail_means(img_arr, fit_fraction)
        # compare current image tail with previous (last) image head
        if last_head_mean is not None:
            percent_diff = abs(last_head_mean - tail_mean) / last_head_mean
            percent_diff = round(100.0 * percent_diff, 2)
        else:
            percent_diff = None
        # calculate similarity size between last head and this tail
        if last_head is not None:
            this_tail = image_tail(img_arr, fit_fraction)
            common_rows_num = common_rows(last_head, this_tail)
        else:
            common_rows_num = None
        # is it a "special" place?
        significant_change = common_rows_num is not None and common_rows_num < 100
        # remember this as last
        last_head_mean = head_mean
        last_head = image_head(img_arr, fit_fraction)        
        # print information
        print(file_name, "mean(head)", head_mean, "mean(tail)", tail_mean, 
        "diff(prev)", percent_diff,
        "common(rows)", common_rows_num,
        "(!)" if significant_change else ""
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("find_temp_drift.py <directory> <fit_size>")
        sys.exit(1)
    input_dir = sys.argv[1]
    fit_size = float(sys.argv[2])

    analyze(input_dir, fit_size)
