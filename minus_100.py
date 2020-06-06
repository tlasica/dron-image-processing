"""
python3 tiff.py input.tiff output.tiff
exiftool -TagsFromFile input.tiff "-all:all>all:all" output.tiff
"""
import sys
from PIL import Image


input_file_path = sys.args[0]
output_file_path = sys.args[1]

img = Image.open(input_file_path)

out_img = Image.eval(img, lambda px: px + (-100))
out_img.save(output_file_path)

