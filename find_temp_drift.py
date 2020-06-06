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


def calculate_fit_means(img, fit_size):
    """
    Calculate averages for first and last N rows
    return pair (first_rows_avg, last_rows_avg)
    """
    img_arr = numpy.array(img)
    num_rows, num_cols = img_arr.shape
    fit_rows = int(fit_size * num_rows)
    first_rows = img_arr[:fit_rows]
    last_rows = img_arr[-fit_rows:]
    return int(first_rows.mean()), int(last_rows.mean())


def analyze(input_dir, fit_size):
    assert 0 < fit_size < 1
    tif_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.tif')])
    last_head = None
    for file_name in tif_files:
        file_path = os.path.join(input_dir, file_name)
        img = Image.open(file_path)
        head_mean, tail_mean = calculate_fit_means(img, fit_size)
        if last_head is not None:
            percent_diff = abs(last_head - tail_mean) / last_head
            percent_diff = round(100.0 * percent_diff, 2)
        else:
            percent_diff = None
        print('processing {f}: mean(head)={head} mean(tail)={tail} diff(prev)={diff}'.format(
            f=file_name, head=head_mean, tail=tail_mean, diff=percent_diff))
        last_head = head_mean


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("find_temp_drift.py <directory> <fit_size>")
        sys.exit(1)
    input_dir = sys.argv[1]
    fit_size = float(sys.argv[2])

    analyze(input_dir, fit_size)

